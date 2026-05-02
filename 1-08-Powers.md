# Powers

## Overview

Powers are named capabilities that may be granted to objects, permitting
them to perform actions that would otherwise be restricted by the permission
model. Powers provide a finer-grained permission system than flags: rather
than granting the broad privileges of WIZARD or ROYALTY, individual powers
allow targeted elevation of specific capabilities.

Powers are distinct from flags in the following ways:

1. **Granularity:** Each power enables a specific, narrowly defined capability
   (e.g., the ability to teleport, the ability to boot players), rather than a
   broad privilege class.

2. **Storage:** Powers are stored in separate bitfields from flags, with their
   own namespace.

3. **Scope:** Powers affect what an object *can do*, while flags primarily
   affect how an object *behaves* or *appears*.

A Level 2 conforming implementation shall support a power-like
fine-grained permission system. Level 1 implementations may rely
solely on the flag and lock model in Chapters 7 and 27 for
permission control. (Powers are listed in the Level 2 feature set
in Chapter 34.)

### Implementation Divergence

The four reference engines diverge **substantially** on power
vocabulary and, in one case, on the underlying architecture. There is
no single agreed-upon set of standard power names, and the tables in
this chapter document per-engine availability rather than a shared
catalog.

- **PennMUSH** implements powers as `FLAG`-style entries with
  uppercase names (`Tport_Anywhere`, `Builder`, `Pemit_All`) and
  grants them via `@power` or (for some) `@set`.
- **TinyMUX** implements powers as a distinct bitfield with lowercase
  internal names (`tel_anywhere`, `builder`, `announce`) displayed in
  `@examine` output. The set is substantially smaller than
  PennMUSH's, and several PennMUSH powers (e.g., `PEMIT_ALL`,
  `CREATE_PLAYER`, `GLOBAL_FUNCS`, `HUGE_QUEUE`, `LOGIN_ANYTIME`,
  `OPEN_ANYWHERE`) do not exist in TinyMUX. TinyMUX instead gates
  the corresponding capability via the WIZARD flag or configuration.
- **TinyMUSH** largely follows TinyMUX's model and shares most of
  TinyMUX's power names.
- **RhostMUSH** has an entirely different permission architecture:
  three 32-bit *power words* (~48 powers), three *depower words* (a
  parallel set of capabilities revocable independently of WIZARD),
  eight *toggle words* (~200 toggles controlling per-object behavior),
  and a *totem* system (custom named capability groups). RhostMUSH's
  power names (`FREE_WALL`, `FREE_QUOTA`, `PCREATE`, `TEL_ANYTHING`,
  `SEARCH_ANY`, etc.) overlap only partially with PennMUSH's and
  TinyMUX's vocabularies.

Portable softcode that tests for powers should use feature detection
(`haspower()` on a named power) rather than assuming a shared
vocabulary. Administrative softcode that grants powers must branch on
the target engine.

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

## Power Catalog

The following tables catalog representative fine-grained capabilities
found across the four reference engines. Columns indicate the
PennMUSH name, the TinyMUX/TinyMUSH name (these two engines largely
agree), and the RhostMUSH name. A cell showing "—" means that engine
does not expose a directly equivalent capability through its power
system (the capability may still be available through a different
mechanism, or gated only by WIZARD). Names in these tables are
user-facing forms displayed by `@examine` and accepted by `@power`.

### Building and Creation

| Capability | PennMUSH | TinyMUX / TinyMUSH | RhostMUSH |
|------------|----------|--------------------|-----------|
| Bypass build restriction | `Builder` | `builder` | `BUILDER` |
| Open exits from any room | `Open_Anywhere` | — (WIZARD) | — |
| Link exits anywhere | `Link_Anywhere` | `link_variable` | — |
| Create player objects | `Pcreate` | — (requires WIZARD) | `PCREATE` |
| Bypass creation quota | `No_Quota` | `no_quota` | `FREE_QUOTA` |

### Movement and Teleportation

| Capability | PennMUSH | TinyMUX / TinyMUSH | RhostMUSH |
|------------|----------|--------------------|-----------|
| Teleport self anywhere | `Tport_Anywhere` | `tel_anywhere` | `TEL_ANYTHING` |
| Teleport other objects | `Tport_Anything` | `tel_anything` | `TEL_ANYTHING` (combined) |
| Interact at a distance | `Long_Fingers` | `long_fingers` | `LONG_FINGERS` |

### Communication

| Capability | PennMUSH | TinyMUX / TinyMUSH | RhostMUSH |
|------------|----------|--------------------|-----------|
| Broadcast `@wall` | `Announce` | `announce` | `FREE_WALL` |
| Pemit to HAVEN targets | `Pemit_All` | — | — |
| Channel administration | `Chat_Privs` | `cemit` (partial) | per-totem |

### Administration

| Capability | PennMUSH | TinyMUX / TinyMUSH | RhostMUSH |
|------------|----------|--------------------|-----------|
| Boot players | `Boot` | `boot` | `BOOT` |
| Halt any object / queue | `Halt_Anything` | `halt` | `HALT_ANY` |
| Unrestricted search | `Search` | — (WIZARD) | `SEARCH_ANY` |
| See any queue | `Ps_All` | `see_queue` | `SEE_QUEUE` |
| Add global `@function` | `Global_Funcs` | — (requires GOD) | — (requires WIZARD) |
| Hide from WHO | `Can_Hide` | `hide` | `HIDE` |

### Resource and Quota

| Capability | PennMUSH | TinyMUX / TinyMUSH | RhostMUSH |
|------------|----------|--------------------|-----------|
| No coin cost | `No_Pay` | `no_pay` | `FREE_MONEY` |
| No creation quota | `No_Quota` | `no_quota` | `FREE_QUOTA` |
| Ignore idle timeout | `Unlimited_Idle` | `idle` | `FREE_IDLE` |
| Raised queue limit | `Huge_Queue` | — (WIZARD via `queue_max`) | — |
| Bypass login restrictions | `Login_Anytime` | — | — |

### Guest / Special

| Capability | PennMUSH | TinyMUX / TinyMUSH | RhostMUSH |
|------------|----------|--------------------|-----------|
| Marked as guest | `Guest` | `guest` (power) | (GUEST flag) |

### Notes on the Catalog

- The PennMUSH column uses the user-facing names listed in
  PennMUSH's `help powers` output (these differ from the internal C
  macro names `CAN_BUILD`, `TEL_ANYWHERE`, etc., which readers may
  encounter in older documentation).
- Several capabilities that PennMUSH exposes as fine-grained powers
  (`Pemit_All`, `Huge_Queue`, `Login_Anytime`, `Open_Anywhere`,
  `Global_Funcs`) are either unavailable in other engines or gated
  only by the WIZARD flag. This is a genuine semantic gap, not a
  naming difference.
- RhostMUSH's depower words allow revoking a capability from a
  wizard or other privileged object — there is no direct analog in
  the other engines.
- RhostMUSH's toggle words (~200 toggles) and totems are distinct
  from the power system catalogued here; see RhostMUSH's
  `POWER_COMPARE.TXT` for the full inventory.

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
