# Command Parsing and Dispatch

## Overview

When a connected player types a line of text at the MUSH prompt, the server
must determine what command the player intended, resolve any object references,
and execute the appropriate action. This chapter specifies the complete
pipeline from raw input to command execution.

## Input Processing

### Line Input

A conforming implementation shall accept input as lines of text terminated by
a newline character. Each line constitutes a single command input.

Leading and trailing whitespace shall be stripped from the input line before
processing. Empty lines (after stripping) shall be silently discarded.

### Command Separators

A single input line may contain multiple commands separated by semicolons
(`;`). The server shall split the line on unescaped, unbraced semicolons and
process each resulting command independently, in left-to-right order:

```
> say Hello; say World
You say, "Hello"
You say, "World"
```

Semicolons inside braces (`{}`), square brackets (`[]`), or preceded by a
backslash (`\`) are not treated as command separators:

```
> think {one;two}
one;two
> think before\;after
before;after
```

### Output Separators

When a single input line produces multiple commands, the output from each
command is delivered in order. There is no guaranteed separator between the
output of successive commands in a single input line.

## The Command Matching Pipeline

When the server processes a command, it attempts to match the input against
several categories of commands in a defined priority order. The first
successful match determines the command that is executed.

A conforming implementation shall use the following matching order:

### Step 1: Prefix Commands

Single-character prefix commands are checked first. These are:

| Prefix | Command    | Meaning |
|--------|------------|---------|
| `"`    | `say`      | `"text` is equivalent to `say text` |
| `:`    | `pose`     | `:text` is equivalent to `pose text` |
| `;`    | `semipose` | `;text` is equivalent to `pose's text` (no space after name) |
| `\`    | `@emit`    | (Implementation-defined; some implementations use `\\`) |
| `#`    | `@force`   | `#<dbref> command` forces the object (wizard only) |
| `&`    | `@set`     | `&attr object=value` sets an attribute |

If the first character of the input matches a prefix command, the remainder
of the input is passed as the argument to the corresponding command. No
further matching is performed.

### Step 2: Built-in Commands

The server checks whether the input matches a built-in command. Built-in
commands include both `@`-commands (e.g., `@dig`, `@set`, `@teleport`) and
short-form commands (e.g., `look`, `go`, `get`, `drop`, `say`, `pose`,
`page`, `whisper`, `kill`, `give`, `WHO`, `QUIT`).

Built-in command matching shall be case-insensitive.

A conforming implementation should support prefix matching on built-in
commands: if the input matches the beginning of exactly one built-in command
name, that command is selected. If the input matches the beginning of multiple
built-in commands, the behavior is implementation-defined (the implementation
may select the shortest match, return an error, or apply other disambiguation
rules).

#### Command Switches

Built-in commands may accept switches, specified as `/<switch-name>` following
the command name:

```
> @set/quiet me = DARK
> @destroy/override #42
```

Multiple switches may be specified:

```
> @pemit/list/silent #42 #43 #44 = Hello
```

Switches modify the behavior of the command as defined by each command's
specification. Unknown switches shall produce an error message.

#### Command Arguments

After the command name and any switches, the remainder of the input is the
command's argument string. Most commands parse their arguments around the `=`
character:

- **Left side:** The target of the command (often an object reference).
- **Right side:** The value or action (e.g., an attribute value, a destination).

Whitespace around the `=` is stripped:

```
> @desc   me   =   A tall figure.
```

is equivalent to:

```
> @desc me=A tall figure.
```

### Step 3: Exit Matching

If the input does not match a built-in command, the server checks whether it
matches the name or alias of an exit in the player's current room.

Exit matching considers:

1. All exits in the current room's exit list.
2. All exits in the player's parent room chain (if parent rooms have exits).
3. All exits in the master room (`#0`), if the exit is not found locally.

Exit names are semicolon-delimited alias lists (e.g., `North;north;n`). The
input is compared against each alias using the name matching rules described
in Chapter 10.

If exactly one exit matches, the player attempts to traverse it (see
Chapter 5, "Object Types," for exit traversal behavior). If multiple exits
match, the behavior is implementation-defined; implementations should select
one randomly.

### Step 4: Enter and Leave Aliases

If the input does not match an exit, the server checks whether it matches an
enter alias (EALIAS attribute) on any object in the room, or a leave alias
(LALIAS attribute) on the player's current location (if the player is inside
an object).

