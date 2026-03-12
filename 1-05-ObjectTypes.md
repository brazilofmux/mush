# Object Types

## Overview

Every object in the database has exactly one type. The type is assigned at
creation and is immutable -- it cannot be changed after the object exists. The
type determines which properties are meaningful for the object, how the object
participates in the location hierarchy, and what commands and behaviors apply
to it.

A conforming implementation shall support the following four object types:

| Type Code | Type   | Description |
|-----------|--------|-------------|
| 0         | ROOM   | A location that can contain objects and have exits. |
| 1         | THING  | A portable object that can be carried, dropped, and manipulated. |
| 2         | EXIT   | A one-way link between locations. |
| 3         | PLAYER | A user-controlled object with network connectivity. |

An implementation may define additional internal types (such as GARBAGE for
destroyed objects or ZONE for zone master objects), but these are not
user-creatable object types and are not specified by this standard except
where noted.

**Compatibility Note:** TinyMUSH and RhostMUSH define TYPE_ZONE as type code
4 for zone master objects. PennMUSH uses bitwise type flags rather than small
integer type codes. These internal representations are implementation details;
this standard specifies only the four user-visible types and their behaviors.

## Rooms

### Description

A room represents a location in the virtual world. Rooms are the fundamental
containers of the MUSH environment. Every thing and every player exists inside
a room (or inside an object that is itself inside a room, recursively).

### Creation

Rooms are created with the `@dig` command:

```
> @dig The Grand Hall
The Grand Hall created as room #42.
```

The `@dig` command may optionally create exits to and from the new room in a
single operation:

```
> @dig The Grand Hall = North;north;n, South;south;s
The Grand Hall created as room #42.
Exit "North" created as exit #43.
Exit "South" created as exit #44.
Trying to link...
Linked exit #43 to The Grand Hall(#42).
Linked exit #44 to <current room>.
```

### Properties

| Property   | Applicable | Description |
|------------|-----------|-------------|
| Location   | Yes       | The dropto destination. When a room has a dropto set, it affects how dropped objects are handled (see "Dropto Behavior" below). If NOTHING, dropped things remain in the room. |
| Contents   | Yes       | The players and things currently present in this room. |
| Exits      | Yes       | The exits leading from this room to other locations. |
| Home       | No        | Not applicable to rooms. |
| Owner      | Yes       | The player who owns this room. |
| Parent     | Yes       | The room's parent, for attribute and command inheritance. |
| Zone       | Yes       | The room's zone master, if any. |

### Name Requirements

A room's name shall be a non-empty string. Room names are not required to be
unique. Room names may contain spaces and most printable characters.

### Dropto Behavior

When a room has a dropto set (i.e., its location field is not NOTHING), the
following behavior applies:

1. When a player drops an object that has the STICKY flag set, the object is
   sent to its HOME location, not to the dropto and not to the room.
2. When a player drops a non-STICKY object in a non-STICKY room with a
   dropto, the object is sent to the dropto location instead of remaining
   in the room.
3. When a room has the STICKY flag set and has a dropto, and all players
   leave the room, any remaining non-STICKY objects are swept to the dropto
   location.
4. If the dropto is HOME, objects are sent to their individual home locations.

**Implementation Note:** The STICKY flag on an object and the STICKY flag on
a room serve different purposes. A STICKY object goes HOME when dropped. A
STICKY room enables the sweep-on-empty behavior for its dropto.

### Room Flags

The following flags have special meaning when set on rooms:

- **FLOATING:** Suppresses the "Floating room" warning for rooms not connected
  to the exit network.
- **JUMP_OK:** Allows players to teleport into this room.
- **LINK_OK:** Allows any player to link exits to this room.
- **ABODE:** Allows players to set this room as their home.
- **HAVEN:** Prevents the `kill` command from being used in this room.
- **DARK:** Suppresses the display of the room's contents list when a player
  looks at the room. Unfindable objects in a DARK room are hidden from
  `@whereis` and similar commands.
- **OPAQUE:** When set on a room, prevents players from seeing the contents
  of objects in the room.

## Things

### Description

A thing is a portable object. Things can represent items, containers, vehicles,
furniture, machines, abstract systems, or any other entity that is not a
location, a connection, or a user. Things are the most versatile object type
and serve as the primary building blocks for interactive softcode systems.

### Creation

Things are created with the `@create` command:

```
> @create Magic Sword
Magic Sword created as object #50.
```

The newly created thing is placed in the creating player's inventory.

An optional cost parameter specifies the recycling value of the object:

```
> @create Magic Sword = 100
Magic Sword created as object #50.
```

### Properties

| Property   | Applicable | Description |
|------------|-----------|-------------|
| Location   | Yes       | The room, player, or thing that currently contains this thing. |
| Contents   | Yes       | Objects contained within this thing (if it is used as a container). |
| Exits      | Yes       | Exits attached to this thing (for vehicle or portable-exit applications). |
| Home       | Yes       | The location to which this thing is sent by the `home` command or when its current location is destroyed. |
| Owner      | Yes       | The player who owns this thing. |
| Parent     | Yes       | This thing's parent, for attribute and command inheritance. |
| Zone       | Yes       | This thing's zone master, if any. |

