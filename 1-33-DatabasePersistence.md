# Database Persistence

## Overview

The MUSH database contains all objects, attributes, flags, locks, and other
game state. Database persistence ensures that this state survives server
restarts, crashes, and planned shutdowns. This chapter specifies the
requirements for saving, loading, and recovering the database.

## Database Contents

The database stores the following information for each object:

| Data | Description |
|------|-------------|
| Dbref | The object's database reference number. |
| Type | The object type (ROOM, THING, EXIT, PLAYER). |
| Name | The object's name (including aliases for exits). |
| Flags | All flags set on the object. |
| Powers | All powers granted to the object. |
| Owner | The dbref of the owning player. |
| Location | The dbref of the containing object. |
| Contents | The head of the contents linked list. |
| Exits | The head of the exits linked list (rooms only). |
| Next | The next object in the contents/exits list. |
| Home/Link | The home location or exit destination. |
| Parent | The parent object dbref. |
| Zone | The zone master dbref. |
| Money | The object's currency balance. |
| Attributes | All attributes and their values, flags, and owners. |
| Locks | All lock expressions. |
| Timestamps | Creation time, last modification time. |

## Database Dump

### The @dump Command

```
@dump [/paranoid]
```

The `@dump` command forces an immediate database save. This creates a
checkpoint of the current database state. The `/paranoid` switch performs
additional consistency checks during the dump. Requires wizard privileges.

### Automatic Dumps

The server shall automatically save the database at regular intervals. The
dump interval is configurable (implementation-defined default, commonly
3600 seconds / 1 hour). The dump interval and offset are set in the server
configuration file.

### Dump Process

When a database dump occurs:

1. A broadcast message is optionally sent to connected players.
2. Internal caches are synchronized (attribute cache, property cache).
3. The database epoch counter is incremented.
4. The database is written to disk.
5. A completion message is optionally broadcast.

### Forking Dumps

To avoid freezing the game during database saves, conforming implementations
should support forking dumps. In a forking dump:

1. The server process calls `fork()` to create a child process.
2. The child process writes the database to disk.
3. The parent process continues running the game.
4. The child process exits when the dump is complete.

This takes advantage of operating system copy-on-write memory semantics:
the child process sees a consistent snapshot of the database at the moment
of the fork, even as the parent continues modifying it.

If forking is unavailable or fails, the server shall fall back to a
non-forking dump, during which the game pauses until the save completes.

## Flat File Format

A conforming implementation shall support a flat file (text) database format
for portability and recovery. The flat file format is implementation-defined
in its details but shall include:

1. A header identifying the format and version.
2. One record per object, containing all object data.
3. Attribute records with name, value, flags, and owner.
4. Lock expressions in a parseable text representation.
5. A terminator line (commonly `***END OF DUMP***`) to verify file
   integrity.

The flat file format enables:

- Database migration between server versions.
- Manual inspection and editing of game state.
- Recovery from corrupted binary database files.

### Dump and Load

Implementations typically provide commands or utilities for flat file
operations:

- `@dump/flatfile` or a command-line utility to export the database.
- A startup option or utility to import a flat file database.

## Database Epoch

Each database dump increments an epoch counter. Database files are often
named with their epoch number to maintain a history of recent dumps. This
enables rollback to a previous dump if the current one is corrupted.

## Crash Recovery

A conforming implementation shall provide crash recovery mechanisms:

1. On unclean shutdown (crash, signal, power failure), the server should
   attempt to write an emergency dump before exiting.
2. On startup, the server shall check for emergency dump files (commonly
   named with a `.CRASH` or `.KILLED` suffix).
3. If an emergency dump exists and is newer than the regular database, the
   server shall load from the emergency dump.
4. The server shall verify database integrity by checking for the
   terminator line.

### Panic Dumps

When the server detects a fatal error (segmentation fault, assertion
failure, etc.), it shall attempt to save the database before exiting. This
panic dump may be a flat file or binary dump, depending on the nature of
the error and the state of internal data structures.

## Database Startup Sequence

When the server starts:

1. Check for crash recovery files.
2. Load the database (from the newest valid file).
3. Verify database consistency.
4. Initialize the object free list (garbage collection of destroyed
   objects).
5. Load auxiliary databases (mail, channels, etc.).
6. Open network ports and begin accepting connections.

## Database Consistency

The server shall maintain internal consistency of the database:

- All linked-list pointers (contents, exits, next) shall form valid chains.
- All location references shall point to valid objects.
- All owner references shall point to valid player objects.
- Destroyed objects shall be properly recycled.

The `@dbck` command (or equivalent) performs an on-demand consistency check
and repairs common issues.

## Storage Backends

The internal storage format is implementation-defined. Common approaches
include:

| Backend | Description |
|---------|-------------|
| Flat file | Text format, loaded entirely into memory. |
| GDBM | GNU database manager, key-value store. |
| LMDB | Memory-mapped key-value store with transactions. |
| Custom binary | Implementation-specific binary format. |

The choice of backend affects performance and memory usage but shall not
affect the observable behavior of the game.

## Shutdown Sequence

When the server shuts down (via `@shutdown` or signal):

1. A broadcast message is sent to all connected players.
2. All connected players are disconnected (triggering ADISCONNECT).
3. The command queue is drained or discarded.
4. The database is saved.
5. Auxiliary databases (mail, channels) are saved.
6. Network ports are closed.
7. The server process exits.

The `@shutdown/abort` command cancels a pending shutdown if the
implementation supports delayed shutdown.

## Implementation Notes

Database size is limited primarily by available memory, as most
implementations load the entire database into RAM. Implementations should
document their maximum supported database size.

The dump interval should balance data safety against I/O load. Frequent
dumps provide better crash recovery but increase disk I/O. Forking dumps
mitigate the performance impact.

Conforming implementations shall ensure that a complete dump cycle (from
initiation to file close) produces a consistent database image. Partial
or corrupted dumps shall be detectable (via the terminator line or
checksums) and shall not overwrite the previous valid dump.
