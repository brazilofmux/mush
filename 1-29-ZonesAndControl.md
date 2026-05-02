# Zones and Control

## Overview

The zone system extends the basic ownership model to support collaborative
building and administration. Zones allow a group of players to share control
over a set of objects without requiring wizard privileges. A zone defines a
logical grouping of objects and a lock that determines who may administer
them.

## Zone Concepts

### Zone Master Object

A **Zone Master Object** (ZMO) is any object designated as the
administrative hub of a zone. The mechanism for designating a ZMO is
implementation-defined: PennMUSH uses a dedicated zone-master flag,
TinyMUX uses any thing referenced via the zone field with no flag
required, and TinyMUSH/RhostMUSH use a combination of flag and lock
mechanisms. See Chapter 7 for per-engine flag details.

Each ZMO carries a lock (the **zone lock**) that determines which
players are zone controllers — players authorized to modify objects
within the zone. The lock attribute and command surface vary by
engine; see "Zone Lock" below.

### Zone Membership

An object belongs to a zone when its zone field is set to a ZMO's dbref.
The zone field is set with the `@chzone` command:

```
@chzone <object> = <zone-master>
```

Objects may belong to at most one zone at a time. Setting the zone to nothing
removes the object from its zone:

```
@chzone <object> =
```

### Zone Controllers

A **zone controller** is any player who passes the ZMO's zone lock. Zone
controllers can modify objects within the zone as though they owned them,
subject to the control rules in Chapter 28. This enables collaborative
building: multiple builders can share control of a zone's rooms, exits, and
objects without needing to own every individual object.

### Shared Players

A player with the SHARED flag operates as a shared account whose objects are
collectively controlled by zone controllers. When a SHARED player is
@chzoned to a ZMO, any player passing the ZMO's zone lock can control objects
owned by the shared player. Level 2.

## Zone Control

### How Zone Control Works

When the control predicate (Chapter 28) is evaluated, zone control is
checked after ownership and before the default denial:

1. The object's zone is retrieved.
2. If the zone is a valid ZMO, the ZMO's zone lock is evaluated with the
   acting player as the test subject.
3. If the lock passes, the player is granted control of the object.

This means zone controllers can:

- Set and modify attributes on zoned objects.
- Set flags on zoned objects.
- @destroy zoned objects.
- @teleport zoned objects.
- @chown zoned objects (implementation-dependent).

Zone controllers cannot:

- Grant themselves wizard flags or powers through zoned objects.
- Modify the ZMO itself (unless they also pass its control requirements).
- Override God-level protections.

### Zone Lock

The zone lock determines who may act as a zone controller. The mechanism
for setting this lock varies across implementations:

- **PennMUSH:** Uses `@lock/zone <ZMO> = <key-expression>`.
- **TinyMUX:** Uses the enter lock (`@lock <ZMO> = <key-expression>`)
  on the ZMO. No dedicated `ZONE` flag exists or is required; zone
  membership is determined entirely by an object's zone field
  (`Zone(thing)`), and `check_zone_handler()` simply tests the enter
  lock on whichever object is referenced.
- **TinyMUSH:** Uses the control lock on the ZMO. The ZMO must have
  CONTROL_OK set to allow zone-based control delegation.

Common lock patterns (PennMUSH syntax):

```
@lock/zone ZMO = =Builder1 | =Builder2 | =Builder3
@lock/zone ZMO = FACTION:Builders
@lock/zone ZMO = +Zone Badge
```

The zone lock uses the standard lock key expression grammar (Chapter 27).

## Automatic Zone Assignment

When a player has a zone set, newly created objects may automatically inherit
the player's zone. This behavior is implementation-defined. The automatic
assignment simplifies building within a zone, as builders do not need to
manually @chzone every object they create.

## Zone Events

When an object moves between zones (entering a room in a different zone from
its previous room), zone transition events are triggered:

| Attribute | Triggered When |
|-----------|----------------|
| ZENTER    | The object enters a room in this zone. |
| OZENTER   | Others see the object enter this zone. |
| AZENTER   | Action list triggered on zone entry. |
| ZLEAVE    | The object leaves this zone. |
| OZLEAVE   | Others see the object leave this zone. |
| AZLEAVE   | Action list triggered on zone departure. |

