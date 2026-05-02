# Administration Commands

## Overview

Administration commands control server operations, manage players, and
provide tools for maintaining the MUSH. Most of these commands require wizard
privileges or specific powers.

## Server Control

### @shutdown

```
@shutdown
```

The `@shutdown` command shuts down the MUSH server. The database is saved
before shutdown. This command requires wizard privileges.

Available switches are implementation-defined. PennMUSH provides `/reboot`
and `/panic`; TinyMUSH provides `/abort` (which triggers an abnormal
termination with core dump, not a cancellation of a pending shutdown).
TinyMUX provides no switches.

### @restart

```
@restart
```

The `@restart` command restarts the MUSH server process. The database is saved,
the server shuts down, and a new instance starts automatically. This command
requires wizard privileges. Level 2.

### @dump

```
@dump
```

The `@dump` command forces an immediate database save. This creates a
checkpoint of the current database state. Normal database dumps occur
automatically at intervals configured by the server administrator.

PennMUSH provides a `/paranoid` switch that performs additional consistency
checks during the dump. This switch is not available in TinyMUX or
TinyMUSH. Level 2.

## Player Management

### @pcreate

```
@pcreate <name> = <password>
```

The `@pcreate` command creates a new player without requiring a network
connection. This is used by wizards to create accounts for specific
individuals. Requires wizard privileges or the CREATE_PLAYER power.

### @newpassword

```
@newpassword <player> = <new-password>
```

The `@newpassword` command resets a player's password. This is used when a
player has forgotten their password. Requires wizard privileges.

### @boot

```
@boot [/port] <player>
```

The `@boot` command disconnects a player from the server. All of the player's
network connections are closed. Requires wizard privileges or the CAN_BOOT
power.

The `/port` switch disconnects a specific port number rather than all
connections for a player.

### @toad

```
@toad <player> [= <recipient>]
```

The `@toad` command converts a player object into a thing, effectively
removing the player's ability to log in. Objects owned by the toaded player
may be optionally transferred to a recipient.

This command is irreversible in practice and should be used only as a last
resort for problem players. Requires wizard privileges.

### @quota

```
@quota [<player>]
@quota/set <player> = <amount>
```

The `@quota` command displays a player's object creation quota -- the number
of additional objects they may create. The `/set` switch changes a player's
quota (requires wizard privileges or the CHANGE_QUOTAS power).

Whether quota enforcement is enabled is a server configuration option.

## Queue Management

### @halt

```
@halt [<object>]
```

The `@halt` command removes all pending queue entries for the specified object
(or the player, if no object is specified). See Chapter 11 for full details.

### @halt/all

```
@halt/all
```

The `@halt/all` command clears all entries from the command queue for all
objects. Requires wizard privileges or the HALT_ANYTHING power. This is an
emergency command for stopping runaway softcode.

TinyMUX and TinyMUSH use `@halt/all`. PennMUSH provides both `@halt/all`
and the alias `@allhalt`. RhostMUSH uses `@halt/all`. Conforming
implementations shall support the `/all` switch on `@halt`.

### @ps

```
@ps [<object>]
```

The `@ps` command displays the contents of the command queue. See Chapter 11
for full details.

## Control Flow Commands

### @switch

```
@switch [/all] <expression> = <pattern1>, <action1>
    [, <pattern2>, <action2>]...
    [, <default-action>]
```

The `@switch` command evaluates \<expression\> and compares the result against
each \<pattern\>. The action corresponding to the first matching pattern is
executed. Patterns use wildcard matching.

The `/all` switch executes the actions for all matching patterns, not just
the first.

If no pattern matches and a default action is provided (an action without a
preceding pattern at the end of the list), the default action is executed.

Example:

```
> @switch %0 = red, {say Red!}, blue, {say Blue!}, {say Unknown color.}
```

### @if / @ifelse

```
@if <condition> = <true-action> [, <false-action>]
```

The `@if` command evaluates \<condition\>. If the result is true (non-zero
and non-empty), the \<true-action\> is executed. Otherwise, the optional
\<false-action\> is executed. Level 2.

TinyMUX provides `@if` (which handles both the true and false branches).
PennMUSH provides `@ifelse` (with `@skip` as an alias) but not `@if`.
The two commands are functionally identical. TinyMUSH and RhostMUSH do not
provide either command; equivalent logic must be achieved with `@switch` or
the `ifelse()` function.

Example:

```
> @if gt(%0, 10) = {say Big number!}, {say Small number.}
```

### @dolist

```
@dolist [/delimit <sep>] <list> = <action>
```

The `@dolist` command iterates over a list, executing \<action\> once for
each element. Within the action, `##` is replaced with the current element
and `#@` is replaced with the current position (starting from 1).

The `/delimit` switch specifies a custom list separator (default is space).

Example:

```
> @dolist apple banana cherry = {say I like ##!}
You say, "I like apple!"
You say, "I like banana!"
You say, "I like cherry!"
```

### @wait

```
@wait <seconds> = <action>
@wait <object> = <action>
@wait <object>/<timeout> = <action>
```

The `@wait` command queues an action for delayed or synchronized execution.
See Chapter 11 for full details.

### @trigger

```
@trigger <object>/<attribute> [= <arg0>, <arg1>, ..., <arg9>]
```

The `@trigger` command executes the contents of an attribute as an action
list. See Chapter 11 for full details.

## Database Information

### @stats

```
@stats [/all] [<player>]
```

