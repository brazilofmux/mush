# Objects and Dbrefs

## The Object Database

A MUSH server maintains a database of objects. Every entity in the virtual
world -- every room, every item, every exit, every player -- is an object in
this database. The database is the complete state of the MUSH world; there is
no game state outside the database except for transient connection information
and the command queue.

### Database References

Each object in the database is identified by a unique non-negative integer
called its **database reference** or **dbref**. The dbref is assigned when the
object is created and does not change for the lifetime of the object.

In user-facing contexts, a dbref is written as the character `#` followed by
the integer. For example, `#0` is the dbref of the first object in the
database, and `#42` is the dbref of the forty-third object created.

A conforming implementation shall support dbrefs in the range 0 to at least
2,147,483,646 (`2^31 - 2`). Implementations should use a signed 32-bit integer
for internal dbref storage.

### Special Dbref Values

The following negative dbref values have special meaning throughout this
standard:

| Value | Name       | Meaning |
|-------|------------|---------|
| `#-1` | NOTHING    | No object. Represents the absence of a valid object reference. Used for unset fields (e.g., an unlinked exit's destination, an empty contents list). |
| `#-2` | AMBIGUOUS  | Ambiguous match. Returned by name-matching operations when the given name matches more than one object and the context does not permit disambiguation. |
| `#-3` | HOME       | Home. A virtual reference representing the home location of the object being processed. When used as an exit destination, causes the traversing object to be sent to its home. |

A conforming implementation shall recognize these three special values. An
implementation may define additional negative dbref values for
implementation-specific purposes (for example, TinyMUX and RhostMUSH define
`#-4` as NOPERM, indicating a permission failure), but shall not redefine
the meaning of `#-1`, `#-2`, or `#-3`.

### Valid Object Test

An object reference is **valid** if and only if it is a non-negative integer
less than the current database size, and the object at that dbref is not of
type GARBAGE. The expression `Good_obj(x)` shall be true when `0 <= x <
db_top` and the object has not been destroyed.

Functions that accept dbref arguments shall return an appropriate error value
(typically an empty string or `#-1`) when given an invalid dbref.

## Object Properties

Every object in the database, regardless of type, shall have the following
properties:

### Identification

- **Dbref:** The object's unique database reference number.
- **Name:** A string identifying the object. Name requirements vary by
  object type (see Chapter 5, "Object Types").
- **Type:** One of ROOM, THING, EXIT, or PLAYER. The type is set at creation
  and is immutable.

### Ownership and Control

- **Owner:** The dbref of the player who owns this object. The owner has the
  right to modify the object's attributes and properties, subject to the
  permission model (see Chapter 28). For player objects, the owner is the
  player itself.

### Location and Containment

- **Location:** The dbref of the object that contains this object, or NOTHING
  if the object has no location. The meaning of location varies by type:
  - For **things** and **players:** the room, thing, or player containing
    this object.
  - For **exits:** the room to which this exit is attached.
  - For **rooms:** implementation-defined; may be used as a dropto (see
    Chapter 5).

- **Contents:** A list of objects contained within this object. Implemented
  as a linked list threaded through the contained objects' "next" pointers.

- **Exits:** A list of exit objects attached to this object. Implemented as a
  linked list threaded through the exits' "next" pointers.

- **Home:** The dbref of the location to which this object is sent when it has
  no other valid location, or when the `home` command is used. Applies to
  things and players; not meaningful for rooms or exits.

- **Link:** The dbref of the destination of an exit, or the home of a thing
  or player. The interpretation varies by type (see Chapter 5).

### Inheritance and Grouping

- **Parent:** The dbref of this object's parent object, or NOTHING if it has
  no parent. When an attribute is not found on an object, the parent chain is
  searched. The maximum depth of parent chain traversal is
  implementation-defined but shall be at least 10.

- **Zone:** The dbref of this object's zone master, or NOTHING if it is not
  zoned. Zones provide an additional axis of inheritance and control (see
  Chapter 29).

### Flags, Powers, and Attributes

- **Flags:** A set of boolean flags that modify the object's behavior. See
  Chapter 7, "Flags and Toggles."

- **Powers:** A set of capabilities granted to the object. See Chapter 8,
  "Powers."

- **Attributes:** A set of named string values. See Chapter 6, "Attributes."

### Timestamps

A conforming implementation should maintain the following timestamps for each
object:

- **Creation time:** The time at which the object was created.
- **Last modification time:** The time at which the object's attributes or
  properties were last changed.
- **Last access time:** The time at which the object was last accessed
  (examined, triggered, or used in a command).

## Object Lifecycle

### Creation

Objects are created by the following commands:

| Command    | Creates  | Description |
|------------|----------|-------------|
| `@dig`     | ROOM     | Creates a new room, optionally with exits. |
| `@create`  | THING    | Creates a new thing in the executor's inventory. |
| `@open`    | EXIT     | Creates a new exit in the current room. |
| `@pcreate` | PLAYER   | Creates a new player (wizard only). |

When an object is created:

1. The implementation shall assign it the next available dbref. An
   implementation may reuse dbrefs from previously destroyed objects.
2. The object's type shall be set and is immutable thereafter.
3. The object's owner shall be set to the creating player, unless otherwise
   specified by the creation command.
4. The object's flags, attributes, and other properties shall be initialized
   to their default values as specified for the object's type.

### Destruction

Objects are destroyed by the `@destroy` command. When an object is destroyed:

1. All objects contained within it shall be relocated. Things and players
   shall be sent to their home. If the home is also invalid, they shall be
   sent to the master room (`#0`).
2. All exits attached to the object shall be destroyed.
3. All attributes on the object shall be removed.
4. The object's type shall be changed to GARBAGE.
5. The object's dbref may be recycled for future use.

The following objects shall not be destroyed:

- Object `#0` (the master room).
- Object `#1` (God).
- Objects with the SAFE flag set, unless the `/override` switch is used.
- Players who are currently connected, unless forced by a wizard.

### Recycling

When a destroyed object's dbref is reused for a new object, the new object
shall have no properties from the destroyed object. All flags, attributes,
and relationships from the previous occupant of the dbref shall be cleared
before the dbref is reassigned.

**Implementation Note:** Some implementations maintain a free list of destroyed
dbrefs for recycling, while others grow the database monotonically and compact
it during maintenance. Both approaches are conforming.

## The Contents List and Exit List

Objects that may contain other objects (rooms, things, players) maintain a
**contents list**. Objects that may have exits attached (rooms, things, players)
maintain an **exits list**. These lists are implemented as singly linked lists:

- The containing object stores the dbref of the first object in the list
  (the **head**).
- Each object in the list stores the dbref of the next object in the list
  via its **next** pointer.
- The end of the list is indicated by NOTHING.

For example, if room `#10` contains three things (`#42`, `#99`, `#7`):

```
Room #10:
  contents = #42
    #42.next = #99
      #99.next = #7
        #7.next = #-1 (NOTHING)
```

The order of objects in the contents list is implementation-defined. An
implementation may order by creation time, insertion time, alphabetically,
or by any other criterion.

**Implementation Note:** The linked-list structure means that counting the
contents of an object requires traversing the entire list. Implementations
that need frequent count operations may wish to cache the count.

## Special Objects

### Object #0: The Master Room

The first object in the database (`#0`) shall be a room. By convention, it
serves as the **master room** -- the container for global commands and exits
that are accessible from any location. When command matching fails to find a
match in the player's current location, the master room is searched as a
fallback (see Chapter 9).

The master room, the player starting room, and the default home location
are distinct concepts that may be configured independently. TinyMUX provides
`master_room`, `player_starting_room`, and `default_home` as separate
configuration parameters. PennMUSH has `player_start` and
`master_room` as separate options. While `#0` commonly serves all three
roles, a conforming implementation should allow each to be configured
independently.

Object `#0` shall not be destroyed. An attempt to destroy `#0` shall fail
with an error message.

### Object #1: God

Object `#1` shall be a player. This player, conventionally called "God" or
the "number one player," has unrestricted administrative access:

1. God passes all permission checks.
2. God can set and clear any flag on any object, including flags that are
   otherwise restricted.
3. God can read and modify any attribute on any object, including attributes
   with the GOD attribute flag.
4. God cannot be destroyed, killed, or stripped of the WIZARD flag.
5. God is the only object that can set the WIZARD flag on other players, unless
   the implementation provides alternative mechanisms.

**Compatibility Note:** All four major implementations agree on `#1` as the
God object. Some implementations allow configuring which dbref is God, but
`#1` is the universal default and the only value specified by this standard.