If a match is found, the corresponding `enter` or `leave` action is performed.

### Step 5: $-Commands

If no match has been found, the server searches for $-commands that match the
input. $-commands are user-defined commands stored in object attributes (see
Chapter 6, "Attributes"). An attribute whose value begins with `$pattern:`
defines a $-command that triggers when user input matches the pattern.

The search order for $-commands is:

1. **The player itself:** Attributes on the player object.
2. **The player's inventory:** Attributes on objects carried by the player.
3. **The current room:** Attributes on the room the player occupies.
4. **Objects in the current room:** Attributes on things present in the room.
5. **Zone master:** If the player or room is zoned, attributes on objects in
   the zone master's contents (if ZONE_CONTENTS is set on the zone master),
   then attributes on the zone master itself.
6. **The master room (`#0`):** Attributes on objects in the master room,
   providing global commands.

Within each location, objects are searched in contents-list order.
Within each object, attributes are searched in implementation-defined order.

If a $-command pattern matches, the corresponding action list is executed.
If multiple $-commands match, all matching commands are executed (not just
the first one).

**Implementation Note:** The exact $-command search order varies across
implementations. TinyMUSH and TinyMUX search the player, contents of the
player's location, the location, the player's inventory, then zones and the
master room. PennMUSH uses a similar but not identical order. This standard
specifies the general principle; the detailed order is implementation-defined
within the categories listed above.

### Step 6: No Match

If no match is found through any of the above steps, the server shall display
an error message to the player. The standard error message is:

```
Huh?  (Type "help" for help.)
```

The exact text of the no-match message is implementation-defined.

## Command Evaluation

### When Evaluation Occurs

Not all stages of command processing involve expression evaluation. The
following rules apply:

- **Built-in commands:** Arguments to most built-in commands are not evaluated
  before being passed to the command handler. The command handler itself
  decides whether to evaluate its arguments. Commands that explicitly evaluate
  their arguments (e.g., `@switch`, `@if`) are documented as doing so.

- **$-commands:** The action list portion of a $-command (after the `:`) is
  evaluated when the command is executed. The wildcard captures from the
  pattern match are available as `%0`, `%1`, etc.

- **Action lists:** Commands in action list attributes (ASUCC, AFAIL, etc.)
  are evaluated when executed.

### The did_it() Pipeline

When an event occurs on an object (e.g., a player looks at it, passes its
lock, or fails its lock), the server executes the **did_it pipeline**. This
is the standard mechanism for displaying messages and executing action lists:

1. **Player message:** The event attribute (e.g., SUCC) is evaluated and
   the result is sent to the player who triggered the event. If the attribute
   is not set, an optional default message is sent.

2. **Others message:** The "others" attribute (e.g., OSUCC) is evaluated and
   the result is sent to all other players in the same room. The player's
   name is prepended to the message. If the attribute is not set, an optional
   default message is sent.

3. **Action list:** The action attribute (e.g., ASUCC) is evaluated and
   executed as a command list.

The did_it pipeline processes all three phases for each event. If an attribute
is not set, the corresponding phase is skipped (or uses a hardcoded default,
depending on the event).

Example:

```
@succ button = You press the button.
@osucc button = presses the button.
@asucc button = @trigger me/ACTIVATE

> press button
You press the button.            [sent to the player]
Bob presses the button.           [sent to others]
[ACTIVATE action list executes]   [action runs]
```

## Special Command Handling

### The home Command

The `home` command is a special built-in that sends the player to their home
location. It is checked after built-in commands but before exit matching
in some implementations, and concurrently with exit matching in others. The
exact position in the matching order is implementation-defined, but `home`
shall always be recognized.

### The QUIT and WHO Commands

The `QUIT` and `WHO` commands are handled at the connection level and shall
be recognized regardless of the player's state. `QUIT` terminates the network
connection. `WHO` displays the list of connected players.

These commands shall be matched case-insensitively.

### Command Prefix Characters

Some implementations allow configuration of additional prefix characters
beyond the standard set. Whether additional prefix characters are supported
is implementation-defined.

## Logging and Monitoring

A conforming implementation should support logging of commands executed by
players with the SUSPECT flag. The implementation may also support broader
command logging for administrative purposes.

Commands executed by objects (via action lists, $-commands, or `@trigger`)
should not be logged by default but may be logged when the VERBOSE flag is
set on the object.