### Name Requirements

A thing's name shall be a non-empty string. Thing names are not required to be
unique. Thing names may contain spaces and most printable characters.

### Home Behavior

Every thing has a home location. The home is set at creation to the creating
player's current room and can be changed with `@link`. When one of the
following occurs, the thing is sent to its home:

1. The thing has the STICKY flag set and is dropped by a player (the thing
   is sent HOME regardless of the room's dropto setting).
2. The room containing the thing is destroyed.
3. The thing's location becomes invalid for any reason.

### Container Behavior

Things may contain other objects. A thing with the ENTER_OK flag set allows
players to enter it using the `enter` command. Things used as containers
participate in the contents list mechanism described in Chapter 4.

### Puppet Behavior

A thing with the PUPPET flag set relays all messages it receives to its owner.
This allows a player to observe events in a location where the player is not
present.

## Exits

### Description

An exit is a one-way connection between two locations. Exits are the mechanism
by which players move through the virtual world. An exit is attached to a
source location and linked to a destination.

### Creation

Exits are created with the `@open` command:

```
> @open North;north;n = #42
Exit "North" created as exit #55.
Linked exit #55 to The Grand Hall(#42).
```

The `@open` command creates the exit in the current room. If a destination is
specified, the exit is linked to that destination. If no destination is
specified, the exit is created unlinked (destination is NOTHING).

### Properties

| Property   | Applicable | Description |
|------------|-----------|-------------|
| Location   | Yes       | The room (or thing) to which this exit is attached -- i.e., its source. |
| Contents   | No        | Exits do not contain objects. |
| Exits      | No        | Exits do not have sub-exits. |
| Home       | No        | Not applicable to exits. |
| Owner      | Yes       | The player who owns this exit. |
| Parent     | Yes       | This exit's parent, for attribute inheritance. |
| Zone       | Yes       | This exit's zone master, if any. |
| Link       | Yes       | The destination to which this exit leads. May be a room, a thing (for entering objects), or HOME. |

### Name Requirements and Aliases

An exit's name has special structure. It consists of one or more names
separated by semicolons. The first name is the **display name**, shown when
the exit is listed. The remaining names are **aliases** that can be used to
traverse the exit.

```
North;north;n
```

In this example, `North` is the display name, and `north` and `n` are aliases.
A player can type any of these three names to use the exit.

Exit names shall not be empty. At least one name (the display name) is
required.

### Traversal

When a player types a command that matches an exit name in the player's current
room, the following sequence occurs:

1. The exit's **default lock** is evaluated against the player. If the lock
   fails, the exit's FAIL and OFAIL messages are displayed, and its AFAIL
   action list is executed. The player does not move.

2. If the lock succeeds, the exit's SUCC and OSUCC messages are displayed in
   the departure room, and the ASUCC action list is executed.

3. The player is moved to the exit's destination.

4. The destination room's contents are displayed to the player (equivalent to
   a `look`).

5. The exit's DROP and ODROP messages are displayed in the arrival room, and
   the ADROP action list is executed.

### Unlinked Exits

An exit with destination NOTHING is **unlinked**. An unlinked exit exists in
its source room's exit list, but attempting to traverse it results in a
message indicating that the exit leads nowhere.

### Exit Linking

An exit may be linked to:

- A **room:** The standard case. Traversing the exit moves the player to the
  destination room.
- A **thing:** Traversing the exit causes the player to enter the thing (as if
  they had typed `enter <thing>`).
- **HOME:** Traversing the exit sends the player to their home location.

An exit shall not be linked to a player or to another exit.

The `@link` command sets or changes an exit's destination:

```
> @link north = #42
Linked.
```

### Exit Matching Priority

When a player types a command, exits are matched before \$-commands but after
built-in commands. If multiple exits match the typed text, the behavior is
implementation-defined; implementations should select one at random or present
a disambiguation message.

See Chapter 9, "Command Parsing and Dispatch," for the complete command
matching order.

## Players

### Description

A player represents a human user of the MUSH. Players are similar to things --
they occupy rooms, carry objects in their inventory, and can have attributes
and flags -- but they have additional capabilities related to network
connectivity, authentication, and command execution.

### Creation

Players are created in one of two ways:

1. **Self-registration:** A user at the connect screen types `create <name>
   <password>`, creating a new player and connecting to it. Whether self-
   registration is permitted is a server configuration option.

2. **Administrative creation:** A wizard uses `@pcreate <name> = <password>`
   to create a player without connecting to it.

### Properties

| Property   | Applicable | Description |
|------------|-----------|-------------|
| Location   | Yes       | The room in which the player is currently present. |
| Contents   | Yes       | The objects in the player's inventory. |
| Exits      | Yes       | Exits attached to the player (for personal exits, rarely used). |
| Home       | Yes       | The player's home location, where they are sent by the `home` command. |
| Owner      | Yes       | The player itself. Players always own themselves. |
| Parent     | Yes       | The player's parent, for attribute and command inheritance. |
| Zone       | Yes       | The player's zone master, if any. |

