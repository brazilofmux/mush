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
> &ACONNECT me = @pemit me = Welcome back!
> &ADISCONNECT me = &LAST_SEEN me = [secs()]
```

Note: The mail system's softcode API varies by implementation. Check your
server's help for the correct function to query mail counts.

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

## Running Code as Another Object: @force

`@force` runs a command as if a different object had typed it. It is
a wizard-level primitive — you cannot `@force` an object you do not
control — but it is the foundation for many automated effects.

```
> @force me = say Hello
You say, "Hello"
> @force #412 = @emit The tavern door creaks open.
```

The first form runs `say Hello` as if you had typed it (useful mainly
in scripts). The second form makes object #412 emit a message into
its location.

### Queued vs. Immediate Execution

`@force` is **queued by default** on TinyMUX and TinyMUSH: the forced
command goes into the command queue and runs on the next cycle, not
inline with the current command. If you need the forced command to
run *right now* — for example, because its return value or side
effect must be visible before the next statement — use the `/now`
switch:

```
> @force/now #412 = @emit Tavern opens.
> think v(STATUS)         (immediate effect of the @emit's attributes)
```

Without `/now`, the `think` runs before the `@emit`.

### Control Requirements

You may `@force` only objects you control — typically ones you own,
or ones zoned to you (see Chapter 9). Wizards can force anything.
`@force` never elevates privilege: the forced command runs with the
target object's permissions, not yours.

### When to Use @force

- **Announcement objects.** Room furniture that emits ambient messages
  on a schedule can be driven by `@force <self> = @emit ...` from a
  timer.
- **Proxy commands.** A ticket machine forces itself to perform the
  side-effect of issuing the ticket.
- **Administrative automation.** Staff bots that cycle rooms,
  post announcements, or run events.

### When Not to Use @force

- **To impersonate players.** Don't. Every engine logs wizard use of
  `@force`, and forcing a player to "say" something is a serious
  breach of trust. Use `@pemit` or `@emit` to narrate *about* a
  character, not to put words in their mouth.
- **To bypass locks.** If the target object's lock denies you, forcing
  a different object through doesn't change the fact that you're
  going around a deliberate restriction.

## Granting Capabilities: @power

Building staff sometimes needs capabilities that normal players lack
— the ability to teleport freely, the ability to boot an abusive
connection, the ability to see any object's queue — without being
promoted all the way to wizard. Powers (Chapter 8 of the Standard)
fill that role on engines that implement them.

```
> @power Morgan = tel_anywhere
Morgan is granted the 'tel_anywhere' power.
> @power Morgan = !tel_anywhere
Morgan has the 'tel_anywhere' power removed.
```

Use `!` in front of the power name to revoke it.

### Available Powers Vary Sharply by Engine

The exact set of powers and their names differ between PennMUSH,
TinyMUX, TinyMUSH, and RhostMUSH — sometimes wildly. A partial
sampling:

| Capability | PennMUSH | TinyMUX |
|------------|----------|---------|
| Teleport self anywhere | `Tport_Anywhere` | `tel_anywhere` |
| Boot connections | `Boot` | `boot` |
| Bypass build restrictions | `Builder` | `builder` |
| Broadcast `@wall` | `Announce` | `announce` |

Several capabilities are PennMUSH-only (`Pemit_All`, `Huge_Queue`,
`Login_Anytime`). RhostMUSH has a completely different permission
architecture with ~48 powers, revocable "depowers," ~200 toggles, and
a totem system. Always check `help powers` on your target server for
the actual available set.

### The Right Mindset

- **Grant the narrowest power that does the job.** Don't give `Builder`
  if someone only needs to `@describe` rooms in a zone — use zones
  instead.
- **Document who has what.** A simple `&STAFF_POWERS #1 = ...` note on
  God or a staff-manager object keeps the picture legible.
- **Revoke on departure.** When a staff member steps down, sweep
  their powers. A dormant character with lingering wizard-adjacent
  capabilities is a standing security risk.

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
| `@force` | Running code as a controlled object. |
| `@force/now` | When the effect must complete before the next step. |
| `@power` | Granting narrow capabilities without promoting to wizard. |
| Zones (Ch 9) | Sharing build/edit access without transferring ownership. |
