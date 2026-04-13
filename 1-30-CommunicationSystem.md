# The Communication System (Channels)

## Overview

The channel system (also called the comsys or chat system) provides named
communication channels that span the entire game. Unlike `say` and `page`,
which are limited to a room or a specific player, channels allow groups
of players to communicate regardless of their locations. Channels are used
for out-of-character conversation, administrative coordination, faction
communication, and many other purposes.

The channel system is **optional** and **not universally present as a
core subsystem**. Of the four reference engines:

- **PennMUSH** ships a built-in channel system as part of the core
  server, exposed through the `@channel` command family.
- **TinyMUX** ships a built-in channel system with a distinct command
  surface (the `@c*` family — see below).
- **TinyMUSH** provides channels through a loadable module
  (`comsys.c`) rather than the core; installations that do not load
  the module have no comsys, and softcode access is minimal when
  loaded.
- **RhostMUSH** has no hardcoded channel system; games running on
  RhostMUSH typically supply channel behavior through softcode, which
  means command syntax and feature set vary per-installation rather
  than per-engine.

The concepts in this chapter — named channels, membership, speaking,
locks — are a useful common vocabulary for discussing channel
behavior, but a softcode author should not assume that any
standardized channel command set is available on a given server.
Engine-level feature detection (for example, checking for the
existence of `addcom` or `@ccreate`) is the only reliable approach.

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

The channel command surface diverges substantially between engines.
Two distinct families exist:

- **The `@channel/<switch>` family** (PennMUSH, RhostMUSH with its own
  switches) groups all channel operations under a single `@channel`
  command with switches selecting the operation.
- **The `@c*` family** (TinyMUX) exposes each operation as a separate
  top-level command: `@ccreate`, `@cdestroy`, `@cwho`, `@clist`,
  `@cemit`, `@cset`, `@cboot`, `@cchown`, `@coflags`, `@cpflags`,
  `@ccharge`.

TinyMUSH provides comsys as a loadable module with a minimal command
set. The examples below use the `@channel/<switch>` form for
readability; implementations that use the `@c*` form expose equivalent
semantics through the parallel commands. Portable softcode should
probe for the command form at configuration time.

### Creating and Deleting Channels

```
@channel/add <name> [= <privileges>]         (PennMUSH)
@channel/create <name> [= <privileges>]      (some PennMUSH builds)
@ccreate <name>                              (TinyMUX)
@channel/delete <name>                       (PennMUSH)
@cdestroy <name>                             (TinyMUX)
```

Creates a new channel with the specified name (and, where supported,
privilege flags) or removes an existing channel. Only the channel
owner or a wizard may delete a channel.

### Joining and Leaving

```
@channel/on <channel>                        (PennMUSH)
@channel/off <channel>                       (PennMUSH)
addcom <alias> = <channel>                   (TinyMUX, also PennMUSH)
delcom <alias>                               (TinyMUX, also PennMUSH)
```

PennMUSH's `/on` and `/off` switches add or remove the player from the
channel. TinyMUX has no equivalent switches — channel membership is
entirely managed through aliases: `addcom <alias> = <channel>` joins
a channel (creating a speaking alias at the same time) and
`delcom <alias>` leaves it. PennMUSH accepts the `addcom`/`delcom`
forms as well and treats them as the preferred way to establish a
speaking alias. Joining a channel requires passing the channel's
join lock.

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

In PennMUSH, locks are set using the `@clock` command:

```
@clock/join <channel> = <key-expression>
@clock/speak <channel> = <key-expression>
```

TinyMUX has no `@clock` command. Channel-level access is managed
through `@cset/<option>` (global channel settings), `@coflags` and
`@cpflags` (per-object-class flags), and the channel object's own
`@lock` (the enter lock on the channel's zone master object). RhostMUSH
and TinyMUSH use their own command sets. The abstract model — joined
vs. speaking access gates — is the same across engines, but the
command surface differs and portable softcode should dispatch
accordingly.

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

The softcode function surface for channels diverges sharply between
engines. PennMUSH exposes the richest per-channel introspection API;
TinyMUX has a smaller set; TinyMUSH's module exposes minimal softcode
access; RhostMUSH has no hardcoded channel functions. The table below
catalogs representative channel functions across the four engines.

| Operation | TinyMUX | PennMUSH | TinyMUSH | RhostMUSH |
|-----------|---------|----------|----------|-----------|
| Channels an object is on | `channels(<obj>)` | `channels(<obj>)` | module | — |
| List all channels | `channels()` | `channels()` | module | — |
| Send cemit (no attribution) | `cemit(<ch>,<msg>)` | `cemit(<ch>,<msg>)` | — | — |
| Channel owner | `cowner(<ch>)` / `chanobj(<ch>)` | `cowner(<ch>)` | — | — |
| Channel description | — | `cdesc(<ch>)` | — | — |
| Channel flags | — | `cflags(<ch>)` | — | — |
| Channel buffer contents | — | `cbuffer(<ch>)` | — | — |
| Channel message count | — | `cmsgs(<ch>)` | — | — |
| Channel members | `cwho(<ch>)` | `clock(<ch>,<type>)` | — | — |
| Player's channel alias | `comalias(<p>,<ch>)` | — | — | — |
| Player's channel title | `comtitle(<p>,<ch>)` | `ctitle(<ch>,<p>)` | — | — |

Portable softcode that introspects channels should feature-detect by
function name and branch on the engine, or restrict itself to
`channels(<obj>)` (which is the only function whose name and
semantics overlap on multiple engines).

### channels()

```
channels([<object>])
```

With an object argument, returns a space-separated list of channels
that \<object\> is on. Without an argument (TinyMUX and PennMUSH),
returns all channels visible to the caller.

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
