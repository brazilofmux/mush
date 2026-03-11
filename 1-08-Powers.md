# Powers

## Overview

Powers are named capabilities that may be granted to objects, permitting them
to perform actions that would otherwise be restricted by the permission model.
Powers provide a finer-grained permission system than flags: rather than
granting the broad privileges of WIZARD or ROYALTY, individual powers allow
targeted elevation of specific capabilities.

Powers are distinct from flags in the following ways:

1. **Granularity:** Each power enables a specific, narrowly defined capability
   (e.g., the ability to teleport, the ability to boot players), rather than a
   broad privilege class.

2. **Storage:** Powers are stored in separate bitfields from flags, with their
   own namespace.

3. **Scope:** Powers affect what an object *can do*, while flags primarily
   affect how an object *behaves* or *appears*.

A conforming implementation shall support a power system. The implementation
shall provide at least two 32-bit words for power storage (64 powers).

## Setting and Clearing Powers

Powers are granted and revoked using the `@power` command:

```
> @power <object> = <power-name>
> @power <object> = !<power-name>
```

Examples:

```
> @power #42 = tel_anywhere
> @power #42 = !boot
```

Only wizards (or God, depending on the power) may grant or revoke powers. The
specific permission level required for each power is listed in the power
catalog below.

## Standard Powers

The following powers are mandatory for a Level 2 conforming implementation. A
Level 1 implementation may support a subset, but shall document which powers
are available.

### Building and Creation Powers

| Power           | Set By  | Description |
|-----------------|---------|-------------|
| CAN_BUILD       | Wizard  | Permits the object to use building commands (`@dig`, `@create`, `@open`) even if building is restricted by server configuration. |
| OPEN_ANYWHERE   | Wizard  | Permits the object to `@open` exits from any room, regardless of room ownership or the OPEN_OK flag. |
| LINK_ANYWHERE   | Wizard  | Permits the object to `@link` exits to any room, regardless of the LINK_OK flag. |
| CREATE_PLAYER   | God     | Permits the object to use `@pcreate` to create new player objects. |

### Movement and Teleportation Powers

| Power           | Set By  | Description |
|-----------------|---------|-------------|
| TEL_ANYWHERE    | Wizard  | Permits the object to `@teleport` itself to any room, regardless of the JUMP_OK flag or teleport locks. |
| TEL_OTHER       | Wizard  | Permits the object to `@teleport` other objects, not just itself. |
| LONG_FINGERS    | Wizard  | Permits the object to interact with objects in other rooms (e.g., examining, getting, or modifying remote objects). |

### Communication Powers

| Power           | Set By  | Description |
|-----------------|---------|-------------|
| CAN_WALL        | Wizard  | Permits the object to use `@wall` to broadcast messages to all connected players. |
| PEMIT_ALL       | Wizard  | Permits the object to use `@pemit` to send messages to players with the HAVEN flag set. |
| CHAT_PRIVS      | Wizard  | Permits the object to use restricted channel operations (creating, destroying, and modifying channels). |

### Administrative Powers

| Power            | Set By  | Description |
|------------------|---------|-------------|
| CAN_BOOT         | Wizard  | Permits the object to `@boot` players, disconnecting them from the server. |
| HALT_ANYTHING    | Wizard  | Permits the object to `@halt` other objects and use `@allhalt` to stop all command queues. |
| SEARCH_EVERYTHING | Wizard | Permits the object to use `@search`, `@stats`, and `@entrances` without ownership restrictions. |
| CHANGE_QUOTAS    | Wizard  | Permits the object to modify other players' creation quotas. |
| SET_POLL         | Wizard  | Permits the object to change the server's poll (DOING header) message. |
| PS_ALL           | Wizard  | Permits the object to use `@ps` to view any player's command queue, not just its own. |
| GLOBAL_FUNCS     | Wizard  | Permits the object to add global user-defined functions via `@function`. |
| CAN_HIDE         | Wizard  | Permits the object to use the DARK flag on players to hide from the WHO list. |

### Resource and Quota Powers

