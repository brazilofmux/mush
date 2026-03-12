# Quick Reference Card

## Movement

| Command | Action |
|---------|--------|
| `north` (or `n`) | Move north. |
| `south`, `east`, `west` | Move in that direction. |
| `home` | Return to your home location. |
| `enter <object>` | Enter an object. |
| `leave` | Leave the object you are inside. |

## Communication

| Command | Action |
|---------|--------|
| `say <message>` | Speak to the room. |
| `"<message>` | Shortcut for say. |
| `pose <message>` | Describe an action. |
| `:<message>` | Shortcut for pose. |
| `;<message>` | Semipose (no space after name). |
| `page <player> = <msg>` | Private message to a player. |
| `whisper <player> = <msg>` | Whisper in the same room. |
| `@emit <message>` | Emit text to the room with no name prefix. |

## Looking and Information

| Command | Action |
|---------|--------|
| `look` | See the current room. |
| `look <object>` | See an object's description. |
| `examine <object>` | Detailed object information (owner only). |
| `inventory` (or `i`) | List what you are carrying. |
| `WHO` | List connected players. |
| `@stats` | Database statistics (admin). |

## Building

| Command | Action |
|---------|--------|
| `@dig <name>` | Create a new room. |
| `@create <name>` | Create a new thing. |
| `@open <exit> = <dest>` | Create an exit to a destination. |
| `@link <exit> = <dest>` | Link an exit to a destination. |
| `@desc <obj> = <text>` | Set an object's description. |
| `@name <obj> = <name>` | Rename an object. |
| `@destroy <obj>` | Destroy an object. |
| `@clone <obj>` | Create a copy of an object. |

## Attributes and Properties

| Command | Action |
|---------|--------|
| `&<attr> <obj> = <val>` | Set a user attribute. |
| `@set <obj> = <flag>` | Set a flag on an object. |
| `@set <obj> = !<flag>` | Clear a flag. |
| `@lock <obj> = <key>` | Lock an object. |
| `@unlock <obj>` | Remove a lock. |
| `@parent <obj> = <parent>` | Set an object's parent. |
| `@chown <obj> = <player>` | Change ownership. |

## MUSHcode Essentials

| Syntax | Meaning |
|--------|---------|
| `think <expr>` | Evaluate and display to yourself. |
| `[function()]` | Evaluate a function inline. |
| `%#` | Dbref of the executor. |
| `%n` | Name of the executor. |
| `%0` - `%9` | Positional arguments. |
| `%r` | Newline. |
| `%b` | Space. |
| `%t` | Tab. |

## Common Functions

| Function | Purpose |
|----------|---------|
| `name(obj)` | Object's name. |
| `loc(obj)` | Object's location. |
| `get(obj/attr)` | Read an attribute. |
| `v(attr)` | Read own attribute. |
| `u(obj/attr, args)` | Call a user function. |
| `add(a, b)` | Addition. |
| `sub(a, b)` | Subtraction. |
| `mul(a, b)` | Multiplication. |
| `div(a, b)` | Integer division. |
| `eq(a, b)` | Equal? |
| `gt(a, b)` | Greater than? |
| `lt(a, b)` | Less than? |
| `if(cond, true, false)` | Conditional. |
| `switch(val, pat, res, ...)` | Multi-way branch. |
| `iter(list, pattern)` | Iterate over a list. |
| `cat(a, b, ...)` | Join with spaces. |
| `strlen(str)` | String length. |
| `mid(str, pos, len)` | Substring. |
| `ucstr(str)` | Uppercase. |
| `lcstr(str)` | Lowercase. |
| `ljust(str, width)` | Left-justify. |
| `rjust(str, width)` | Right-justify. |
| `ansi(code, str)` | Apply color. |
| `secure(str)` | Sanitize input. |
| `words(list)` | Count list elements. |
| `first(list)` | First element. |
| `rest(list)` | All but first. |
| `sort(list)` | Sort a list. |
| `setq(name, val)` | Set a register. |
| `r(name)` | Read a register. |

## \$-Commands

```
&CMD_NAME object = $pattern:action
```

The `$` prefix defines a custom command. `*` in the pattern captures
input as `%0`, `%1`, etc.

## ANSI Color Codes

| Code | Color |
|------|-------|
| `r` | Red |
| `g` | Green |
| `y` | Yellow |
| `b` | Blue |
| `m` | Magenta |
| `c` | Cyan |
| `w` | White |
| `h` | Highlight (bold) |

Use with `ansi()`: `ansi(hr, text)` produces bold red text.

## Mail

| Command | Action |
|---------|--------|
| `@mail` | List messages. |
| `@mail <num>` | Read message. |
| `@mail <player> = <subj>/<body>` | Send mail. |
| `@mail/reply <num> = <body>` | Reply. |
| `@mail/delete <num>` | Delete message. |

## Channels

| Command | Action |
|---------|--------|
| `@channel/list` | List channels. |
| `@channel/join <chan>` | Join a channel. |
| `@channel/leave <chan>` | Leave a channel. |
| `addcom <alias> = <chan>` | Add channel alias. |
| `<alias> <message>` | Talk on channel. |

## Debugging

| Command | Action |
|---------|--------|
| `@set me = TRACE` | Enable function tracing. |
| `@set me = !TRACE` | Disable tracing. |
| `@ps` | View the command queue. |
| `@halt me` | Stop all queued commands. |
