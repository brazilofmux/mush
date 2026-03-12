# Advanced Programming Patterns

## Overview

This chapter covers techniques used by experienced MUSHcode programmers:
parent-based inheritance, data storage patterns, event-driven design,
semaphores, and performance optimization.

## Parent-Based Code Organization

Instead of putting code on every object, use a parent object to hold shared
code. All children inherit the parent's attributes:

```
> @create NPC Parent
> &CMD_TALK NPC Parent = $talk to *:@pemit %# =
  [name(me)] says, "[default(me/DIALOGUE, I have nothing to say.)]"
> &CMD_LOOK NPC Parent = $look at *:@pemit %# =
  [default(me/APPEARANCE, An unremarkable person.)]

> @create Baker
> @parent Baker = NPC Parent
> &DIALOGUE Baker = Fresh bread today! Best in the city!
> &APPEARANCE Baker = A heavyset woman with flour-dusted arms.

> @create Guard
> @parent Guard = NPC Parent
> &DIALOGUE Guard = Move along, citizen. Nothing to see here.
```

Both the Baker and the Guard respond to `talk to` and `look at` using the
parent's code, but with their own data.

### Overriding Parent Behavior

A child can override a parent's attribute by defining its own:

```
> &CMD_TALK Guard = $talk to *:@pemit %# =
  [name(me)] glares at you. "I said move along."
```

The Guard now has a custom response while the Baker still uses the parent's.

## Data Storage Patterns

### Attribute-Based Data

The simplest storage pattern uses one attribute per value:

```
> &HEALTH me = 100
> &MANA me = 50
> &LEVEL me = 5
```

### Delimited Data

Store multiple values in a single attribute using delimiters:

```
> &STATS me = 100|50|5|Warrior|Human
```

Access with `elements()` or `extract()` using a custom delimiter:

```
> &FN_GET_HEALTH me = first(v(STATS), |)
> &FN_GET_CLASS me = extract(v(STATS), 4, 1, |)
```

### Attribute Trees

Use hierarchical attribute names for structured data:

```
> &SKILL_SWORDS me = 75
> &SKILL_MAGIC me = 30
> &SKILL_STEALTH me = 50
```

List all skills with a wildcard:

```
> think lattr(me/SKILL_*)
SKILL_SWORDS SKILL_MAGIC SKILL_STEALTH
```

Process them:

```
> &CMD_SKILLS me = $+skills:@pemit %# =
  [iter(lattr(me/SKILL_*),
    [ljust(after(##, SKILL_), 15)][rjust(v(##), 3)]%r)]
```

```
> +skills
SWORDS           75
MAGIC            30
STEALTH          50
```

## Event-Driven Design

### ^-Listeners

A `^`-pattern attribute triggers when matching text appears in the room:

```
> @set me = MONITOR
> &LISTEN me = *
> &AHEAR me = @switch %0 = *help*, {@pemit %# = Type +help for
  assistance.}
```

Or using a `^`-listener attribute:

```
> &^KNOCK me = ^knock*:@emit Someone knocks on the door.
```

When anyone in the room says something containing "knock", the emit fires.

### ACONNECT and ADISCONNECT

Run code when a player connects or disconnects:

```
> &ACONNECT me = @pemit me = Welcome back! You have
  [mail(me)] mail messages.
> &ADISCONNECT me = &LAST_SEEN me = [secs()]
```

### Zone-Based Events

If you have a zone, you can set events on the Zone Master Object that
fire for all objects in the zone:

```
> &AZENTER ZMO = @pemit %# = You enter the Enchanted Forest zone.
```

## Semaphores

Semaphores prevent race conditions when multiple commands try to modify the
same data simultaneously:

```
> &CMD_DEPOSIT atm = $deposit *:@wait me = {
  @set me/BALANCE = [add(v(BALANCE), %0)];
  @pemit %# = Deposited %0. Balance: [v(BALANCE)];
  @notify me
}
```

The `@wait me` queues the action on the object's semaphore. Only one
semaphore-queued action runs at a time. `@notify me` releases the
semaphore for the next queued action.

Without a semaphore, two simultaneous deposits might both read the same
balance before either writes, causing one deposit to be lost.

## Error Handling

### Input Validation

Always validate player input:

```
> &CMD_HEAL me = $+heal *:@switch 1 =
  [not(isnum(%0))], {@pemit %# = Amount must be a number.},
  [lt(%0, 1)], {@pemit %# = Amount must be positive.},
  [gt(%0, v(MANA))], {@pemit %# = Not enough mana.},
  {@set me/HEALTH = [min(add(v(HEALTH), %0), v(MAXHEALTH))];
   @set me/MANA = [sub(v(MANA), %0)];
   @pemit %# = Healed for %0. Health: [v(HEALTH)] Mana: [v(MANA)]}
```

### Default Values

Use `default()` to handle missing attributes:

```
> think default(me/NONEXISTENT, 0)
0
```

## Performance Tips

### Minimize Function Calls

Every function call has overhead. Instead of:

```
> think add(1, add(2, add(3, add(4, 5))))
```

Use:

```
> think add(1, 2, 3, 4, 5)
```

Many functions (`add`, `mul`, `cat`, `strcat`) accept multiple arguments.

### Cache Repeated Lookups

If you use the same value multiple times, store it in a register:

```
> think [setq(loc, loc(me))][name(r(loc))] has
  [words(lcon(r(loc)))] objects
Town Square has 5 objects
```

Without the register, `loc(me)` would be evaluated twice.

### Use Attribute Trees Over Search

Instead of searching the entire database:

```
> think search(type=THING FLAG=MARKER)    <-- Expensive
```

Store references in attributes:

```
> &MARKED_OBJECTS me = #100 #200 #300     <-- Fast lookup
```

## Code Organization Conventions

Experienced coders follow naming conventions:

| Prefix | Purpose |
|--------|---------|
| `CMD_` | \$-command attributes. |
| `FN_` | User-defined functions (called with u()). |
| `DO_` | Action lists (called with @trigger). |
| `DATA_` | Data storage attributes. |
| `CONF_` | Configuration values. |
| `HELP_` | Help text for commands. |

## Debugging

### The TRACE Flag

Set the TRACE flag on an object to see every function evaluation:

```
> @set me = TRACE
> think add(mul(2, 3), 4)
```

You will see each function call and its result. Remove TRACE when done:

```
> @set me = !TRACE
```

### @ps: Viewing the Queue

```
> @ps
```

Shows pending commands in the queue. Useful for finding runaway code.

### @halt: Stopping Runaway Code

```
> @halt me
```

Clears all pending queue entries for your character. Use this if code is
looping out of control.

## Quick Reference

| Pattern | When To Use |
|---------|------------|
| Parent objects | Shared behavior across similar objects. |
| Attribute trees | Structured data with dynamic keys. |
| Semaphores | Preventing data races in concurrent access. |
| `ulocal()` | Calling functions without register leakage. |
| Register caching | Avoiding repeated expensive lookups. |
| Input validation | Every command that accepts player input. |
| TRACE flag | Debugging complex expressions. |
