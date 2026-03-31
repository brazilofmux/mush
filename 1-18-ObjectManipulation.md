# Object Manipulation

## Overview

Object manipulation commands allow players to interact with things in the
virtual world: picking up items, dropping them, giving them to other players,
examining their properties, and destroying them when no longer needed.

## Carrying and Moving Objects

### get / take

```
get [/quiet] <object>
take [/quiet] <object>
```

The `get` command picks up a thing from the current room and places it in the
player's inventory. The `take` command is a synonym.

The object's default lock is evaluated. If it fails, the FAIL, OFAIL, and
AFAIL attributes are triggered, and the object is not picked up. On success,
the SUCC, OSUCC, and ASUCC attributes are triggered, and the object is moved
to the player's inventory.

The object must be a thing (not a room, exit, or player). The player must be
in the same room as the object.

### drop

```
drop [/quiet] <object>
```

The `drop` command removes a thing from the player's inventory and places it
in the current room.

The object's drop lock (LDROP) is evaluated. If it fails, the DFAIL, ODFAIL,
and ADFAIL attributes are triggered. On success, the DROP, ODROP, and ADROP
attributes are triggered.

If the object has the STICKY flag set, the object is sent to its HOME
location regardless of the room's dropto setting. If the room has a dropto
set and neither the object nor the room is STICKY, the object is sent to
the dropto location instead of remaining in the room. See Chapter 5,
"Object Types," for the complete dropto behavior rules.

### give

```
give [/quiet] <recipient> = <object>
give [/quiet] <recipient> = <amount>
```

The `give` command transfers a thing or currency to another player. The
recipient must be in the same room as the giver.

When giving an object, the giver's give lock (LGIVE) on the object is
checked, and the recipient's receive lock (LRECEIVE) is checked. If either
fails, the give is denied and the appropriate failure messages are triggered.

When giving currency, the specified amount is transferred from the giver's
balance to the recipient's balance. The giver must have sufficient funds.

## Object Information

### examine

```
examine [/<switch>] <object>[/<attribute>]
```

The `examine` command displays detailed information about an object,
including:

1. The object's name, dbref, type, and flags.
2. The object's owner, location, home, and zone.
3. The object's parent (if set).
4. All visible attributes and their values.
5. The object's contents and exits (if any).

If an attribute name is specified after `/`, only that attribute is displayed.

### Switches

| Switch     | Description | Level |
|------------|-------------|-------|
| `/brief`   | Show only the object header, not attributes. | 1 |
| `/full`    | Show all attributes, including internal flags. | 2 |
| `/parent`  | Show inherited attributes from the parent chain. | 2 |
| `/owner`   | Show the owner of each attribute. TinyMUSH only. | 2 |
| `/debug`   | Show debug information. TinyMUX only. | 2 |

### Permissions

A player may examine objects they own. Wizards may examine any object.
Objects with the VISUAL flag set may be examined by anyone. Objects with the
OPAQUE flag suppress some information for non-owners.

### @decompile

```
@decompile [/<switch>] <object>[/<attribute>]
```

The `@decompile` command produces output that, when typed, would recreate the
object's attributes and flags. This is useful for backing up objects or
transferring them between servers.

Example output:

```
@create Magic Sword
@desc Magic Sword = A gleaming blade of finest steel.
&CMD_SWING Magic Sword = $swing *:@pemit %#=You swing at %0!
@set Magic Sword = STICKY
```

## Finding Objects

### @find

```
@find <name>
```

The `@find` command lists all objects owned by the player whose name matches
the given string. The match uses substring matching (not prefix matching).

### @search

```
@search [<player>] [<class>=<restriction>]
```

The `@search` command provides a powerful search facility for finding objects
in the database. Common search classes:

| Class     | Restriction | Description |
|-----------|-------------|-------------|
| `type`    | ROOM, THING, EXIT, PLAYER | Objects of the specified type. |
| `name`    | \<pattern\> | Objects with matching names. |
| `flags`   | \<flag-list\> | Objects with specified flags set. |
| `parent`  | \<dbref\>   | Objects with the specified parent. |
| `zone`    | \<dbref\>   | Objects in the specified zone. |
| `owner`   | \<player\>  | Objects owned by the specified player. |
| `powers`  | \<power-list\> | Objects with specified powers. |

By default, `@search` only shows objects the player owns. Wizards and objects
with the SEARCH_EVERYTHING power can search all objects.

### @entrances

```
@entrances [<object>]
```

The `@entrances` command lists all exits that lead to the specified object
(or the current room if no object is specified), all objects whose home is
the specified location, and all objects linked to it.

## Object Ownership

### @chown

```
@chown [/preserve] <object> = <player>
@chown [/preserve] <object>/<attribute> = <player>
```

The `@chown` command transfers ownership of an object (or a specific
attribute) to another player. This command typically requires wizard
privileges, unless the object has the CHOWN_OK flag set and the player
receiving ownership is the executor.

The `/preserve` switch retains the original owner's attributes and settings
that would otherwise be reset on ownership change.

## Object Destruction

### @destroy

```
@destroy [/override] <object>
```

The `@destroy` command destroys an object, removing it from the database.
The destruction process is described in Chapter 4, "Objects and Dbrefs."

Objects with the SAFE flag require the `/override` switch to destroy. Objects
`#0` and `#1` cannot be destroyed under any circumstances.

Some implementations delay destruction by one database cycle, setting the
GOING flag and allowing the destruction to be canceled by clearing the flag.

### Canceling Destruction

If the implementation uses delayed destruction, the pending destruction of
an object with the GOING flag may be canceled. PennMUSH provides an
`@undestroy` command for this purpose. TinyMUX, TinyMUSH, and RhostMUSH
cancel pending destruction by clearing the GOING flag with
`@set <object> = !GOING`. Level 2.

## Object Movement

### @teleport

See Chapter 15 for the full specification of `@teleport`. In the context of
object manipulation, `@teleport` is used to move objects to arbitrary
locations:

```
> @teleport #42 = #100
```

Moves object `#42` to room `#100`.

## Miscellaneous

### kill

```
kill <player> = <cost>
```

The `kill` command attempts to kill a player. The cost determines the
probability of success. If successful, the victim is sent to their home
location. If the room has the HAVEN flag set, the `kill` command is disabled.

Whether the `kill` command is enabled at all is a server configuration option.
Many MUSHes disable it entirely.

### @verb

```
@verb <object> = <actor>, <succ-attr>, <osucc-attr>, <asucc-attr>,
      <fail-attr>, <ofail-attr>, <afail-attr>[, <lock-attr>]
```

The `@verb` command triggers the did_it pipeline on an object using arbitrary
attribute names. The arguments are the names of the attributes to use for
the success message, others-success message, action-on-success, failure
message, others-failure message, action-on-failure, and optionally a lock
attribute. The `<actor>` argument specifies who is considered the actor for
the purpose of lock evaluation and message display. Level 2.
