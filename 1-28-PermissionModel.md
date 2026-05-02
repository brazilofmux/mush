# The Permission Model

## Overview

The permission model defines who may perform which actions on which objects.
It is the security foundation of a MUSH, governing everything from who can
modify an object's attributes to who can teleport across the world. The model
is built on a hierarchy of control levels, augmented by flags and powers.

## The Control Predicate

The central concept in the permission model is **control**. A player who
controls an object may modify its attributes, flags, locks, and other
properties. Control is determined by evaluating the following conditions in
order:

1. **God:** Player #1 (God) controls all objects. No object controls God
   except God itself.

2. **Control All:** A player with the `control_all` power controls all
   objects (except God).

3. **Wizard:** A player with the WIZARD flag controls all objects (except
   God). The scope of wizard control is implementation-defined but typically
   covers the entire database.

4. **Ownership:** A player controls objects they own. An object owned by
   a player is controlled by that player, provided the inheritance rules
   are satisfied (see below).

5. **Zone Control:** A player who passes the zone lock of an object's zone
   master may control that object. See Chapter 29.

The first matching condition determines the result. If no condition grants
control, the action is denied.

**Implementation extension — control lock.** TinyMUSH, PennMUSH, and
RhostMUSH provide an additional condition: if an object has the
CONTROL_OK flag set and a control lock (`@lock/control`), any player
who passes the control lock controls the object. TinyMUX does not
register a `CONTROL_OK` flag or a `/control` lock switch, so this
step is absent there. Where the control lock exists, it is evaluated
after the conditions above.

### Inheritance and the INHERIT Flag

Objects (things and exits) may inherit their owner's privilege level. An
object with the INHERIT flag set inherits wizard or royalty privileges from
its owner. Without INHERIT, an object owned by a wizard normally operates
at mortal privilege levels.

In TinyMUX, inheritance is also granted automatically when an object owns
itself (`Owner(x) == x`), or when the owner has the INHERIT flag set. This
means self-owned objects (e.g., those created by `@create` and then
`@chowned` to themselves) inherit their owner's privileges without needing
the INHERIT flag explicitly set.

This separation prevents arbitrary softcode on wizard-owned objects from
automatically having wizard powers.

The control predicate includes an inheritance check: a player controls an
owned object only if the player inherits **or** the target object does not
inherit. This prevents mortal-privilege objects from modifying
wizard-privilege objects owned by the same player.

## Privilege Hierarchy

The privilege hierarchy from highest to lowest:

| Level | Description |
|-------|-------------|
| God (Player #1) | Absolute authority. Cannot be controlled by others. |
| Wizard | Controls all objects. Can set most flags and powers. |
| Royalty | Limited administrative privileges. Level 2. |
| Power-holder | Specific elevated capabilities without full wizard access. |
| Owner | Controls owned objects. |
| Zone controller | Controls objects in managed zones. |
| Normal player | No special privileges. |

### God

Player #1 is the God character. God has the following unique properties:

- Controls all objects unconditionally.
- Cannot be controlled, @forced, or @booted by any other player.
- Is the only player who can set or clear the WIZARD flag on players.
- Is the only player who can grant the `control_all` power.
- Is typically the only player who can @toad other wizards.

### Wizards

Players with the WIZARD flag have broad administrative control:

- Control all non-God objects.
- Can examine any object.
- Can teleport any object anywhere.
- Can use remote object references (dbrefs and *player notation).
- Can set most flags and powers on other objects.
- Can @force other objects (including players).

### Royalty

Players with the ROYALTY flag have a subset of wizard capabilities. The
exact scope of royalty privileges is implementation-defined but typically
includes teleportation, hiding from the WHO list, and administrative
examination of objects. Royalty does not imply control of all objects. Level 2.

## Powers

Powers provide fine-grained privilege escalation without granting full wizard
access. A power is granted to an object using the `@power` command and can
only be granted by a wizard (or God, for certain restricted powers).

Powers interact with the permission model by enabling specific actions that
would otherwise be denied. Common permission-related powers include:

| Power | Effect |
|-------|--------|
| `control_all` | Controls all objects (God-only grant). |
| `see_all` | Can examine any object's attributes. |
| `tel_anywhere` | Can teleport to any location. |
| `tel_anything` | Can teleport any object. |
| `chown_anything` | Can change ownership of any object. |
| `pass_locks` | Automatically passes all locks. |
| `boot` | Can disconnect players. |
| `halt` | Can halt any object's queue. |
| `link_to_anything` | Can link exits to any destination. |
| `open_anywhere` | Can create exits in any room. |
| `search` | Can search the entire database. |

The complete power catalog is specified in Chapter 8.

## Permission Checks

Different operations require different permission levels. The following
table summarizes common permission requirements:

### Object Modification

| Operation | Requirement |
|-----------|-------------|
| Set attributes | Control the object. |
| Set flags | Control the object (some flags require wizard). |
| Set powers | Wizard privilege. |
| @chown | Wizard, or CHOWN_OK + target is self. |
| @destroy | Control the object (SAFE requires /override). |
| @name | Control the object (players need password). |
| @parent | Control the child; PARENT_OK on parent or control parent. |

### Movement

| Operation | Requirement |
|-----------|-------------|
| @teleport self | JUMP_OK destination, or `tel_anywhere` power. |
| @teleport other | Wizard or `tel_anything` power. |
| Traverse exit | Pass the exit's default lock. |
| Enter object | ENTER_OK on target, pass enter lock. |

### Communication

| Operation | Requirement |
|-----------|-------------|
| Page | Pass target's page lock. |
| @pemit | No special requirement (HAVEN blocks). |
| @force | Control the target. |
| @wall | Wizard flag or `can_wall` power. |

### Examination

| Operation | Requirement |
|-----------|-------------|
| Examine own object | Ownership. |
| Examine VISUAL object | Anyone (limited by OPAQUE). |
| Examine any object | Wizard or `see_all` power. |
| @search all | Wizard or `search` power. |

## The MISTRUST and TRUST Flags

PennMUSH provides a MISTRUST flag that restricts an object's ability to
exercise control beyond its direct ownership:

- A MISTRUST object cannot control other objects via zone control.
- The MISTRUST flag is available on things, exits, and rooms.

PennMUSH also provides a TRUST flag (which is an alias for INHERIT). A
TRUST object prevents other objects from controlling it (except wizards,
the owner, or other TRUST objects owned by the same player) and allows
the object to control its owner.

These flags are PennMUSH-specific. TinyMUX and TinyMUSH do not provide
them. Level 2.

## Remote Object Access

Normally, commands operate on objects in the player's current location or
inventory. Wizards (and some power-holders) can reference objects anywhere
in the database using:

- Direct dbref references: `@set #42 = DARK`
- Player name references: `@examine *Bob`

Normal players are restricted to the Nearby match context (see Chapter 10)
for most operations.

## Implementation Notes

The permission model is the most security-critical component of a MUSH
implementation. Conforming implementations shall ensure that:

- Permission checks cannot be bypassed by race conditions in the command
  queue.
- The God character (#1) is protected from modification by all other players.
- Wizard-level flags and powers cannot be self-granted by non-wizards.
- Attribute access respects both object-level and attribute-level permissions.
- Side-effect functions enforce the same permission checks as their command
  equivalents.
