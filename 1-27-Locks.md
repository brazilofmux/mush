# Locks

## Overview

Locks are boolean expressions that control access to objects and their
features. When a player attempts an action -- passing through an exit,
picking up an object, entering a container, paging another player -- the
relevant lock is evaluated with the player as the test subject. If the lock
evaluates to true, the action succeeds; if false, the action is denied and
appropriate failure messages are displayed.

Locks are one of the most powerful features of the MUSH object model. Through
lock key expressions, builders create puzzles, restrict areas, implement
access control, and build interactive systems.

## Lock Types

Every object may have multiple locks, each controlling a different aspect of
interaction. Locks are set with the `@lock` command using a switch to
specify the lock type.

### Standard Lock Types

The following lock types shall be supported by all conforming implementations:

| Lock Type | Switch | Controls |
|-----------|--------|----------|
| Default   | (none) | Primary object interaction: passing exits, getting things. |
| Enter     | `/enter` | Entering a container or vehicle. |
| Leave     | `/leave` | Leaving a container. |
| Use       | `/use` | Using an object (the `use` command). |
| Drop      | `/drop` | Dropping an object from inventory. |
| Give      | `/give` | Giving an object to another player. |
| Receive   | `/receive` | Receiving objects from other players. |
| Page      | `/page` | Receiving pages from other players. |
| Teleport  | `/teleport` | Teleporting to a location. |
| Mail      | `/mail` | Receiving @mail from other players. |
| Speech    | `/speech` | Speaking in a location. |
| Command   | `/command` | Using \$-commands on an object. |
| Parent    | `/parent` | Parenting objects to this one. |
| Link      | `/link` | Linking exits to this location. |
| Control   | `/control` | Controlling this object (when CONTROL_OK is set). |
| Zone      | `/zone` | Zone membership access. |

### Extended Lock Types

The following lock types are Level 2:

| Lock Type | Switch | Controls |
|-----------|--------|----------|
| Destroy   | `/destroy` | Destroying this object (when DESTROY_OK is set). |
| Chown     | `/chown` | Changing ownership (when CHOWN_OK is set). |
| Follow    | `/follow` | Following this player. |
| Forward   | `/forward` | Forwarding messages through this object. |
| Filter    | `/filter` | Filtering messages through this location. |
| Examine   | `/examine` | Examining a VISUAL object. |
| Interact  | `/interact` | Interacting with this object (PennMUSH). |
| Listen    | `/listen` | Listening to messages (PennMUSH). |
| From      | `/from` | Receiving messages from this object (PennMUSH). |
| Pay       | `/pay` | Paying this player (PennMUSH). |
| MailForward | `/mailforward` | Forwarding mail (PennMUSH). |
| Take      | `/take` | Taking objects from this container (PennMUSH). |
| Dropto    | `/dropto` | Activating dropto on this room (PennMUSH). |
| InFilter  | `/infilter` | Filtering incoming messages (PennMUSH). |

### Per-Engine Availability Matrix

The extended lock types above are supported by some but not all
reference engines. PennMUSH implements the most complete set — its
total lock-type inventory exceeds 30 — while TinyMUX, TinyMUSH, and
RhostMUSH implement smaller, overlapping subsets. The following
matrix summarizes availability for the commonly-needed extensions;
`✓` indicates the lock is implemented, `—` indicates it is not (or
the equivalent is provided through a different mechanism).

| Lock Type  | TinyMUX | TinyMUSH | PennMUSH | RhostMUSH |
|------------|---------|----------|----------|-----------|
| Default    | ✓       | ✓        | ✓        | ✓         |
| Enter      | ✓       | ✓        | ✓        | ✓         |
| Leave      | ✓       | ✓        | ✓        | ✓         |
| Use        | ✓       | ✓        | ✓        | ✓         |
| Drop       | ✓       | ✓        | ✓        | ✓         |
| Give       | ✓       | ✓        | ✓        | ✓         |
| Receive    | ✓       | ✓        | ✓        | ✓         |
| Page       | ✓       | ✓        | ✓        | ✓         |
| Teleport   | ✓       | ✓        | ✓        | ✓         |
| Mail       | ✓ (`maillock`) | ✓ | ✓ (`Mail`) | ✓     |
| Speech     | ✓ (req. Auditorium) | ✓ (req. Auditorium) | ✓ | ✓ |
| Command    | ✓       | ✓        | ✓        | ✓         |
| Parent     | ✓       | ✓        | ✓        | ✓         |
| Link       | ✓       | ✓        | ✓        | ✓         |
| Control    | ✓       | ✓ (req. CONTROL_OK) | ✓ | ✓    |
| Zone       | (enter lock on ZMO) | (control lock + CONTROL_OK) | ✓ (`/zone`) | ✓ |
| Destroy    | —       | —        | ✓        | —         |
| Chown      | —       | —        | ✓        | —         |
| Follow     | —       | —        | ✓        | —         |
| Forward    | —       | —        | ✓        | —         |
| Filter     | —       | —        | ✓        | —         |
| Examine    | —       | —        | ✓        | —         |
| Interact   | —       | —        | ✓        | —         |
| Listen     | —       | —        | ✓        | —         |
| From       | —       | —        | ✓        | —         |
| Pay        | —       | —        | ✓        | —         |
| MailForward| —       | —        | ✓        | —         |
| Take       | —       | —        | ✓        | —         |
| Dropto     | —       | —        | ✓        | —         |
| InFilter   | —       | —        | ✓        | —         |