| Power           | Set By  | Description |
|-----------------|---------|-------------|
| NO_PAY          | Wizard  | The object does not spend coins when performing actions that normally have a cost. |
| NO_QUOTA        | Wizard  | The object is not subject to quota restrictions when creating objects. |
| UNLIMITED_IDLE  | Wizard  | The object is not subject to idle timeout disconnection. |
| HUGE_QUEUE      | Wizard  | The object's command queue limit is raised to a very large value (implementation-defined, but typically the database size). |
| LOGIN_ANYTIME   | Wizard  | The object can connect to the server even when logins are restricted. |

### Guest and Special Powers

| Power           | Set By  | Description |
|-----------------|---------|-------------|
| IS_GUEST        | Wizard  | Marks the object as a guest with restricted capabilities. Guest objects typically cannot build, modify other objects, or perform administrative actions. |

## Power Functions

A conforming implementation shall provide the following functions for
inspecting powers:

| Function | Arguments | Returns | Level |
|----------|-----------|---------|-------|
| `powers(<object>)` | An object reference. | A space-separated list of power names set on the object. | 2 |
| `haspower(<object>, <power-name>)` | An object and a power name. | `1` if the power is granted, `0` otherwise. | 2 |

## Power Inheritance

Powers are not inherited through the parent chain. An object has only the
powers explicitly granted to it. However, when the INHERIT flag is set on an
object, commands executed by that object are evaluated with the owner's
permission level, which includes the owner's powers.

**Implementation Note:** The interaction between INHERIT and powers varies
across implementations. Some implementations pass all of the owner's powers
to inherited objects, while others pass only a subset. Softcode that depends
on specific power inheritance behavior should test on the target implementation.

## Relationship Between Powers, Flags, and Wizardry

The following diagram illustrates the relationship between the three
permission mechanisms:

```
God (#1)
  |
  +-- Has all powers and all flags implicitly
  |
Wizard (WIZARD flag)
  |
  +-- Has broad administrative access
  +-- Can grant most powers to others
  |
Royalty (ROYALTY flag)
  |
  +-- Has elevated read access
  +-- Limited administrative capabilities
  |
Powered Object (specific powers)
  |
  +-- Has only the specific capabilities granted
  +-- No implicit administrative access
  |
Normal Object (no flags or powers)
  |
  +-- Only owner-level access to owned objects
```

A wizard implicitly has all powers. A royalty object has the powers associated
with elevated read access but not administrative powers. A normal object with
specific powers has exactly those capabilities and nothing more.

This layered system allows administrators to delegate specific capabilities
without granting full wizard access.

## Implementation-Defined Powers

A conforming implementation may provide additional powers beyond those listed
above. Common implementation-specific powers include:

| Power            | Implementations    | Description |
|------------------|--------------------|-------------|
| SQL_OK           | PennMUSH, TinyMUX  | Permits the object to execute SQL queries. |
| UNKILLABLE       | RhostMUSH          | The object cannot be killed. |
| NO_CONNECT       | RhostMUSH          | Suppress connection announcements. |
| EXAMINE_ALL      | Multiple           | Permits examining any object. |
| FREE_MONEY       | RhostMUSH          | The object has unlimited coins. |
| GRAB             | RhostMUSH          | Permits getting objects from other rooms. |
| JOIN_PLAYER      | RhostMUSH          | Permits joining other players. |
| TEL_BEHIND       | RhostMUSH          | Permits pulling players through teleport. |

Implementation-defined powers shall not conflict with the names of standard
powers specified in this chapter.

## The @power Command

### Syntax

```
@power[/<switch>] <object> = <power-name>
@power[/<switch>] <object> = !<power-name>
```

### Switches

| Switch    | Description |
|-----------|-------------|
| `/list`   | Lists all available powers and their descriptions. |

### Permissions

Only wizards may grant or revoke powers, with the following exceptions:

- Powers marked "God" in the catalog above may only be granted by God (`#1`).
- No player may grant powers to an object they do not control.
- No player may grant powers they do not themselves possess, except God.

### Display

When `@examine` is used on an object with powers, the powers are displayed
in the object header or in a separate line, depending on the implementation.
The `powers()` function provides a programmatic way to retrieve the power list.
