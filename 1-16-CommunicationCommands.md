# Communication Commands

## Overview

Communication commands allow players to interact with each other and with the
virtual world through text. These commands are the social foundation of a MUSH,
enabling conversation, role-playing, and collaborative storytelling.

## Speech Commands

### say

```
say <message>
"<message>
```

The `say` command speaks a message to all players in the current room. The
speaker sees:

```
You say, "<message>"
```

Other players in the room see:

```
<name> says, "<message>"
```

The `"` prefix is a shortcut: `"Hello` is equivalent to `say Hello`.

### pose

```
pose <message>
:<message>
```

The `pose` command displays an action. All players in the room, including the
poser, see:

```
<name> <message>
```

A space is inserted between the name and the message. The `:` prefix is a
shortcut.

Example:

```
> :waves hello.
Bob waves hello.
```

### semipose

```
;<message>
```

The semipose is identical to `pose` except that no space is inserted between
the name and the message. This is useful for possessives and similar
constructions:

```
> ;'s eyes widen.
Bob's eyes widen.
```

## Emit Commands

### @emit

```
@emit <message>
```

The `@emit` command displays a message to all players in the current room
without any name prefix. The message appears exactly as typed.

### @pemit

```
@pemit <target-list> = <message>
```

The `@pemit` command sends a message to one or more specific objects. The
message is seen only by the named recipients. The \<target-list\> is a list
of names or dbrefs separated by spaces or commas.

The HAVEN flag does not block @pemit messages. HAVEN blocks `page` messages
and, in some implementations, the `kill` command. The PEMIT_ALL power
(PennMUSH-specific, Level 2) allows a player to @pemit to any target
regardless of other restrictions.

### @oemit

```
@oemit <object> = <message>
```

The `@oemit` command sends a message to all players in the object's location
except the specified object. This is used to show a message to everyone else
in the room.

### @remit

```
@remit <room> = <message>
```

The `@remit` command sends a message to all players in the specified room.
The sender does not need to be in the room. The sender must control the room
or have appropriate permissions.

### @femit

```
@femit <object> = <message>
```

The `@femit` command is equivalent to `@emit` but causes the message to
appear as if emitted from the specified object's location. Available in
TinyMUX, TinyMUSH, and RhostMUSH. PennMUSH does not provide this command.
Level 2.

## Remote Communication

### page

```
page <player-list> = <message>
page <player-list>
```

The `page` command sends a private message to one or more players, regardless
of their location. The sender sees:

```
You paged <name> with '<message>'.
```

The recipient sees:

```
<name> pages: <message>
```

Without a message, `page` sends a notification that the sender is looking
for the recipient.

The recipient's LPAGE lock is checked. If it fails, the page is rejected and
the sender sees the recipient's REJECT attribute (if set) or a default
rejection message.

Multiple recipients may be specified by separating names with spaces or
commas.

### whisper

```
whisper <player> = <message>
```

The `whisper` command sends a private message to a player in the same room.
Other players in the room see that the whisper occurred but do not see its
content:

```
<name> whispers something to <target>.
```

## Broadcast Commands

### @wall

```
@wall <message>
```

The `@wall` command broadcasts a message to all connected players. This
command requires the WIZARD flag or the CAN_WALL power.

The message is typically prefixed with an indicator:

```
Broadcast: <message>
```

### think

```
think <message>
```

The `think` command evaluates its argument as an expression and displays the
result to the player only. No other player sees the output. This is the
primary tool for testing expressions and debugging softcode.

## Forced Communication

### @force

```
@force <object> = <command>
```

The `@force` command causes another object to execute a command as if it had
typed it. The forced object becomes the executor of the command.

`@force` requires that the player control the target object. Wizards may
force any object. Forcing a player requires wizard privileges.

**Security Note:** `@force` is powerful and potentially dangerous. It should
be used with care, especially when the command text includes unevaluated
user input.

## Message Attributes for Communication

Several attributes affect communication behavior:

| Attribute | Description |
|-----------|-------------|
| AWAY      | Displayed to players who page this player while they are away. |
| IDLE      | Displayed to players who page this player while they are idle. |
| REJECT    | Displayed to players whose page is rejected by the LPAGE lock. |
| HAVEN     | When the HAVEN flag is set, `page` messages are blocked. |
| LSPEECH   | Lock on a room controlling who may speak in it. Requires the AUDITORIUM flag on the room in TinyMUX and TinyMUSH. |

## Speech Locks

When a room has an LSPEECH lock set, the lock is evaluated against any
player attempting to use `say`, `pose`, `semipose`, or `@emit` in that room.
If the lock fails, the player's speech is blocked and they receive an error
message.

**Implementation Note:** In TinyMUX and TinyMUSH, the LSPEECH lock is only
evaluated if the room has the AUDITORIUM flag set. Without the flag, the
lock is ignored. PennMUSH evaluates LSPEECH without requiring an additional
flag.

## Nospoof

When a player has the NOSPOOF flag set, all messages they receive are
prefixed with the source of the message in brackets:

```
[Bob(#42)] Hello, everyone!
```

This allows the player to verify the origin of messages and detect spoofing
attempts.
