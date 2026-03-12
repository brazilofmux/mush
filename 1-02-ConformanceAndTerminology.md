# Conformance and Terminology

## Conformance

### Requirement Levels

This standard uses the following terms to indicate requirement levels, consistent
with their definitions in RFC 2119:

- **shall** -- The behavior is an absolute requirement of this standard. A
  conforming implementation must exhibit this behavior.

- **shall not** -- The behavior is absolutely prohibited by this standard. A
  conforming implementation must not exhibit this behavior.

- **should** -- There may exist valid reasons in particular circumstances to
  ignore this requirement, but the full implications must be understood and
  carefully weighed before choosing a different course.

- **should not** -- There may exist valid reasons in particular circumstances
  when the behavior is acceptable or even useful, but the full implications
  should be understood and the case carefully weighed.

- **may** -- The behavior is truly optional. A conforming implementation may
  or may not provide this behavior, but shall document its choice.

### Conformance Levels

This standard defines two conformance levels:

- **MUSH Standard Level 1** (Core) -- An implementation that supports all
  mandatory features described in this standard. Level 1 conformance is the
  minimum required to claim conformance with this standard.

- **MUSH Standard Level 2** (Extended) -- An implementation that supports all
  mandatory features and all features identified as Level 2 requirements.
  Level 2 conformance indicates a full-featured implementation suitable for
  general-purpose use.

The specific requirements for each level are enumerated in Chapter 34,
"Conformance Levels."

### Conformance Claims

An implementation claiming conformance with this standard shall:

1. State the conformance level claimed (Level 1 or Level 2).
2. Document all optional features supported.
3. Document the behavior chosen for all implementation-defined behaviors.
4. Document any extensions to the standard, clearly identifying them as
   extensions.

### Extensions

A conforming implementation may provide features beyond those specified in this
standard, provided that:

1. Extensions do not alter the behavior of any mandatory feature.
2. Extension commands and functions use names that do not conflict with names
   reserved by this standard (see Chapter 37).
3. Extensions are documented as such.

## Terminology

### Objects and the Database

- **object** -- An entity in the MUSH database, identified by a unique database
  reference number. Every object has a type, a name, an owner, and a set of
  attributes.

- **dbref** -- A database reference: a non-negative integer that uniquely
  identifies an object. Written in user-facing contexts as `#` followed by the
  integer (e.g., `#0`, `#42`, `#1234`).

- **type** -- One of the fundamental object categories: ROOM, THING, EXIT, or
  PLAYER. Every object has exactly one type, assigned at creation and immutable
  thereafter.

- **room** -- An object of type ROOM. Rooms represent locations in the virtual
  world. Rooms may contain other objects and have exits leading to other rooms.

- **thing** -- An object of type THING. Things represent portable items,
  containers, vehicles, and other tangible entities. Things may be carried by
  players, placed in rooms, or nested inside other things.

- **exit** -- An object of type EXIT. Exits represent connections between rooms.
  An exit has a source (the room it is attached to) and a destination (the room
  or object it leads to).

- **player** -- An object of type PLAYER. Players represent human users
  connected to the server. Players have all the capabilities of things, plus
  the ability to connect via the network and execute commands.

- **garbage** -- An object that has been destroyed and is awaiting reuse. Garbage
  objects are not visible to users and have no meaningful properties. Whether
  garbage objects occupy database slots is implementation-defined.

- **attribute** -- A named property of an object that holds a string value.
  Attributes store descriptions, messages, MUSHcode programs, and other data.

- **flag** -- A boolean property of an object. Flags modify an object's behavior
  or indicate status (e.g., DARK, WIZARD, STICKY).

- **power** -- A named capability that may be granted to an object, permitting
  it to perform actions that would otherwise be restricted by the permission
  model.

### Special Objects and References

- **God** -- The player object `#1`. God has unrestricted access to all server
  functions and cannot be destroyed or stripped of privilege.

- **master room** -- The room object `#0`. The master room serves as the root
  of the location hierarchy and the starting location for newly created players.
  Objects in the master room may provide global commands and exits.