Zone transition events are triggered on the ZMO. They fire before the
destination room's OENTER/AENTER events. These attributes are
PennMUSH-specific; TinyMUX and TinyMUSH do not support zone transition
events. Level 2.

## Zone Communication

### @zemit

```
@zemit <zone> = <message>
```

The `@zemit` command sends a message to all players in rooms belonging to the
specified zone. The sender must control the zone or be a zone controller.
Level 2.

### zemit()

```
zemit(<zone>, <message>)
```

The functional equivalent of `@zemit`. Level 2.

## Zone Information Functions

### zone()

```
zone(<object>)
```

Returns the dbref of \<object\>'s ZMO, or `#-1` if the object has no zone.

### zwho()

```
zwho(<zone>)
```

Returns a space-separated list of dbrefs of connected players who are in
rooms belonging to \<zone\>. Level 2.

### zfun()

```
zfun(<attribute> [, <arg0>, ...])
```

Evaluates \<attribute\> on the executor's ZMO, passing optional arguments.
This enables zone-wide utility functions stored on the ZMO. Level 2.

## Zone Restrictions

### Z_TEL

When a room or ZMO has the Z_TEL flag set (Level 2), objects within the zone
cannot be teleported to destinations outside the zone. The `home` command is
exempt from this restriction. This flag enables physically enclosed zones
such as puzzle areas or restricted regions.

### Flag and Power Stripping

When a non-player object is @chzoned, privileged flags and powers may
be stripped to prevent privilege escalation through zone reassignment.
The exact set stripped is implementation-defined (Chapter 36). Some
engines provide a `/preserve` switch on `@chzone` that retains the
object's privileged flags and powers — PennMUSH and RhostMUSH expose
this switch; TinyMUX has no `@chzone` switches and always strips the
configured privileged-flags set on non-player objects.

## Commands

### @chzone

```
@chzone <object> = <zone-master>
@chzone <object> =
```

Changes the zone of \<object\>. The executor must control \<object\>
and either control the zone master or pass the zone master's chzone
lock.

Setting the zone to nothing (empty right side) removes the object
from its zone.

**Switches (implementation-defined).** PennMUSH and RhostMUSH provide
`@chzone/preserve <object> = <zone-master>` to retain the object's
privileged flags and powers; the switch requires wizard privileges.
TinyMUX registers no switches for `@chzone` and always strips the
configured privileged-flag set on non-player objects.

### @chzoneall

```
@chzoneall <player> = <zone-master>
```

Changes the zone of all objects owned by \<player\> to \<zone-master\>.
Requires wizard privileges. Where supported, the `/preserve` switch
behaves as for `@chzone`. Level 2.

## Design Patterns

### Building Team Zone

A common zone pattern for collaborative building:

1. Create a zone master object: `@create Building Zone`
2. Mark it as a zone master, if the engine has a flag for that
   (PennMUSH `ZMP`/`Zone`; on TinyMUX/TinyMUSH any thing can serve as
   the ZMO without a flag).
3. Set the zone lock: `@lock/zone Building Zone = =Alice | =Bob | =Carol`
   (PennMUSH); or set the enter lock on the ZMO (TinyMUX); or set the
   control lock and enable `CONTROL_OK` (TinyMUSH). See the per-engine
   matrix in the Zone Control section above.
4. Zone the build area: `@chzone <room> = Building Zone` (for each room).

Alice, Bob, and Carol can now all modify rooms, exits, and objects in the
zone.

### Quest Zone with Shared Objects

For interactive systems where objects need shared programmability:

1. Create a shared player: `@pcreate QuestBot`
2. Set SHARED: `@set QuestBot = SHARED`
3. Create a ZMO and zone QuestBot to it.
4. Set the zone lock to the quest builders.
5. Create quest objects owned by QuestBot.

All zone controllers can now program QuestBot's objects.

## Implementation Notes

Zone control represents a delegation of authority. Conforming implementations
shall ensure that zone control cannot be used to escalate privileges beyond
what the zone controllers already possess. Specifically:

- Zone controllers shall not be able to grant themselves wizard flags or
  powers through zoned objects.
- Zone controllers shall not be able to modify the ZMO itself through zone
  control alone (additional ownership or control is required).
- The @chzone command shall strip privileged flags from non-player objects
  by default to prevent privilege transfer.

The exact set of flags stripped during @chzone is implementation-defined
but shall include at minimum the WIZARD and ROYALTY flags.
