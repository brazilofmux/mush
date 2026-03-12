# Flags and Toggles

## Overview

Flags are boolean properties of objects. Each flag represents a single on/off
state that modifies the object's behavior, indicates its status, or controls
access permissions. Flags are the primary mechanism for configuring object
behavior beyond what attributes provide.

A conforming implementation shall store flags as bitfields. The number of flag
words (32-bit integers used for storage) is implementation-defined, but a
conforming implementation shall support at least three flag words (96 flags).

**Compatibility Note:** TinyMUSH and TinyMUX use three 32-bit flag words.
RhostMUSH uses four flag words. PennMUSH uses a dynamic flag system with no
fixed limit. All approaches are conforming.

## Setting and Clearing Flags

Flags are set and cleared using the `@set` command:

```
> @set <object> = <flag-name>
> @set <object> = !<flag-name>
```

Examples:

```
> @set me = DARK
> @set #42 = !STICKY
> @set here = JUMP_OK
```

The `!` prefix clears (removes) a flag. Without the prefix, the flag is set.

### Flag Setting Permissions

Not all flags can be set by all players. Each flag has an associated permission
level that determines who may set or clear it:

| Permission Level | Who May Set |
|-----------------|-------------|
| Any             | Any player on objects they control. |
| Wizard          | Only wizards (objects with WIZARD flag). |
| Royalty         | Wizards and royalty. |
| God             | Only God (`#1`). |
| Internal        | Set by the server only; cannot be set by any user. |

The specific permission level for each flag is listed in the flag catalog
below.

### Type Restrictions

Many flags apply only to certain object types. Setting a flag on an object of
the wrong type shall have no effect or shall produce an error message. The
applicable types for each flag are listed in the flag catalog.

## Flag Display

When a player examines an object, its flags are shown as part of the object
header. Flags are displayed as a string of single-character codes following
the object's dbref:

```
> examine me
Player Name(#42PWc)
```

In this example, `P` indicates the PLAYER type, `W` indicates the WIZARD flag,
and `c` indicates the CONNECTED flag.

Type flags are always displayed:

| Character | Type |
|-----------|------|
| `R`       | ROOM |
| (none)    | THING (things have no type character) |
| `E`       | EXIT |
| `P`       | PLAYER |

## Standard Flags

The following flags are mandatory for a conforming implementation. They are
organized by functional category.

### Visibility and Display Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| DARK        | `D`  | All         | Any        | Hides the object. On rooms, suppresses the contents list. On things and players, hides them from the room's contents display. On exits, hides them from the exits list. |
| OPAQUE      | --   | All         | Any        | Prevents players from seeing the contents of the object. On rooms, contents of objects in the room are hidden. |
| LIGHT       | --   | All         | Any        | The object is visible even in a DARK room. Overrides DARK on the room for this specific object. |
| VISUAL      | `V`  | All         | Any        | All attributes on this object are visible to everyone, as if every attribute had AF_VISUAL set. |
| TRANSPARENT | `t`  | All         | Any        | Alias for SEETHRU. Allows looking through the object to see the other side. |
| TERSE       | `q`  | Players     | Any        | The player sees only room names, not full descriptions, when moving. |
| MYOPIC      | `m`  | Players     | Any        | The player sees objects as if they were not the owner and not a wizard. |

### Movement and Location Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| STICKY      | `S`  | Things/Rooms | Any       | On things: the thing goes home when dropped. On rooms: activates dropto behavior (see Chapter 5). |
| JUMP_OK     | `J`  | Rooms       | Any        | Any player may `@teleport` to this room. |
| LINK_OK     | `L`  | Rooms       | Any        | Any player may `@link` exits to this room. |
| ABODE       | `A`  | Rooms       | Any        | Any player may set this room as their home using `@link`. |
| ENTER_OK    | `e`  | Things      | Any        | Players may `enter` this object. |
| HAVEN       | `H`  | Rooms/Players | Any      | On rooms: the `kill` command is disabled. On players: pages are blocked. |
| FLOATING    | `F`  | Rooms       | Any        | Suppresses the "floating room" warning for rooms not connected to the exit network from `#0`. |
| UNFINDABLE  | `U`  | All         | Any        | The object cannot be located by `@whereis` or `loc()` from a remote location. |

### Control and Permission Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| WIZARD      | `W`  | Players     | God        | Grants full administrative privileges. See Chapter 28 for the complete list of wizard capabilities. |
| ROYALTY     | --   | Players     | Wizard     | Grants elevated read access and limited administrative capabilities. |
| INHERIT     | `I`  | All         | Any        | The object inherits its owner's permission level when executing commands. Without this flag, objects execute at basic permission level regardless of their owner's privileges. |
| CHOWN_OK    | `C`  | Things      | Any        | Any wizard may `@chown` this object without the owner's intervention. |
| DESTROY_OK  | `d`  | All         | Any        | Any player who controls the object may destroy it without the SAFE flag check. |
| SAFE        | `s`  | All         | Any        | The object cannot be destroyed by `@destroy` unless the `/override` switch is used. |
| CONTROL_OK  | --   | All         | Any        | The object's LCONTROL lock determines who has control, in addition to the owner and wizards. |
| PARENT_OK   | --   | All         | Any        | Any player may `@parent` other objects to this one. |

