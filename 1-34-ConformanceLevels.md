# Conformance Levels

## Overview

This chapter defines the conformance levels for implementations of this
standard. Conformance levels allow implementations to claim compliance at
different tiers, recognizing that the MUSH feature set has grown
substantially over decades and that not all features are equally essential.

## Level 1: Core Conformance

A Level 1 conforming implementation shall support the following:

### Object Model

- The four object types: ROOM, THING, EXIT, PLAYER (Chapter 5).
- Database reference numbers (dbrefs) with the `#N` syntax (Chapter 4).
- The special values NOTHING (`#-1`), AMBIGUOUS (`#-2`), and HOME (`#-3`).
- Object properties: name, owner, location, home/link, flags, attributes.
- Object creation: `@dig`, `@create`, `@open`, `@pcreate`.
- Object destruction: `@destroy`.
- The linked-list containment model for contents and exits.

### Attributes

- User-defined attributes via the `&` command and `@set`.
- Standard message attributes (DESC, SUCC, OSUCC, ASUCC, FAIL, OFAIL,
  AFAIL, DROP, ODROP, ADROP).
- Attribute flags: at minimum AF_WIZARD, AF_LOCKED, AF_VISUAL.
- Attribute inheritance via the parent chain.
- \$-commands and ^-listeners.

### Flags

- The standard flag set defined in Chapter 7, excluding flags marked
  Level 2.
- Setting and clearing flags via `@set`.

### Commands

- All commands in Chapters 15-19 not marked Level 2.
- The command parsing and dispatch pipeline (Chapter 9).
- The did_it() message pipeline.
- The six-step command matching sequence.

### Expression Evaluation

- The expression evaluator (Chapter 12).
- Percent-code substitutions (Chapter 13).
- Function calling with `[function()]` syntax.
- Brace grouping `{}` and comma-separated argument lists.

### Functions

- All functions in Chapters 20-26 not marked Level 2.
- The `u()` user-defined function mechanism.
- Register functions: `setq()`, `setr()`, `r()`.

### Locks

- The default lock type.
- Lock key expressions with at minimum: object references, AND (`&`),
  OR (`|`), NOT (`!`), and attribute locks (`:` syntax).

### Permissions

- The control predicate based on ownership.
- The WIZARD flag granting administrative control.
- God (#1) protection.

### Networking

- TCP/IP connection handling.
- The `connect` and `create` login commands.
- Multiple simultaneous connections per player.
- The `QUIT` command.

### Persistence

- Database save and load.
- Automatic periodic dumps.
- Crash recovery via emergency dumps.

## Level 2: Extended Conformance

A Level 2 conforming implementation shall support all Level 1 requirements
plus the following:

### Extended Object Model

- The `@clone` command with attribute copying.
- The `@undestroy` command for delayed destruction.
- Object identifiers (`objid()`) for distinguishing recycled dbrefs.

### Extended Attributes

- The complete standard attribute set (Chapter 6), including format
  attributes (CONFORMAT, EXITFORMAT), connection attributes (ACONNECT,
  ADISCONNECT), and enter/leave attributes.
- Attribute inheritance from the parent chain with proper override
  semantics.

### Powers

- The power system (Chapter 8).
- The standard power set.
- Granting and revoking powers via `@power`.

### Extended Locks

- All lock types defined in Chapter 27.
- Evaluation locks (`/` syntax).
- Indirect locks (`@` syntax).
- Identity (`=`), carry (`+`), and owner (`$`) lock operators.

### Extended Commands

- All commands marked Level 2 in Chapters 15-19.
- The `@switch`, `@if`, `@dolist` control flow commands.
- Queue management: `@wait` (timed and semaphore), `@notify`, `@drain`.

### Extended Functions

- All functions marked Level 2 in Chapters 20-26.
- Side-effect functions with appropriate gating.
- Higher-order list functions: `map()`, `filter()`, `fold()`.
- Regular expression functions.

### Zones

- The zone system (Chapter 29).
- Zone-based control delegation.
- The ZONE_MASTER flag and `@chzone` command.

### Systems

- The channel system (Chapter 30).
- The mail system (Chapter 31).
- SSL/TLS support is recommended but not required.

### Extended Permissions

- The ROYALTY privilege level.
- The INHERIT flag and inheritance semantics.
- The MISTRUST flag.
- Control locks (`@lock/control`).

## Conformance Claims

An implementation claiming conformance to this standard shall state:

1. The conformance level (Level 1 or Level 2).
2. Any Level 2 features supported by a Level 1 implementation (partial
   Level 2 support is permitted and encouraged).
3. Any deviations from the standard, with rationale.
4. The list of implementation-defined behaviors and their chosen values
   (see Chapter 36).

## Conformance Testing

This standard does not define a formal test suite. Implementations are
encouraged to develop and publish test suites that verify conformance at
each level. The reference implementations (TinyMUSH, TinyMUX, RhostMUSH,
PennMUSH) serve as behavioral references where this standard is ambiguous.

## Compatibility Note

Existing MUSH implementations predate this standard and may not conform
to all requirements at their current conformance level. Implementations
should document their conformance status and work toward full compliance
over time. Backward compatibility with existing databases and softcode
should be maintained where possible.
