# Attributes

## Overview

An attribute is a named property of an object that holds a string value.
Attributes are the primary mechanism for storing data on objects: descriptions,
messages, MUSHcode programs, lock expressions, and arbitrary user data are all
stored as attributes.

Every object may have any number of attributes. Attributes are divided into
two categories:

1. **Standard attributes** -- Predefined by the server with specific names,
   meanings, and default permissions. Standard attributes have reserved names
   and often trigger specific server behaviors.

2. **User-defined attributes** -- Created by users to store arbitrary data.
   User-defined attributes have no inherent server behavior but may contain
   \$-commands, ^-listen patterns, or data accessed by softcode.

## Attribute Names

### Naming Rules

Attribute names are case-insensitive. A conforming implementation shall store
and compare attribute names without regard to case, though it may preserve the
case of the name as originally set.

A valid attribute name shall satisfy the following rules:

1. The name shall be at least one character long.
2. The name shall begin with a letter (A-Z, a-z) or underscore (`_`).
3. The name may contain letters, digits, and the following special characters:
   `_`, `-`, `.`, `'`, `` ` ``.
4. The name shall not exceed the implementation's maximum attribute name length.
   A conforming implementation shall support attribute names of at least 31
   characters.

**Compatibility Note:** PennMUSH supports attribute names up to 1024 characters.
TinyMUSH and TinyMUX limit names to 31 characters. This standard requires
support for at least 31 characters; implementations may support longer names.

### Reserved Prefixes

The following attribute name patterns are reserved:

- Names beginning with `_` are reserved for implementation-specific internal
  attributes.
- The names `VA` through `VZ` are reserved as user-accessible shortcut
  attributes (see "Shortcut Attributes" below).

## Attribute Values

An attribute value is a string. A conforming implementation shall support
attribute values of at least 4,000 characters. Implementations should support
values of at least 8,000 characters.

Attribute values may contain any printable character. Whether control
characters (other than tab) are permitted in attribute values is
implementation-defined.

An attribute with an empty string value is distinct from the absence of the
attribute. Setting an attribute to an empty string clears the attribute.

## Setting and Retrieving Attributes

### Setting Attributes

Attributes are set using the `@set` command or the `&` shortcut:

```
> @set <object>/<attribute> = <value>
> &<attribute> <object> = <value>
```

Examples:

```
> @set me/DESC = A tall figure in a dark cloak.
Set.
> &MY_DATA #42 = some stored value
Set.
```

Setting an attribute to an empty value clears it:

```
> &MY_DATA #42 =
Cleared.
```

### Retrieving Attributes

Attributes are retrieved through several mechanisms:

- The `get()` function returns the value of an attribute:
  `get(#42/DESC)` returns the description of object `#42`.

- The `v()` function returns the value of an attribute on the executing object:
  `v(DESC)` returns the executing object's description.

- The `xget()` function is equivalent to `get()` in most implementations.

- The `@examine` command displays all visible attributes on an object.

### Attribute Permissions

Whether a player can read or modify an attribute depends on:

1. The object's ownership and the player's privilege level.
2. The attribute flags set on the attribute.
3. The attribute's lock, if any.

See "Attribute Flags" below for details.

## Standard Attributes

A conforming implementation shall support the following standard attributes.
These are organized by function.

### Message Attributes

Message attributes define text displayed to players when events occur. They
follow a systematic naming convention with three variants for each event:

- **\<EVENT\>** -- Message shown to the player who triggered the event.
- **O\<EVENT\>** -- Message shown to other players in the same room.
- **A\<EVENT\>** -- Action list executed when the event occurs.

The following table lists all standard message attribute groups:

| Event     | Invoker   | Others    | Action    | Trigger |
|-----------|-----------|-----------|-----------|---------|
| Success   | SUCC      | OSUCC     | ASUCC     | Passing the default lock |
| Failure   | FAIL      | OFAIL     | AFAIL     | Failing the default lock |
| Drop      | DROP      | ODROP     | ADROP     | Dropping an object or arriving via exit |
| Enter     | --        | OENTER    | AENTER    | Entering a room or container |
| Leave     | --        | OLEAVE    | ALEAVE    | Leaving a room or container |
| Move      | MOVE      | OMOVE     | AMOVE     | Moving through an exit |
| Use       | USE       | OUSE      | AUSE      | Using an object |
| Pay       | PAY       | OPAY      | APAY      | Paying an object's cost |
| Kill      | KILL      | OKILL     | --        | Killing a player |
| Teleport  | TPORT     | OTPORT    | ATPORT    | Teleporting (source room) |
| Teleport  | --        | OXTPORT   | --        | Teleporting (destination room) |
| Describe  | --        | --        | ADESC     | Looking at the object |

### Failure Message Attributes

Additional failure messages cover specific lock types:

| Lock      | Invoker   | Others    | Action    | Trigger |
|-----------|-----------|-----------|-----------|---------|
| Enter     | EFAIL     | OEFAIL    | AEFAIL    | Failing the enter lock |
| Leave     | LFAIL     | OLFAIL    | ALFAIL    | Failing the leave lock |
| Use       | UFAIL     | OUFAIL    | AUFAIL    | Failing the use lock |
| Give      | GFAIL     | OGFAIL    | AGFAIL    | Failing the give lock |
| Receive   | RFAIL     | ORFAIL    | ARFAIL    | Failing the receive lock |
| Drop      | DFAIL     | ODFAIL    | ADFAIL    | Failing the drop lock |
| Teleport  | TFAIL     | OTFAIL    | ATFAIL    | Failing the teleport lock |
| Tel-From  | TOFAIL    | OTOFAIL   | ATOFAIL   | Failing the teleport-out lock |

### Descriptive Attributes

| Attribute | Description |
|-----------|-------------|
| DESC      | The object's description, shown by `look`. Default flags: AF_VISUAL. |
| IDESC     | Interior description, shown to players inside the object. |
| SEX       | Grammatical gender for pronoun substitution. Default flags: AF_VISUAL. |
| ALIAS     | Alternative names for the object. Default flags: AF_VISUAL. |
| NAME      | The object's display name (internal use). |

### Listening Attributes

| Attribute    | Description |
|--------------|-------------|
| LISTEN       | A pattern string. When the object hears text matching this pattern, the AHEAR/AMHEAR/AAHEAR action lists are triggered. |
| AHEAR        | Action list executed when a non-self message matches LISTEN. |
| AMHEAR       | Action list executed when a self-generated message matches LISTEN. |
| AAHEAR       | Action list executed when any message matches LISTEN. |
| FORWARDLIST  | Space-separated list of dbrefs to which audible messages are forwarded. Default flags: AF_PRIVATE. |
| FILTER       | A pattern. Only messages matching this pattern are forwarded. |
| INFILTER     | A pattern. Only incoming messages matching this pattern are relayed. |
| PREFIX       | Text prepended to forwarded messages. |
| INPREFIX     | Text prepended to incoming relayed messages. |

### Connection Attributes

| Attribute    | Description |
|--------------|-------------|
| ACONNECT     | Action list executed when the object's owner connects. |
| ADISCONNECT  | Action list executed when the object's owner disconnects. |
| STARTUP      | Action list executed when the server starts or restarts. |

**Implementation Note:** ACONNECT and ADISCONNECT on rooms are triggered when
any player connects or disconnects while in that room. ACONNECT and ADISCONNECT
on the master room (`#0`) are triggered for all player connections and
disconnections.

### Economy Attributes

| Attribute  | Description |
|------------|-------------|
| COST       | Number of coins required to use this object. |
| CHARGES    | Number of uses remaining before the object stops working. |
| RUNOUT     | Action list executed when CHARGES reaches zero. |
| ALLOWANCE  | Daily coin allowance for players. |

### Enter/Leave Aliases

| Attribute  | Description |
|------------|-------------|
| EALIAS     | Semicolon-separated aliases for the `enter` command on this object. |
| LALIAS     | Semicolon-separated aliases for the `leave` command from inside this object. |
| OXENTER    | Message shown to others in the destination when entering. |
| OXLEAVE    | Message shown to others in the destination when leaving. |

### Queue and Semaphore Attributes

| Attribute  | Description |
|------------|-------------|
| SEMAPHORE  | Semaphore counter for `@wait`/`@notify`. Default flags: AF_LOCK, AF_NOCLONE. |
| QUEUEMAX   | Maximum number of queue entries for this object. |

### Player Attributes

| Attribute  | Description |
|------------|-------------|
| LAST       | Timestamp of the most recent connection. Default flags: AF_WIZARD, AF_NOCLONE. |
| LASTSITE   | Hostname of the most recent connection. |
| AWAY       | Message returned to pages when the player is away. |
| IDLE       | Message returned to pages when the player is idle. |
| REJECT     | Message returned when a page is rejected. |
| LOGINDATA  | Server-maintained login history. |
| TIMEOUT    | Per-player idle timeout in seconds. |

### Password Attribute

The **PASSWORD** attribute stores the player's authentication credential.
This attribute shall not be readable through normal attribute access by any
player, including God. Its storage format (plaintext, hashed, or encrypted)
is implementation-defined, but a conforming implementation should store
passwords in a hashed or encrypted form.

### Format Attributes (Level 2)

Format attributes allow objects to customize the display of standard output:

| Attribute    | Description |
|--------------|-------------|
| CONFORMAT    | Custom format for the contents list display. |
| EXITFORMAT   | Custom format for the exits list display. |
| NAMEFORMAT   | Custom format for the object's name display. |
| DESCFORMAT   | Custom format for the description display. |

When a format attribute is set, the server evaluates it as MUSHcode and uses
the result in place of the default display format.

### Lock Attributes

Lock expressions are stored as attributes. The following lock attributes are
standard:

| Attribute  | Lock Type | Controls |
|------------|-----------|----------|
| LOCK       | Default   | Passing/failing the object |
| LENTER     | Enter     | Entering the object |
| LLEAVE     | Leave     | Leaving the object |
| LPAGE      | Page      | Paging the player |
| LUSE       | Use       | Using the object |
| LGIVE      | Give      | Giving the object away |
| LRECEIVE   | Receive   | Receiving objects |
| LDROP      | Drop      | Dropping the object |
| LTPORT     | Teleport  | Teleporting to the object |
| LTELOUT    | Teleport-out | Teleporting from the location |
| LLINK      | Link      | Linking exits to the object |
| LPARENT    | Parent    | Parenting to the object |
| LCONTROL   | Control   | Controlling the object |
| LSPEECH    | Speech    | Speaking in the location |
| LOPEN      | Open      | Opening exits from the location |

See Chapter 27, "Locks," for the lock expression syntax.

### Comment Attribute

The **COMMENT** attribute is a wizard-only annotation field. Default flags:
AF_WIZARD, AF_MDARK. It is not visible to non-wizard players and is intended
for administrative notes.

### Shortcut Attributes (VA through VZ)

The attributes **VA** through **VZ** (26 attributes) are predefined,
general-purpose storage slots with no default flags. They provide convenient
short names for commonly needed per-object data storage.

These attributes are accessed like any other attribute:

```
> &VA me = Hello
> think v(VA)
Hello
```

They may also be accessed through percent substitution:

```
> think %va
Hello
```

## Attribute Flags

Attribute flags control the visibility and modifiability of individual
attributes. They are distinct from object flags (Chapter 7).

### Standard Attribute Flags

A conforming implementation shall support the following attribute flags:

| Flag        | Description |
|-------------|-------------|
| AF_VISUAL   | Anyone can see this attribute, regardless of object ownership. |
| AF_DARK     | Only the server (or God) can see this attribute. |
| AF_MDARK    | Only wizards can see this attribute (mortal-dark). |
| AF_ODARK    | Only the owner can see this attribute. |
| AF_WIZARD   | Only wizards can modify this attribute. |
| AF_GOD      | Only God (`#1`) can modify this attribute. |
| AF_LOCK   | Only the attribute's creator can modify it. |
| AF_NOPROG   | This attribute is not searched for \$-commands. |
| AF_PRIVATE  | This attribute is not inherited by child objects. |
| AF_NOCLONE  | This attribute is not copied by `@clone`. |
| AF_NOPARSE  | \$-command patterns in this attribute are not evaluated. |
| AF_REGEXP   | \$-command and ^-listen patterns use regular expressions instead of wildcards. |
| AF_CASE     | Regular expression matching is case-sensitive (used with AF_REGEXP). |
| AF_SAFE     | This attribute cannot be modified (server-enforced). |
| AF_IS_LOCK  | This attribute contains a lock expression. |
| AF_CONST    | Server-set attribute that no user can modify. |
| AF_INTERNAL | Internal server attribute; not visible to any user. |

### Setting Attribute Flags

Attribute flags are set using the `@set` command with the attribute flag
name:

```
> @set <object>/<attribute> = <flag>
> @set <object>/<attribute> = !<flag>
```

Examples:

```
> @set me/SECRET_DATA = DARK
> @set me/PUBLIC_INFO = VISUAL
> @set me/FROZEN_VALUE = SAFE
```

The `!` prefix removes a flag:

```
> @set me/SECRET_DATA = !DARK
```

### Default Attribute Flags

Standard attributes have default flags assigned by the server. For example,
DESC defaults to AF_VISUAL (anyone can read descriptions), while LAST defaults
to AF_WIZARD and AF_NOCLONE (only wizards can see login times, and they are
not copied by `@clone`).

User-defined attributes are created with no flags by default.

## User-Defined Attributes

### Creation

User-defined attributes are created implicitly when a value is first set on
them using `@set` or `&`:

```
> &MY_CUSTOM_ATTR me = some value
```

This creates the attribute `MY_CUSTOM_ATTR` on the object if it does not
already exist.

A conforming implementation shall also support explicit attribute creation
via the `@attribute` command, which allows setting default flags for the
attribute name globally:

```
> @attribute/access MY_GLOBAL_ATTR = wizard visual
```

### Attribute Ownership

Each attribute on an object has an implicit creator. The creator is the player
who first set the attribute. When an attribute has the AF_LOCK flag set,
only the creator (or a wizard) can modify it.

## Attribute Inheritance

When a function retrieves an attribute from an object and the attribute is not
set on that object, the server searches the object's parent chain:

1. Check the object itself.
2. Check the object's parent.
3. Check the parent's parent.
4. Continue up the chain until the attribute is found or the chain ends.

The maximum depth of this search is implementation-defined but shall be at
least 10 levels.

Attributes with the AF_PRIVATE flag are not inherited -- the search stops at
the object on which AF_PRIVATE is set.

The `get()`, `v()`, and `u()` functions all retrieve attributes with
inheritance -- they walk the parent chain as described above. All four
reference implementations use parent-aware retrieval in `get()` (e.g.,
TinyMUX calls `atr_pget`, PennMUSH calls `atr_get_with_parent`).

**Compatibility Note:** Some implementations provide functions that explicitly
bypass inheritance (e.g., `xget()` in some configurations) or retrieve with
a fallback (e.g., `default()`), but `get()` itself is inheritance-aware in
all four reference implementations.

## Attribute Actions

Attributes participate in two action mechanisms:

### \$-Commands

An attribute whose value begins with `$<pattern>:` defines a user command.
When a player types text matching \<pattern\>, the action list following the
colon is executed:

```
> &CMD_GREET me = $greet *:@pemit %#=You greet %0 warmly.
```

When the player types `greet Bob`, the action list is executed with `%0` bound
to `Bob`.

By default, patterns use wildcard matching (`*` matches any string). If the
AF_REGEXP flag is set on the attribute, patterns use regular expression
matching.

### ^-Listeners

An attribute whose value begins with `^<pattern>:` defines a listener. When
the object hears text matching \<pattern\>, the action list is executed:

```
> &HEAR_HELLO me = ^*hello*:@pemit %#=I heard you say hello!
```

^-listeners require the MONITOR flag to be set on the object.

## Examining Attributes

The `@examine` command displays an object's attributes:

```
> examine me
Player Name(#42PW)
Type: PLAYER  Flags: PLAYER
...
DESC [#42]: A tall figure in a dark cloak.
MY_DATA [#42]: some stored value
```

The display format for attributes typically includes the attribute name, the
dbref of the object on which it is set (important for inherited attributes),
and the value.

Attribute flags are shown on the attribute line when using detailed examine
modes (implementation-defined format).