### Communication Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| PUPPET      | `p`  | Things      | Any        | The object relays all messages it receives to its owner. |
| MONITOR     | `M`  | All         | Any        | Enables ^-listen pattern matching on the object's attributes. Required for ^-listeners to function. |
| NOSPOOF     | `N`  | Players     | Any        | The server prefixes messages with the originator's identity, preventing spoofed communication. |
| QUIET       | `Q`  | All         | Any        | Suppresses routine success messages (e.g., "Set." after `@set`). |
| VERBOSE     | `v`  | All         | Any        | The object reports every command it executes to its owner. Used for debugging. |
| AUDIBLE     | --   | All         | Any        | Messages from inside the object are relayed to the object's location. Works with FORWARDLIST. |

### Execution and Debugging Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| HALT        | `h`  | All         | Any        | The object cannot execute any commands. All queue entries for this object are discarded. |
| TRACE       | `T`  | All         | Any        | Enables evaluation tracing. When set, the server displays each function call and its result during expression evaluation. |
| GOING       | `G`  | All         | Internal   | The object has been scheduled for destruction. Set by `@destroy`, cleared if the destruction is canceled. This flag shall not be directly settable by users. |

### Player State Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| CONNECTED   | `c`  | Players     | Internal   | The player has at least one active network connection. Set and cleared by the server. This flag shall not be directly settable by users. |
| SUSPECT     | `u`  | Players     | Wizard     | The player is under administrative monitoring. Commands executed by SUSPECT players may be logged. |
| SLAVE       | `x`  | Players     | Wizard     | The player is restricted to a minimal command set. Used for newly created or restricted accounts. |
| GUEST       | --   | Players     | Wizard     | The player is a guest account with reduced privileges. |
| ROBOT       | `r`  | Players     | Any        | The player is a program-controlled account, not a human user. |
| IMMORTAL    | `i`  | Players     | God        | The player cannot be killed. |

### Building Flags

| Flag        | Char | Types        | Permission | Description |
|-------------|------|-------------|------------|-------------|
| OPEN_OK     | --   | Rooms       | Any        | Any player may `@open` exits from this room, subject to the LOPEN lock. |

### Zone Flags

| Flag          | Char | Types     | Permission | Description |
|---------------|------|----------|------------|-------------|
| ZONE_MASTER   | --   | All      | Any        | Marks this object as a zone master. See Chapter 29 for zone behavior. |
| ZONE_CONTENTS | --   | All      | Any        | When set on a zone master, objects in the zone master's contents list are searched for \$-commands. |
| ZONE_PARENT   | --   | Things   | Any        | When set, this zone master also acts as a parent for objects in the zone. |

**Compatibility Note:** Zone flag names and behaviors vary across
implementations. Some implementations use ZONE as an object type rather than a
flag. This standard specifies zone behavior through flags to accommodate all
implementations.

## Implementation-Defined Flags

A conforming implementation may provide additional flags beyond those listed
above. Common implementation-specific flags include:

| Flag        | Implementations     | Description |
|-------------|---------------------|-------------|
| ANSI        | TinyMUSH, RhostMUSH | Enables ANSI color code processing for the player. |
| HTML        | TinyMUSH            | Enables HTML output for the player. |
| GAGGED      | TinyMUSH, TinyMUX   | Prevents the player from speaking or posing. |
| STAFF       | TinyMUSH            | Staff-level access between royalty and wizard. |
| VACATION    | TinyMUSH            | Indicates the player is on extended absence. |
| CLOAK       | RhostMUSH           | Hides the player from WHO but more thoroughly than DARK. |
| FUBAR       | RhostMUSH           | Severely restricts the player's capabilities. |
| INDESTRUCTIBLE | RhostMUSH        | The object cannot be destroyed under any circumstances. |
| MARKER0-MARKER9 | TinyMUSH, TinyMUX | Ten general-purpose marker flags for administrative use. |

Implementation-defined flags shall not conflict with the names of standard
flags specified in this chapter. If an implementation provides a flag with
behavior that overlaps a standard flag, it shall use the standard name.

## Flag Functions

A conforming implementation shall provide the following functions for
inspecting and testing flags:

| Function | Arguments | Returns | Level |
|----------|-----------|---------|-------|
| `flags(<object>)` | An object reference. | A string of flag characters representing all flags set on the object. | 1 |
| `hasflag(<object>, <flag-name>)` | An object and a flag name. | `1` if the flag is set, `0` otherwise. | 1 |
| `set(<object>, <flag-name>)` | An object and a flag name (with optional `!` prefix). | Sets or clears the flag. Returns empty string on success. Side-effect function. | 2 |

The `flags()` function returns the same flag character string shown in the
`@examine` header. The exact set of characters and their order is
implementation-defined, but the type character shall appear first.

## Toggle System

Some implementations provide a **toggle** system separate from flags. Toggles
function identically to flags but use a separate namespace and storage. This
standard does not require a separate toggle system; implementations may
implement all boolean properties as flags.

**Compatibility Note:** RhostMUSH maintains a separate toggle system with
its own set of names and permission controls. TinyMUSH and TinyMUX implement
all boolean properties as flags. PennMUSH uses a unified dynamic flag system.
For portability, softcode should use `hasflag()` for all boolean property
checks.
