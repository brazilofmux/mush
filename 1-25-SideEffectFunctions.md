# Side-Effect Functions

## Overview

Side-effect functions modify the game state from within expressions. Unlike
pure functions that merely compute and return values, side-effect functions
create objects, move things, set attributes, and send messages. They are the
functional equivalents of built-in commands, callable from within the
expression evaluator.

Side-effect functions are powerful but carry security implications. Most
implementations gate their availability behind a configuration option, a
flag on the calling object (such as SIDEFX), or a power. The specific
gating mechanism is implementation-defined.

A side-effect function performs its action and returns a value (often the
dbref of a created object, or an empty string). Unlike commands, side-effect
functions can be embedded in expressions, enabling compact one-line programs.

## Object Creation

### create()

```
create(<name> [, <cost>])
```

Creates a new thing with the specified \<name\>. The optional \<cost\>
parameter sets the object's recycling value. Returns the dbref of the newly
created object, or `#-1` on failure.

### open()

```
open(<exit-name>[;<aliases>] [, <destination>])
```

Creates a new exit in the executor's current room. If \<destination\> is
provided, the exit is linked to it. Returns the dbref of the new exit.
Level 2.

### dig()

```
dig(<room-name> [, <exit-to> [, <exit-back>]])
```

Creates a new room. Optionally creates exits to and from the new room.
Returns the dbref of the new room. Level 2.

### clone()

```
clone(<object>)
```

Creates a duplicate of \<object\>, copying all attributes. Returns the dbref
of the clone. Level 2.

## Object Modification

### set()

```
set(<object>, <flag>)
set(<object>, !<flag>)
set(<object>/<attribute>, <value>)
```

Sets or clears a flag on an object, or sets the value of an attribute.
Returns an empty string. This is the functional equivalent of the `@set`
command.

### attrib_set()

```
attrib_set(<object>/<attribute>, <value>)
```

Sets the value of an attribute on an object. Equivalent to the attribute-
setting form of `set()`. Level 2.

### wipe()

```
wipe(<object>[/<pattern>])
```

Removes attributes from an object. Without a pattern, removes all user-
settable attributes. With a pattern, removes only matching attributes.
Returns an empty string. Level 2.

### name()

```
name(<object>, <new-name>)
```

When called with two arguments, sets the name of \<object\> to \<new-name\>.
Returns an empty string. Level 2.

Note: With one argument, `name()` is a pure function that returns the
object's name (see Chapter 23).

## Object Destruction

### destroy()

```
destroy(<object>)
```

Destroys \<object\>, removing it from the database. Returns 1 on success,
0 on failure. Level 2.

## Movement

### tel()

```
tel(<object>, <destination>)
```

Teleports \<object\> to \<destination\>. Returns an empty string. This is the
functional equivalent of `@teleport`.

### link()

```
link(<object>, <destination>)
```

Sets the home or destination of \<object\>. Returns an empty string. Level 2.

## Communication

### pemit()

```
pemit(<target-list>, <message>)
```

Sends \<message\> to the specified targets (a space-separated list of player
dbrefs). Returns an empty string. This is the functional equivalent of
`@pemit`.

### remit()

```
remit(<room>, <message>)
```

Sends \<message\> to all objects in \<room\>. Returns an empty string. This
is the functional equivalent of `@remit`.

### oemit()

```
oemit(<object>, <message>)
```

Sends \<message\> to all objects in \<object\>'s location except \<object\>
itself. Returns an empty string. This is the functional equivalent of
`@oemit`.

### emit()

```
emit(<message>)
```

Sends \<message\> to all objects in the executor's location. Returns an empty
string. This is the functional equivalent of `@emit`. Level 2.

### lemit()

```
lemit(<message>)
```

Sends \<message\> to all objects in the executor's location. Synonym for
`emit()` in most implementations. Level 2.

### zemit()

```
zemit(<zone>, <message>)
```

Sends \<message\> to all objects in rooms belonging to the specified \<zone\>.
Returns an empty string. Level 2.

## Execution

### trigger()

```
trigger(<object>/<attribute> [, <arg0>, <arg1>, ...])
```

Triggers the specified attribute on \<object\> as an action list. Arguments
are passed as `%0` through `%9`. Returns an empty string. This is the
functional equivalent of `@trigger`.

### force()

```
force(<object>, <command>)
```

Forces \<object\> to execute \<command\>. Returns an empty string. Requires
that the caller control \<object\>. This is the functional equivalent of
`@force`. Level 2.

### wait()

```
wait(<seconds>, <action>)
wait(<object>, <action>)
```

Queues \<action\> for delayed or synchronized execution. With a numeric first
argument, waits the specified number of seconds. With an object, waits on
the object's semaphore. Returns an empty string. Level 2.

## Linking and Parenting

### parent()

```
parent(<object>, <parent>)
```

When called with two arguments, sets the parent of \<object\> to \<parent\>.
Returns an empty string. Level 2.

Note: With one argument, `parent()` is a pure function that returns the
object's parent (see Chapter 23).

### chown()

```
chown(<object>, <player>)
```

Transfers ownership of \<object\> to \<player\>. Returns an empty string.
Level 2.

### chzone()

```
chzone(<object>, <zone>)
```

Sets the zone of \<object\> to \<zone\>. Returns an empty string. Level 2.

## Locks

### lock()

```
lock(<object>, <key-expression>)
lock(<object>/<lock-type>, <key-expression>)
```

Sets a lock on \<object\>. Without a lock type, sets the default lock.
Returns 1 on success, 0 on failure. Level 2.

### unlock()

```
unlock(<object>)
unlock(<object>/<lock-type>)
```

Removes a lock from \<object\>. Returns 1 on success, 0 on failure. Level 2.

## Register Functions

While not traditionally categorized as side-effect functions, register-
setting functions modify interpreter state:

### setq()

```
setq(<register>, <value>)
```

Sets the named register to \<value\>. Returns an empty string. Registers
persist for the duration of the current action list (or until overwritten).

### setr()

```
setr(<register>, <value>)
```

Sets the named register to \<value\> and returns \<value\>. This combines
assignment and use in a single function call.

### r()

```
r(<register>)
```

Returns the current value of the named register.

## Implementation Notes

The availability of side-effect functions varies significantly across
implementations. The gating mechanisms include:

- A global configuration option enabling or disabling all side-effect
  functions.
- A per-object flag (such as SIDEFX) that must be set before an object may
  use side-effect functions.
- A power (such as SIDEFX) granted to specific objects.
- Individual configuration bits for each side-effect function.

Conforming Level 1 implementations shall support at minimum: `set()`,
`tel()`, `pemit()`, `remit()`, `oemit()`, `trigger()`, `create()`, `setq()`,
`setr()`, and `r()`.

Side-effect functions called from within `switch()`, `if()`, or similar
conditional functions are only executed if their branch is selected. This
behavior is guaranteed by the lazy evaluation semantics of conditional
functions.

**Security Note:** Side-effect functions in user-accessible attributes
(especially $-commands) must be carefully controlled. Unrestricted access
to `force()`, `tel()`, or `set()` can be used to escalate privileges.