### Name Requirements

Player names are subject to stricter requirements than other object types:

1. Player names shall be unique across the database. No two players may have
   the same name (comparison is case-insensitive).
2. Player names shall not begin with a number or the character `#`.
3. Player names shall not contain the characters `=`, `&`, `|`, or other
   characters that conflict with command parsing. The exact set of prohibited
   characters is implementation-defined but shall include at minimum: `[`, `]`,
   `{`, `}`, `(`, `)`, `;`, `,`, `"`, and whitespace other than spaces.
4. Player names shall be at least one character long.

### Connection and Disconnection

A player is **connected** when at least one network connection is authenticated
to that player. A player may have multiple simultaneous connections. The
CONNECTED flag indicates whether a player currently has any active connections.

When a player connects:

1. The CONNECTED flag is set on the player.
2. The ACONNECT attribute on the player, the player's location, and the master
   room are executed (if they exist).
3. The player is shown the room description (equivalent to `look`).
4. The player's LAST attribute is updated with the connection timestamp.

When a player disconnects (last connection closes):

1. The ADISCONNECT attribute on the player, the player's location, and the
   master room are executed (if they exist).
2. The CONNECTED flag is cleared.

### Player-Specific Attributes

The following attributes have special meaning on player objects:

- **ALIAS:** Alternative names by which the player can be addressed.
- **PASSWORD:** The player's hashed password. This attribute is not readable
  by any user, including God, through normal attribute access. Its storage
  format is implementation-defined.
- **LAST:** The timestamp of the player's most recent connection.
- **LASTSITE:** The hostname or IP address of the player's most recent
  connection.
- **MONEY:** The player's currency balance (pennies, credits, or whatever
  unit the game uses). The name of the currency is configurable.
- **QUOTA:** The number of additional objects the player is permitted to
  create, if quota enforcement is enabled.
- **SEX:** The player's grammatical gender, used for pronoun substitution
  (`%s`, `%o`, `%p`, `%a`).

### Player-Specific Flags

The following flags have special meaning on player objects:

- **WIZARD:** Grants unrestricted administrative access (see Chapter 28).
- **ROYALTY:** Grants elevated read access and limited administrative
  capabilities.
- **CONNECTED:** Set by the server when the player is connected; cleared
  when disconnected. This flag shall not be settable by users.
- **SUSPECT:** Marks the player for monitoring. Commands executed by SUSPECT
  players may be logged.
- **GUEST:** Marks the player as a guest account with restricted privileges.
- **SLAVE:** Restricts the player to a minimal command set.

## Type Predicates

A conforming implementation shall provide the following functions for testing
an object's type:

| Function       | Returns |
|----------------|---------|
| `type(<obj>)`  | The type name as a string: `ROOM`, `THING`, `EXIT`, or `PLAYER`. The return value for destroyed or invalid objects is implementation-defined. |
| `hastype(<obj>, <type>)` | `1` if the object is of the named type, `0` otherwise. |
| `isdbref(<string>)` | `1` if the string is a syntactically valid dbref, `0` otherwise. Level 2. |

**Compatibility Note:** The `type()` function is universal across all four
implementations. For destroyed objects, PennMUSH returns `GARBAGE`, TinyMUX
and TinyMUSH return `#-1 ILLEGAL TYPE`, and RhostMUSH returns `#-1 NOT FOUND`.
The `hastype()` function is available in TinyMUSH, TinyMUX, and PennMUSH.
RhostMUSH provides equivalent functionality. The `isdbref()` function is not
available in all implementations and is therefore Level 2.

## Type Comparison Table

The following table summarizes the capabilities of each object type:

| Capability                     | ROOM | THING | EXIT | PLAYER |
|-------------------------------|------|-------|------|--------|
| Has location                   | (1)  | Yes   | Yes  | Yes    |
| Has contents                   | Yes  | Yes   | No   | Yes    |
| Has exits                      | Yes  | Yes   | No   | Yes    |
| Has home                       | No   | Yes   | No   | Yes    |
| Has owner                      | Yes  | Yes   | Yes  | (2)    |
| Can be carried                 | No   | Yes   | No   | No     |
| Can contain objects             | Yes  | Yes   | No   | Yes    |
| Can have exits attached        | Yes  | Yes   | No   | Yes    |
| Can be entered                 | Yes  | (3)   | No   | No     |
| Can execute commands            | No   | (4)   | No   | Yes    |
| Can connect to the network     | No   | No    | No   | Yes    |
| Name must be unique            | No   | No    | No   | Yes    |
| Created by                     | @dig | @create | @open | @pcreate / create |

Notes:

1. A room's location field stores its dropto destination, not a containing
   object.
2. A player always owns itself.
3. Things with ENTER_OK set can be entered by players.
4. Things can execute action lists and \$-commands, but cannot directly receive
   user input from the network.