The `@stats` command displays database statistics: the total number of
objects, broken down by type (rooms, things, exits, players, garbage).
With a player argument, shows statistics for that player's objects.

The `/all` switch provides detailed breakdowns. Viewing other players' stats
requires wizard privileges or the SEARCH_EVERYTHING power.

### @list

```
@list <category>
```

The `@list` command displays lists of server-defined items. Common categories:

| Category     | Displays |
|--------------|----------|
| `attributes` | Built-in attribute names and numbers. |
| `commands`   | Built-in command names. |
| `functions`  | Built-in function names. |
| `flags`      | Available flag names and characters. |
| `powers`     | Available power names. |

### @uptime

```
@uptime
```

The `@uptime` command displays how long the server has been running since
its last restart. Available in PennMUSH (`@uptime`) and RhostMUSH
(`+uptime`). TinyMUX and TinyMUSH do not provide this command. Level 2.

## Object Administration

### @chown

See Chapter 18 for the full specification.

### @chzone

```
@chzone <object> = <zone>
```

The `@chzone` command changes an object's zone assignment (see
Chapter 29). PennMUSH also accepts the shorter `@zone` as an alias;
TinyMUX, TinyMUSH, and RhostMUSH register `@chzone` only.

### @power

```
@power <object> = <power-name>
@power <object> = !<power-name>
```

The `@power` command grants or revokes powers. See Chapter 8 for full
details.

## Administrative Communication

### @wall

See Chapter 16 for the full specification.

### @motd

```
@motd <message>
```

The `@motd` command sets the Message of the Day, displayed to players when
they connect. Requires wizard privileges.

### @doing

```
@doing <message>
```

The `@doing` command sets the player's DOING message, displayed in the WHO
list. TinyMUX and TinyMUSH provide `@doing` as a built-in command.
PennMUSH does not have `@doing`; players set their DOING message via the
`DOING` connection-level command or `@poll`. Level 2.

## Configuration

### @function

```
@function <name> = <object>/<attribute>
@function/delete <name>
```

The `@function` command registers or removes a global user-defined function.
See Chapter 14 for details.

Permission requirements vary by implementation: TinyMUX and TinyMUSH
restrict `@function` to God (privilege level 1). PennMUSH requires the
`Global_Funcs` power. RhostMUSH requires wizard privileges. A conforming
implementation shall restrict `@function` to sufficiently privileged
administrators; the exact mechanism is implementation-defined.

### @attribute

```
@attribute/access <name> = <flags>
```

The `@attribute` command manages global attribute definitions, including
default flags for user-defined attribute names. See Chapter 6 for details.

## Help System

A conforming implementation shall provide at least a topic-based help
lookup command. The `help` command with an optional \<topic\> argument
is the common entry point.

### help

```
help [<topic>]
```

The `help` command displays help text on the specified topic. Without
an argument, it displays a general index. Matching behavior (exact,
prefix, wildcard, or substring) is implementation-defined, but all
four reference engines accept unambiguous prefix matches.

### Additional Help Commands

Most engines ship one or more additional help namespaces for
restricted audiences or alternative content. The set of commands and
their scopes is **implementation-defined**. Representative examples:

| Command       | Scope                                   | Engines |
|---------------|-----------------------------------------|---------|
| `wizhelp`     | Wizard-only topics                      | TinyMUX, TinyMUSH, RhostMUSH |
| `plushelp`    | Plus-command softcode reference         | TinyMUX, TinyMUSH            |
| `staffhelp`   | Staff procedures                        | TinyMUX                      |
| `+help`       | Admin-provided supplementary help       | TinyMUSH (`helpfile` config) |

PennMUSH takes a different approach: instead of a fixed command set,
it exposes the help subsystem through the `help_command` and
`ahelp_command` configuration directives, which bind arbitrary
command names to named help indexes. PennMUSH's built `help`
command itself is composed at build time from multiple source
directories (`game/txt/hlp/`) via a composition script.

RhostMUSH's `help` command additionally accepts `/search`, `/query`,
and `/syntax` switches for wildcard topic search, content search,
and usage-only display respectively.

### Help File Layout (Implementation-Defined)

This standard does not specify:

- The on-disk file format or directory layout.
- Whether indexes are precomputed, generated at startup, or composed
  at build time.
- The matching algorithm (exact, prefix, wildcard, substring).
- Whether administrators may add custom help namespaces at runtime or
  only through server configuration.

Conforming implementations shall document these choices. Portable
softcode must not assume that, for example, `wizhelp` exists or that
`help_command` is configurable.

## WHO and Connection Information

### WHO

```
WHO [<pattern>]
```

The `WHO` command displays a list of currently connected players, including
their names, idle times, connection times, and DOING messages. The optional
pattern filters the list.

WHO visibility of privileged players is implementation-defined. Common
mechanisms include the DARK flag (which may require a `Can_Dark` or
`Can_Hide` power), the UNFINDABLE flag, and the `Hidden` power. The
interaction between these flags and powers varies across implementations.

### DOING

```
DOING [<message>]
```

Sets the player's DOING column in the WHO list. Without an argument, displays
the current WHO list (equivalent to `WHO`).

## Session Commands

### QUIT

```
QUIT
```

The `QUIT` command disconnects the current network connection. If the player
has other connections, those remain active. `QUIT` is recognized at the
connection level and does not require the player to be logged in.

### @password

```
@password <old-password> = <new-password>
```

The `@password` command changes the player's own password. The old password
must be provided for verification.
