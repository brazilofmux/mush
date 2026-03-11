# Movement and Look

## Overview

Movement and look commands are the most basic interactions in a MUSH. They
allow players to navigate the virtual world and perceive their surroundings.
These commands are used constantly during normal play and form the foundation
of the user experience.

## look

### Syntax

```
look [<object>]
look/<switch> [<object>]
```

### Description

The `look` command displays information about an object or the player's
current location. Without an argument, `look` displays the current room.

When looking at a room, the display shall include:

1. The room's name.
2. The room's DESC attribute (evaluated as an expression).
3. The ADESC action list is triggered (if set).
4. A list of visible exits (unless the room is DARK or the EXITFORMAT
   attribute provides custom formatting).
5. A list of visible contents -- players and things in the room (unless the
   room is DARK or the CONFORMAT attribute provides custom formatting).

When looking at an object (thing, player, or exit), the display shall include
the object's name and DESC attribute. The ADESC action list is triggered.

### Switches

| Switch     | Description | Level |
|------------|-------------|-------|
| `/outside` | When inside an object, look at the outside instead of the inside. | 2 |

### Name Matching

The `look` command uses the Nearby match context (see Chapter 10). If no
argument is given, it displays the current room.

### Permissions

Any player may look at objects in their current location and at objects they
carry. Looking at objects in other locations requires the LONG_FINGERS power
or other special access.

DARK objects are not displayed in contents lists but may be looked at
directly by name if the player knows the name.

## go / move

### Syntax

```
go [/quiet] <direction>
<direction>
```

### Description

The `go` command moves the player through an exit. The \<direction\> argument
is matched against exit names and aliases in the current room (see Chapter 9,
"Command Parsing and Dispatch," Step 3).

In practice, players rarely type `go`; they simply type the exit name:

```
> north
> n
> go north
```

All three forms are equivalent.

### Movement Sequence

When a player successfully traverses an exit, the following sequence occurs:

1. The exit's default lock is evaluated. If it fails, the exit's FAIL, OFAIL,
   and AFAIL attributes are triggered, and movement does not occur.
2. The exit's SUCC and OSUCC are displayed in the departure room. ASUCC is
   triggered.
3. The departure room's LEAVE, OLEAVE, and ALEAVE attributes are triggered.
   The arrival room's OXENTER is displayed in the departure room.
4. The player is moved to the exit's destination.
5. The exit's DROP and ODROP are displayed in the arrival room. ADROP is
   triggered.
6. The player's MOVE, OMOVE, and AMOVE attributes are triggered.
7. The arrival room's ENTER, OENTER, and AENTER attributes are triggered.
   The departure room's OXLEAVE is displayed in the arrival room.
8. The player automatically looks at the new room.

### Switches

| Switch   | Description | Level |
|----------|-------------|-------|
| `/quiet` | Suppress movement messages. | 2 |

## home

### Syntax

```
home
```

### Description

The `home` command moves the player to their home location (the location
stored in their home/link field). The player's departure and arrival messages
are triggered normally.

If the player's home location is invalid (destroyed or otherwise
inaccessible), the player is moved to the player starting room (commonly
`#0`, but the actual room is an implementation-defined configuration
parameter).

## enter

### Syntax

```
enter [/quiet] <object>
```

### Description

The `enter` command moves the player inside a thing that has the ENTER_OK
flag set. The object must be in the same room as the player. Enter may also
be triggered by typing an object's EALIAS.

The enter lock (LENTER) is evaluated. If it fails, the EFAIL, OEFAIL, and
AEFAIL attributes are triggered.

On success, the SUCC, OSUCC, and ASUCC of the object are triggered in the
departure location. The player is moved inside the object and sees its IDESC
(interior description) or DESC.

## leave

### Syntax

```
leave [/quiet]
```

### Description

The `leave` command moves the player out of an object they have entered,
returning them to the room containing that object. Leave may also be
triggered by typing the containing object's LALIAS.

The leave lock (LLEAVE) is evaluated. If it fails, the LFAIL, OLFAIL, and
ALFAIL attributes are triggered.

## @teleport

### Syntax

```
@teleport [/quiet] [<object> =] <destination>
@teleport [/quiet] [<object> =] home
```

### Description

The `@teleport` command moves an object to a destination without requiring a
connecting exit. Without a left-hand argument, the player teleports
themselves.

### Permissions

- A player may teleport themselves to any room with the JUMP_OK flag set.
- A player with the TEL_ANYWHERE power may teleport themselves anywhere.
- A player with the TEL_OTHER power may teleport other objects.
- Wizards may teleport any object anywhere.
- The destination's LTPORT lock is checked. If it fails, teleportation is
  denied.
- The origin's LTELOUT lock is checked. If it fails, teleportation from that
  location is denied.

### Message Sequence

1. OXTPORT is triggered in the departure room (announcing the impending
   departure to others).
2. The object is moved to the destination.
3. TPORT, OTPORT, and ATPORT are triggered in the arrival room.
4. The object sees the new room (if a player).

## inventory

### Syntax

```
inventory
```

### Description

The `inventory` command displays the contents of the player's inventory
(objects the player is carrying) and the player's current currency balance.

## score

### Syntax

```
score
```

### Description

The `score` command displays the player's current currency balance. The
currency name is implementation-defined (commonly "Pennies").

## use

### Syntax

```
use <object>
```

### Description

The `use` command attempts to use an object. The object's use lock (LUSE) is
evaluated. On success, the USE, OUSE, and AUSE attributes are triggered. On
failure, the UFAIL, OUFAIL, and AUFAIL attributes are triggered.

The `use` command does not inherently do anything beyond triggering the
message pipeline. The object's AUSE attribute provides the actual
functionality.

## Displaying Exits

When a room is displayed (via `look`), the available exits are shown. The
default display lists the display names of all non-DARK exits, typically
formatted as:

```
Obvious exits:
North  South  East
```

If the room has an EXITFORMAT attribute, it is evaluated and used instead
of the default display. EXITFORMAT receives the list of exit dbrefs and can
produce custom formatting.

## Displaying Contents

When a room is displayed, the contents (players and things) are listed. The
default display shows the names of all non-DARK objects in the room.

If the room has a CONFORMAT attribute, it is evaluated and used instead of
the default display. CONFORMAT receives the list of content dbrefs and can
produce custom formatting.
