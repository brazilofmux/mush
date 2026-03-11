# Object and Database Functions

## Overview

Object and database functions retrieve information about objects in the
database: their names, locations, types, flags, attributes, and
relationships. These functions are the primary means by which MUSHcode
programs inspect and interact with the game world.

## Object Identification

### name()

```
name(<object>)
```

Returns the name of \<object\>. For exits, returns only the primary name
(before the first semicolon).

### fullname()

```
fullname(<object>)
```

Returns the full name of \<object\>, including all aliases for exits
(semicolon-separated). Level 2.

### num()

```
num(<name>)
```

Returns the dbref of the object matching \<name\>, using the standard name
matching rules (see Chapter 10). Returns `#-1` if no match is found,
`#-2` if the match is ambiguous.

### dbref()

```
dbref(<number>)
```

Returns the dbref formed by prepending `#` to \<number\>. Does not validate
whether the dbref refers to an existing object.

### objid()

```
objid(<object>)
```

Returns the unique object identifier for \<object\>, typically in the form
`#<dbref>:<creation-time>`. This identifier distinguishes between an object
and any future object that may reuse the same dbref. Level 2.

## Location and Containment

### loc()

```
loc(<object>)
```

Returns the dbref of the location containing \<object\>.

### where()

```
where(<object>)
```

Returns the dbref of \<object\>'s true location. For most objects, this is
identical to `loc()`. Level 2.

### room()

```
room(<object>)
```

Returns the dbref of the room ultimately containing \<object\>. If the object
is inside a thing which is inside a room, `room()` returns the room.

### rloc()

```
rloc(<object>, <depth>)
```

Returns the location of \<object\> after traversing \<depth\> levels of
containment. `rloc(<object>, 0)` returns the object itself;
`rloc(<object>, 1)` is equivalent to `loc(<object>)`.

### home()

```
home(<object>)
```

Returns the dbref of \<object\>'s home location.

### owner()

```
owner(<object>)
```

Returns the dbref of the player who owns \<object\>.

### zone()

```
zone(<object>)
```

Returns the dbref of \<object\>'s zone master, or `#-1` if the object has
no zone.

### parent()

```
parent(<object>)
```

Returns the dbref of \<object\>'s parent, or `#-1` if the object has no
parent.

### lparent()

```
lparent(<object>)
```

Returns a space-separated list of dbrefs in \<object\>'s parent chain,
starting with the object itself and ending with the ultimate ancestor.

### children()

```
children(<object>)
```

Returns a space-separated list of dbrefs of all objects whose parent is
\<object\>.

## Contents and Exits

### con()

```
con(<object>)
```

Returns the dbref of the first object in \<object\>'s contents list. Returns
`#-1` if the contents are empty.

### lcon()

```
lcon(<object>)
```

Returns a space-separated list of all dbrefs in \<object\>'s contents.

### next()

```
next(<object>)
```

Returns the dbref of the next object in the same contents or exit list as
\<object\>. Returns `#-1` if \<object\> is the last in the list.

### exit()

```
exit(<room>)
```

Returns the dbref of the first exit in \<room\>'s exit list. Returns `#-1`
if the room has no exits.

### lexits()

```
lexits(<room>)
```

Returns a space-separated list of all exit dbrefs in \<room\>.

### entrances()

```
entrances(<object>)
```

Returns a space-separated list of dbrefs of all exits linked to \<object\>,
objects whose home is \<object\>, and other links to \<object\>.

### nearby()

```
nearby(<object1>, <object2>)
```

Returns 1 if \<object1\> and \<object2\> are in the same location (or one
contains the other), and 0 otherwise.

## Type and Flag Information

### type()

```
type(<object>)
```

Returns the type name of \<object\>: `ROOM`, `THING`, `EXIT`, or `PLAYER`.

### hastype()

```
hastype(<object>, <type>)
```

Returns 1 if \<object\> is of the specified \<type\>, and 0 otherwise.

### flags()

```
flags(<object>)
```

Returns a string of flag characters set on \<object\>. Each flag is
represented by its single-character abbreviation.

### hasflag()

```
hasflag(<object>, <flag-name>)
```

Returns 1 if \<object\> has the named flag set, and 0 otherwise.

### powers()

```
powers(<object>)
```

Returns a space-separated list of power names granted to \<object\>.

### haspower()

```
haspower(<object>, <power-name>)
```

Returns 1 if \<object\> has the named power, and 0 otherwise.

## Attribute Access

### get()

```
get(<object>/<attribute>)
```

Returns the raw (unevaluated) value of \<attribute\> on \<object\>. Returns
an empty string if the attribute does not exist.

### get_eval()

```
get_eval(<object>/<attribute>)
```

Returns the evaluated value of \<attribute\> on \<object\>. The attribute
is evaluated in the context of the calling object.

### xget()

```
xget(<object>, <attribute>)
```

Returns the raw value of \<attribute\> on \<object\>. Equivalent to
`get(<object>/<attribute>)` but uses two arguments instead of a slash-
separated single argument.

### v()

```
v(<attribute>)
```

Returns the value of \<attribute\> on the executing object. Equivalent to
`get(%!/<attribute>)`. This is the most efficient way to read an attribute
on the current object.

### eval()

```
eval(<object>, <attribute>)
```

