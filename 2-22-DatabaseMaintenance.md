# Database Maintenance

## Overview

The MUSH database is a single file that stores every object, attribute,
flag, and piece of data in the game. Keeping it healthy is one of the
most important responsibilities of a server administrator. This chapter
covers how the database works, how to back it up, and how to recover
from problems.

## How the Database Works

A MUSH database is a flat file containing a serialized representation of
all objects. Each object entry includes:

- The dbref, name, and type.
- Location, contents, exits, and owner.
- All flags and powers.
- All attributes and their values.

The server loads the entire database into memory at startup and operates
on it in memory during play. Periodically, it writes a snapshot back to
disk. This is called a **dump** or **database save**.

## Database Dumps

### Automatic Dumps

The server saves automatically at intervals set in the configuration:

```
dump_interval 3600
```

This saves every 3600 seconds (one hour). Some servers default to 30
minutes. During a dump, the server may briefly pause or fork a child
process to write the file without blocking gameplay.

### Manual Dumps

Trigger a save at any time:

```
> @dump
Database save started.
```

Always do a manual dump before:

- Shutting down the server.
- Making major changes to important objects.
- Any risky administrative operation.

### Forked Dumps

Older MUSH servers (and PennMUSH, TinyMUSH, RhostMUSH today) fork a
child process to write the database, so players do not experience lag
during the save. If your server supports forked dumps, ensure the
system has enough memory for both parent and child processes; the
configuration option is usually:

```
fork_dump yes
```

TinyMUX 2.14 replaces the fork-for-save approach with Write-Ahead
Logging (WAL) checkpoints, which stream changes to disk continuously
and therefore never fork the process for a periodic save. On
TinyMUX 2.14 the `fork_dump` option only affects `@dump/flatfile`
exports; periodic saves proceed transparently regardless of the
setting.

## Backups

### Why Back Up?

Database corruption, accidental `@destroy` commands, bad code, and
hardware failures can all cause data loss. Backups are your insurance.

### Backup Strategy

A simple daily backup script:

```
#!/bin/bash
DB=data/netmush.db
BACKUP_DIR=data/backups
DATE=$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP_DIR"
cp "$DB" "$BACKUP_DIR/netmush-$DATE.db"
# Keep 30 days of backups
find "$BACKUP_DIR" -name "*.db" -mtime +30 -delete
```

Run this from cron daily or after each clean shutdown.

### What to Back Up

- **The database file.** This is essential.
- **The configuration file.** Stores all your settings.
- **Softcode exports.** Text files of important objects exported with
  `@decompile` or similar tools.
- **Log files.** Useful for forensics if something goes wrong.

## Database Cleanup

Over time, databases accumulate unused objects. Regular cleanup keeps
things manageable.

### Finding Garbage

Look for objects with no obvious purpose:

```
> @search type=THING owner=me
> @find whatever                    (search by name substring)
```

`@find` takes a name substring, not a type keyword: use `@search` for
filtering by type or owner. `@find =THING` does not work in any major
engine — it treats the empty string as the name pattern and then
fails or returns nothing.

Objects left by departed players, abandoned builds, and test objects
all contribute to bloat.

### @destroy

Remove unwanted objects:

```
> @destroy #42
```

Most servers delay actual destruction until the next database save,
giving you a chance to recover with `@undestroy` if you make a mistake.

### @purge

Some servers have a `@purge` command that immediately reclaims destroyed
objects:

```
> @purge
```

### Quota Audits

Check what players own the most objects:

```
> @stats/all
```

Players who have left the game may have hundreds of objects consuming
database space. Consider recycling them or chowning them to a storage
player.

## Database Repair

### Flat File Format

If the database becomes corrupted, you may need to edit the flat file
directly. The flat file is a text format that can be opened in any
editor. Objects look something like:

```
!42
name Baker
location 5
...
```

**Make a backup before editing the flat file.** Even experienced
administrators can make things worse with a misplaced edit.

### Common Problems

| Problem | Solution |
|---------|----------|
| Server will not start. | Check the log for error messages. Often a corrupted object at a specific dbref. |
| Missing objects after crash. | Restore from the most recent backup. |
| Circular containment. | An object is inside itself. Fix with flat file editing. |
| Orphaned exits. | Exits pointing to destroyed rooms. Use `@find` to locate and `@destroy` to clean up. |

### Recovery Process

1. Stop the server.
2. Copy the corrupted database aside (do not delete it).
3. Try loading a recent backup.
4. If no backup works, edit the flat file to fix the specific problem.
5. Restart and verify.

## Monitoring Database Health

Keep an eye on these metrics:

```
> @stats
Total objects: 5,421
Rooms: 342  Things: 3,890  Exits: 1,102  Players: 87
Garbage: 15
```

Watch for:

- **Rapid object growth** that does not match building activity.
- **High garbage counts** that are not being reclaimed.
- **Database file size** growing faster than expected.

## Tips

- **Automate backups.** Do not rely on remembering to do them manually.
- **Test your recovery process.** Restore a backup to a test instance
  periodically to make sure your backups actually work.
- **Keep the flat file format documented.** If you ever need to hand-edit
  the database, you will want a reference.
- **Monitor disk space.** A full disk during a database dump can corrupt
  the file.
- **Use @dump before risky operations.** It takes seconds and can save
  hours of recovery work.