- **NOTHING** -- The special value `#-1`, representing the absence of an object.
  Used for unset references (e.g., an unlinked exit, an empty contents list).

- **AMBIGUOUS** -- The special value `#-2`, returned by name-matching operations
  when multiple objects match the given name and the match cannot be resolved.

- **HOME** -- The special value `#-3`, representing the home location of an
  object. When used as an exit destination, HOME causes the traversing object
  to be moved to its home location.

### Relationships

- **location** -- The object that contains a given object. For things and
  players, the location is typically a room. For exits, the location is the
  room to which the exit is attached.

- **contents** -- The set of objects contained within a given object. The
  contents of a room include the players and things present in that room.

- **owner** -- The player who owns an object. The owner has control over the
  object's attributes and properties, subject to the permission model.

- **parent** -- An object from which another object inherits attributes and
  \$-commands. Attribute lookup traverses the parent chain when an attribute
  is not found on the object itself.

- **zone** -- A grouping mechanism that associates objects with a zone master
  object. Zones enable shared control and attribute inheritance across groups
  of related objects.

- **home** -- The default location to which a thing or player is sent when it
  has no other valid location (e.g., when its current location is destroyed).

### Command Processing

- **executor** -- The object on whose behalf a command is being executed. In
  most cases, the executor is the player who typed the command, but commands
  triggered by action lists or `@trigger` may execute on behalf of another
  object.

- **enactor** -- The player or object that originally caused the current chain
  of command execution. The enactor is preserved across `@trigger` and
  action list chains.

- **caller** -- The object that directly invoked the current function or
  command. In a chain of `u()` calls, the caller is the object that called the
  current function, while the enactor is the object that started the chain.

- **action list** -- A sequence of commands stored in an attribute, executed
  in response to an event (e.g., an object being looked at triggers the ADESC
  action list).

- **\$-command** -- A user-defined command stored in an attribute. An attribute
  whose value begins with `\$pattern:` defines a command that is triggered when
  a player types text matching the pattern.

- **^-listen** -- A user-defined listener stored in an attribute. An attribute
  whose value begins with `^pattern:` is triggered when the object hears text
  matching the pattern.

### Evaluation

- **expression** -- A string that may contain function calls, substitutions,
  and literal text. When evaluated, an expression produces a result string.

- **function** -- A named operation invoked within an expression using the
  syntax `function(arg1,arg2,...)`. Functions accept zero or more arguments
  and return a string result.

- **substitution** -- A percent-code (e.g., `%n`, `%#`, `%0`) that is replaced
  with a context-dependent value during expression evaluation.

- **register** -- A temporary named storage location for values during
  expression evaluation. Registers are designated `%q0` through `%q9` and
  `%qa` through `%qz`.

- **softcode** -- MUSHcode programs written by users and stored in object
  attributes, as distinct from the server's compiled code (hardcode).

- **hardcode** -- The compiled server code that implements the MUSH engine,
  as distinct from user-written softcode.

### Permissions and Security

- **control** -- The ability to modify an object. An object is controlled by
  its owner, by wizards, and by objects that pass the object's control lock.

- **wizard** -- An object with the WIZARD flag set. Wizards have broad
  administrative privileges as defined by the permission model.

- **royalty** -- An object with elevated privileges below wizard level, typically
  able to examine objects and bypass certain restrictions.

- **lock** -- A boolean expression evaluated against an object to determine
  whether an action is permitted. Locks are stored as attributes and may
  reference flags, attributes, and other properties of the tested object.

- **zone master** -- An object that serves as the control point for a zone.
  The zone master's locks and attributes may govern the behavior of all objects
  in its zone.

### Networking

- **connection** -- A network session between a client and the server,
  typically over TCP/IP using the Telnet protocol.

- **descriptor** -- The server's internal handle for a network connection. A
  single player may have multiple simultaneous connections (descriptors).

- **connect screen** -- The text displayed to a client before the user logs in
  as a player.

- **WHO list** -- The list of currently connected players, available via the
  WHO or DOING command.