The divergence between PennMUSH and the other three engines on
extended lock types is substantial: roughly half of PennMUSH's lock
vocabulary has no direct equivalent elsewhere. Portable softcode that
needs fine-grained access control on non-Penn engines must typically
implement the check in softcode itself — on an attribute-matches-lock
basis — rather than rely on a hardcoded lock type.

## Lock Key Expressions

A lock key expression is a boolean formula that determines who passes the
lock. The expression is evaluated with a test subject (typically the player
attempting the action) and the locked object.

### Grammar

Lock key expressions follow this grammar, listed from lowest to highest
precedence:

```
<expression>  ::= <term> | <term> '|' <expression>
<term>        ::= <factor> | <factor> '&' <term>
<factor>      ::= '!' <factor> | <atom>
<atom>        ::= <object-ref>
                 | '=' <object-ref>
                 | '+' <object-ref>
                 | '$' <object-ref>
                 | '@' <object-ref> ['/' <lock-type>]
                 | <attribute> ':' <pattern>
                 | <attribute> '/' <pattern>
                 | '(' <expression> ')'
<object-ref>  ::= <dbref> | <name> | '#true' | '#false'
```

### Operators

| Operator | Name | Description |
|----------|------|-------------|
| `&`      | AND  | Both operands must be true. |
| `\|`     | OR   | Either operand must be true. |
| `!`      | NOT  | Inverts the result. |

Operator precedence from lowest to highest: OR, AND, NOT. Parentheses
override precedence.

### Key Types

#### Object Reference (bare name or dbref)

```
@lock exit = #42
@lock exit = Magic Key
```

Evaluates to true if the test subject **is** the specified object or
**carries** the specified object. This is the most common lock type.

#### Identity Lock (=)

```
@lock door = =Bob
```

Evaluates to true only if the test subject **is** the specified object.
Unlike bare object references, identity locks do not check inventory.

#### Carry Lock (+)

```
@lock door = +Magic Key
```

Evaluates to true only if the test subject **carries** the specified object.
Unlike bare object references, carry locks do not match the subject itself.

#### Owner Lock (\$)

```
@lock building = $Bob
```

Evaluates to true if the test subject has the same owner as the specified
object. This allows any object owned by a particular player to pass.

#### Indirect Lock (@)

```
@lock door = @#100
@lock door = @#100/enter
```

Evaluates to true if the test subject passes the specified lock on another
object. Without a lock type, the default lock is used. This enables lock
sharing and delegation.

Indirect locks are subject to a nesting depth limit (implementation-defined,
typically 20) to prevent infinite recursion.

#### Attribute Lock (colon)

```
@lock door = FACTION:Rebels
@lock door = RANK:*Captain*
```

Evaluates to true if the test subject (or an object carried by the subject)
has the named attribute set to a value matching the pattern. Wildcard matching
(`*` and `?`) is used.

#### Evaluation Lock (slash)

```
@lock door = CHECKPASS/1
```

Evaluates the named attribute on the locked object as a MUSHcode expression,
with the test subject available as `%#`. Evaluates to true if the result
equals the specified value. This is the most powerful and flexible lock type,
enabling arbitrary programmatic access control.

Evaluation locks have higher computational cost than other lock types and
are subject to expression evaluation limits.

### Boolean Constants

The special values `#true` and `#false` represent locks that always pass or
always fail, respectively. An unset lock is equivalent to `#true`.

### Compound Expressions

Lock key expressions may be combined using boolean operators:

```
@lock vault = Magic Key & =Bob
@lock club = FACTION:Rebels | FACTION:Alliance
@lock exit = !#42
@lock complex = (Key1 | Key2) & =Bob & !#99
```

## Lock Evaluation

When a lock is evaluated:

1. The lock expression is parsed into a boolean expression tree.
2. The tree is evaluated recursively with the test subject.
3. For AND expressions, both branches must be true.
4. For OR expressions, either branch must be true.
5. Implementations may use short-circuit evaluation.

### Lock Failure

When a lock evaluation fails, the object's failure message attributes are
triggered (FAIL, OFAIL, AFAIL for the default lock; type-specific failure
attributes for other locks). See Chapter 6 for the message attribute catalog.

### Lock Storage

Locks are stored as compiled boolean expressions on the object. The internal
representation is implementation-defined (tree structure, bytecode, or other
formats). The `@lock` command compiles the key expression at set time; the
`examine` command decompiles it for display.

## Commands

### @lock

```
@lock [/<lock-type>] <object> = <key-expression>
```

Sets a lock on \<object\>. Without a lock type switch, the default lock is
set. The key expression is compiled and stored on the object.

### @unlock

```
@unlock [/<lock-type>] <object>
```

Removes a lock from \<object\>, restoring it to the always-pass state.

## Implementation Notes

The evaluation lock type (`attribute/value`) is the most computationally
expensive lock type, as it invokes the full expression evaluator. Conforming
implementations shall enforce evaluation limits (recursion depth, CPU time)
during lock evaluation to prevent denial of service.

Lock nesting via indirect locks (`@`) shall be limited to prevent infinite
recursion. The nesting limit is implementation-defined but shall be at least
10 levels.

Attribute locks check both the test subject and objects in the test subject's
inventory. This enables "key" objects that grant access based on their
attributes.
