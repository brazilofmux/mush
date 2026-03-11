# Building Commands

## Overview

Building commands create and configure the objects that make up the virtual
world. These commands are used by builders to construct rooms, create exits,
define objects, and set their properties.

## Object Creation

### @dig

```
@dig [/teleport] <room-name> [= <exit-to>[;<aliases>] [, <exit-back>[;<aliases>]]]
```

The `@dig` command creates a new room. The room is created with the executor
as its owner.

If exit names are provided after the `=`, the first exit is created from the
current room to the new room, and the optional second exit is created from the
new room back to the current room.

The `/teleport` switch teleports the executor to the newly created room
after creation.

Example:

```
> @dig The Library = North;north;n, South;south;s
The Library created as room #100.
Exit "North" created as exit #101.
Exit "South" created as exit #102.
Linked exit #101 to The Library(#100).
Linked exit #102 to Town Square(#5).
```

### @create

```
@create <thing-name> [= <cost>]
```

The `@create` command creates a new thing in the executor's inventory. The
optional cost sets the recycling value of the object.

Example:

```
> @create Magic Sword = 10
Magic Sword created as object #103.
```

### @open

```
@open <exit-name>[;<aliases>] [= <destination>]
```

The `@open` command creates a new exit in the executor's current room. If
a destination is specified, the exit is linked to that destination. Otherwise,
the exit is created unlinked.

Example:

```
> @open West;west;w = #42
Exit "West" created as exit #104.
Linked exit #104 to The Garden(#42).
```

### @clone

```
@clone [/preserve] <object> [= <cost>]
```

The `@clone` command creates a duplicate of an existing object. The clone
receives copies of all attributes on the original (except those with
AF_NOCLONE set). The clone's ACLONE attribute is triggered after creation.

The `/preserve` switch preserves the original object's ownership on the
clone. Without it, the clone is owned by the executor.

## Object Properties

### @name

```
@name <object> = <new-name>
```

The `@name` command changes an object's name. For players, `@name` also
requires the current password:

```
@name me = NewName <password>
```

Player names must satisfy the naming rules in Chapter 5. Exit names may
include aliases separated by semicolons.

### @desc

```
@desc <object> = <description>
```

The `@desc` command sets the object's DESC attribute. This is equivalent to
`&DESC <object> = <description>` but is the conventional form.

### @set

```
@set [/quiet] <object> = <flag>
@set [/quiet] <object> = !<flag>
@set [/quiet] <object>/<attribute> = <value>
@set [/quiet] <object>/<attribute> = <attribute-flag>
```

The `@set` command is the general-purpose command for modifying object
properties. It can:

1. Set or clear flags on an object.
2. Set the value of an attribute.
3. Set or clear attribute flags on an attribute.

The `/quiet` switch suppresses the confirmation message.

### @lock

```
@lock [/<lock-type>] <object> = <key-expression>
```

The `@lock` command sets a lock on an object. Without a lock type, the
default lock is set. The lock expression syntax is specified in Chapter 27.

Common lock types:

| Switch      | Lock Type | Controls |
|-------------|-----------|----------|
| (default)   | Default   | Passing/failing the object. |
| `/enter`    | Enter     | Entering the object. |
| `/leave`    | Leave     | Leaving the object. |
| `/use`      | Use       | Using the object. |
| `/page`     | Page      | Paging the player. |
| `/teleport` | Teleport  | Teleporting to the location. |
| `/give`     | Give      | Giving the object to others. |
| `/receive`  | Receive   | Receiving objects from others. |
| `/drop`     | Drop      | Dropping the object. |
| `/speech`   | Speech    | Speaking in the location. |
| `/link`     | Link      | Linking exits to the location. |
| `/parent`   | Parent    | Parenting other objects to this one. |
| `/control`  | Control   | Controlling this object. |

### @unlock

```
@unlock [/<lock-type>] <object>
```

The `@unlock` command removes a lock from an object. Without a lock type,
the default lock is removed.

## Linking and Inheritance

### @link

```
@link <object> = <destination>
@link <object> = home
```

The `@link` command sets the destination of an exit or the home location of
a thing or player. For exits, the destination must be a room (with LINK_OK
set, or owned by the executor) or HOME. For things and players, the
destination sets their home.

### @unlink

```
@unlink <exit>
```

The `@unlink` command removes the destination from an exit, leaving it
unlinked.

### @parent

```
@parent <object> = <parent>
@parent <object> =
```

The `@parent` command sets or clears the parent of an object. The parent
object must have the PARENT_OK flag set, or be owned by the executor, or the
executor must be a wizard.

When a parent is set, the object inherits attributes, $-commands, and
^-listeners from the parent (see Chapter 6, "Attributes," Attribute
Inheritance).

Setting the parent to nothing (empty right side) clears the parent.

### @zone

```
@zone <object> = <zone-master>
@zone <object> =
```

The `@zone` command assigns an object to a zone (see Chapter 29). The zone
master must have the ZONE_MASTER flag set. Setting the zone to nothing clears
the zone assignment.

## Attribute Commands

### & (set attribute)

```
&<attribute> <object> = <value>
&<attribute> <object> =
```

The `&` prefix sets a user-defined attribute on an object. Setting the value
to empty clears the attribute. This is the most common way to set attributes.

### @wipe

```
@wipe <object>[/<pattern>]
```

The `@wipe` command removes attributes from an object. Without a pattern,
all user-settable attributes are removed. With a pattern (using wildcards),
only matching attributes are removed.

Example:

```
> @wipe #42/CMD_*
```

Removes all attributes beginning with `CMD_` from object `#42`.

### @edit

```
@edit <object>/<attribute> = <search>, <replace>
```

The `@edit` command performs a search-and-replace on the value of an
attribute. This is useful for making small changes to long attribute values
without retyping the entire value.

Example:

```
> @edit me/DESC = tall, short
```

Changes "tall" to "short" in the player's description.

## Message Attributes

The following `@`-commands are shortcuts for setting the corresponding
message attributes:

| Command   | Sets Attribute | Description |
|-----------|---------------|-------------|
| `@desc`   | DESC          | Description |
| `@succ`   | SUCC          | Success message |
| `@osucc`  | OSUCC         | Others' success message |
| `@asucc`  | ASUCC         | Success action list |
| `@fail`   | FAIL          | Failure message |
| `@ofail`  | OFAIL         | Others' failure message |
| `@afail`  | AFAIL         | Failure action list |
| `@drop`   | DROP          | Drop message |
| `@odrop`  | ODROP         | Others' drop message |
| `@adrop`  | ADROP         | Drop action list |
| `@enter`  | ENTER         | Enter message |
| `@oenter` | OENTER        | Others' enter message |
| `@aenter` | AENTER        | Enter action list |
| `@leave`  | LEAVE         | Leave message |
| `@oleave` | OLEAVE        | Others' leave message |
| `@aleave` | ALEAVE        | Leave action list |
| `@idesc`  | IDESC         | Interior description |
| `@sex`    | SEX           | Gender for pronoun substitution |
| `@listen` | LISTEN        | Listen pattern |
| `@away`   | AWAY          | Away message |
| `@idle`   | IDLE          | Idle message |
| `@reject` | REJECT        | Page rejection message |

Each of these commands is equivalent to using `&ATTR <object> = <value>` but
is provided as a convenience and for backward compatibility.