Returns the evaluated value of \<attribute\> on \<object\>. The attribute is
evaluated in the context of \<object\>.

### u()

```
u(<object>/<attribute> [, <arg0>, <arg1>, ...])
```

Calls a user-defined function. The value of \<attribute\> on \<object\> is
evaluated with the supplied arguments available as `%0` through `%9`.
See Chapter 14 for the full specification of `u()`.

### ulocal()

```
ulocal(<object>/<attribute> [, <arg0>, <arg1>, ...])
```

Same as `u()`, but preserves the calling context's registers. Any register
changes made during the function call are reverted when it returns.

### default()

```
default(<object>/<attribute>, <default-value>)
```

Returns the value of \<attribute\> on \<object\>, or \<default-value\> if the
attribute does not exist or is empty.

### edefault()

```
edefault(<object>/<attribute>, <default-value>)
```

Returns the evaluated value of \<attribute\> on \<object\>, or the evaluated
\<default-value\> if the attribute does not exist or is empty.

### udefault()

```
udefault(<object>/<attribute>, <default-value> [, <arg0>, ...])
```

Calls \<attribute\> as a user function (like `u()`), or evaluates
\<default-value\> if the attribute does not exist or is empty.

### hasattr()

```
hasattr(<object>, <attribute>)
```

Returns 1 if \<attribute\> exists on \<object\> (even if empty), and 0
otherwise.

### hasattrval()

```
hasattrval(<object>, <attribute>)
```

Returns 1 if \<attribute\> exists on \<object\> and has a non-empty value,
and 0 otherwise.

### lattr()

```
lattr(<object> [/<pattern>])
```

Returns a space-separated list of attribute names on \<object\>. If
\<pattern\> is specified (using wildcards), only matching attribute names are
returned.

### nattr()

```
nattr(<object>)
```

Returns the number of attributes set on \<object\>.

### lattrp()

```
lattrp(<object> [/<pattern>])
```

Returns a space-separated list of attribute names on \<object\>, including
attributes inherited from the parent chain. Level 2.

## Object Evaluation

### objeval()

```
objeval(<object>, <expression>)
```

Evaluates \<expression\> as though \<object\> were the executor. The
permissions of \<object\> apply during evaluation. This function requires
that the caller control \<object\>.

### objmem()

```
objmem(<object>)
```

Returns the approximate memory usage of \<object\> in bytes. The calculation
method is implementation-defined.

## Database Search

### search()

```
search([<player>] [<class>=<restriction>])
```

Searches the database for objects matching the specified criteria. Returns a
space-separated list of matching dbrefs. Common search classes:

| Class    | Restriction | Description |
|----------|-------------|-------------|
| `type`   | TYPE        | Objects of the specified type. |
| `name`   | PATTERN     | Objects with matching names. |
| `flags`  | FLAG-LIST   | Objects with specified flags. |
| `parent` | DBREF       | Objects with the specified parent. |
| `zone`   | DBREF       | Objects in the specified zone. |
| `powers` | POWER-LIST  | Objects with specified powers. |

By default, `search()` returns only objects the caller owns. The
SEARCH_EVERYTHING power or wizard privileges are required to search all
objects.

### stats()

```
stats([<player>])
```

Returns database statistics as a list of numbers: total objects, rooms,
exits, things, players, and garbage. With a \<player\> argument, returns
statistics for that player's objects only.

## Permission Functions

### controls()

```
controls(<player>, <object>)
```

Returns 1 if \<player\> has control over \<object\> (as defined by the
permission model in Chapter 28), and 0 otherwise.

### findable()

```
findable(<player>, <object>)
```

Returns 1 if \<player\> can locate \<object\> (the object is not UNFINDABLE
and is not in an UNFINDABLE room), and 0 otherwise.

### visible()

```
visible(<player>, <object>)
```

Returns 1 if \<object\> is visible to \<player\>, and 0 otherwise.

## Connection Information

### conn()

```
conn(<player>)
```

Returns the number of seconds \<player\> has been connected to the server.
Returns -1 if the player is not connected.

### idle()

```
idle(<player>)
```

Returns the number of seconds since \<player\> last issued a command.
Returns -1 if the player is not connected.

### doing()

```
doing(<player>)
```

Returns \<player\>'s DOING string as displayed in the WHO list.

### money()

```
money(<object>)
```

Returns the currency balance of \<object\>.

## Creation Information

### lastcreate()

```
lastcreate(<player> [, <type>])
```

Returns the dbref of the most recent object created by \<player\>. If
\<type\> is specified (`R`, `T`, `E`, or `P`), returns the most recent
object of that type.

## WHO Functions

### lwho()

```
lwho()
```

Returns a space-separated list of dbrefs of all connected players.

### mwho()

```
mwho()
```

Returns a space-separated list of dbrefs of connected players who are not
DARK. Level 2.

### nwho()

```
nwho()
```

Returns the number of connected players.

## Implementation Notes

Functions that return object information (such as `loc()`, `owner()`,
`flags()`) are subject to visibility checks. A conforming implementation
shall return appropriate error values when the caller does not have
permission to examine the target object.

The `u()` family of functions (`u()`, `ulocal()`, `udefault()`) are the
primary mechanism for modular MUSHcode programming. The distinction between
`u()` and `ulocal()` is critical: `u()` shares the caller's register
namespace, while `ulocal()` provides isolation.
