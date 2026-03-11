# The Communication System (Channels)

## Overview

The channel system (also called the comsys or chat system) provides named
communication channels that span the entire game. Unlike `say` and `page`,
which are limited to a room or a specific player, channels allow groups
of players to communicate regardless of their locations. Channels are used
for out-of-character conversation, administrative coordination, faction
communication, and many other purposes.

The channel system is Level 2. Implementations may differ in command syntax
and administrative features, but the core concepts described here are common
to all major implementations.

## Channel Properties

Each channel has the following properties:

| Property | Description |
|----------|-------------|
| Name | The channel's unique name (case-insensitive). |
| Owner | The player who created the channel. |
| Description | A brief description of the channel's purpose. |
| Privileges | Flags controlling who may join, speak, and administer. |
| Locks | Boolean key expressions controlling access. |

## Channel Commands

### Creating and Deleting Channels

```
@channel/add <name> [= <privileges>]
@channel/delete <name>
```

The `/add` switch creates a new channel with the specified name and optional
privilege flags. The `/delete` switch removes a channel. Only the channel
owner or a wizard may delete a channel.

### Joining and Leaving

```
@channel/on <channel>
@channel/off <channel>
```

The `/on` switch adds the player to the channel. The `/off` switch removes
the player from the channel. Joining a channel requires passing the
channel's join lock.

Some implementations support aliases for MUX compatibility:

```
addcom <alias> = <channel>
delcom <alias>
```

These create a short alias that can be used as a prefix for speaking on the
channel.

### Speaking on Channels

```
@chat <channel> = <message>
+<channel> <message>
<alias> <message>
```

Sends a message to all players on the channel. The message is broadcast
with the speaker's name and the channel name as context.

Channel speech supports the same communication modes as room speech:

| Prefix | Mode | Example Output |
|--------|------|----------------|
| (none) | Say | `[Channel] Player says, "message"` |
| `:`    | Pose | `[Channel] Player message` |
| `;`    | Semipose | `[Channel] Playermessage` |

### Channel Information

```
@channel/list
@channel/who <channel>
```

The `/list` switch displays all visible channels with their descriptions and
member counts. The `/who` switch displays the players currently on a
specific channel.

## Channel Locks

Channels support multiple lock types that control different aspects of
access:

| Lock | Controls |
|------|----------|
| Join | Who may join the channel. |
| Speak | Who may speak on the channel (while joined). |
| See | Who may see the channel in listings. |
| Hide | Who may hide their presence on the channel. |
| Mod | Who may modify channel settings. |

Locks are set using the `@clock` command:

```
@clock/join <channel> = <key-expression>
@clock/speak <channel> = <key-expression>
```

Lock key expressions use the same grammar as object locks (Chapter 27).

## Channel Privileges

Channel privilege flags control broad access categories:

| Flag | Description |
|------|-------------|
| Player | Only players (not objects) may join. |
| Object | Objects may join the channel. |
| Admin | Only royalty and wizards may join. |
| Wizard | Only wizards may join. |
| Quiet | Suppress join/leave/connect/disconnect notices. |
| Open | Players may speak without joining. |
| Hide_OK | Players may hide on the channel. |

The set of privilege flags and their characters is implementation-defined.

## Channel Administration

```
@channel/privs <channel> = <privileges>
@channel/chown <channel> = <player>
@channel/rename <channel> = <new-name>
@channel/describe <channel> = <description>
@channel/wipe <channel>
```

These commands modify channel properties. The `/chown` switch transfers
ownership (wizard only). The `/wipe` switch removes all members from the
channel.

## Channel Formatting

Implementations may support custom formatting of channel output through
attributes on the receiving object:

- A `@chatformat` attribute, when set, is evaluated to produce the
  channel output seen by that object. This enables per-player customization
  of channel display.

- A mogrifier object may be assigned to a channel to transform messages
  before broadcast.

The specifics of formatting customization are implementation-defined.

## Channel Functions

### channels()

```
channels(<object>)
```

Returns a space-separated list of channel names that \<object\> is on.

### cemit()

```
cemit(<channel>, <message>)
```

Sends a message to a channel without speaker attribution. Requires
appropriate permissions.

### cowner()

```
cowner(<channel>)
```

Returns the dbref of the channel's owner.

## Channel Recall

Some implementations maintain a buffer of recent messages for each channel.
Players joining a channel or reconnecting may view recent history:

```
@channel/recall <channel> [= <count>]
```

The buffer size is configurable per channel. This feature is
implementation-defined.

## Implementation Notes

Channel storage is separate from the main object database. Channels are
typically stored in a dedicated file (e.g., `chatdb`) that is loaded at
startup and saved during database dumps.

The channel system is distinct from the `@listen` and `^` pattern-matching
system. Channels provide structured, named communication groups, while
listeners provide pattern-triggered responses to room-level speech.

Conforming Level 2 implementations that provide a channel system shall
support at minimum: channel creation and deletion, joining and leaving,
speaking on channels, and channel listing.
