# User-Defined Commands and Functions

## $-Commands: Custom Commands

A $-command is an attribute that defines a new command players can type. It
is the most common way to add interactivity to objects.

### Basic Syntax

```
> &CMD_GREET me = $greet:say Hello!
```

The format is `$<pattern>:<action>`. When anyone in the room types
something matching the pattern, the action executes.

### Wildcard Arguments

Use `*` in the pattern to capture player input:

```
> &CMD_GREET me = $greet *:say Hello, %0!
```

```
> greet Morgan
You say, "Hello, Morgan!"
```

The first `*` becomes `%0`, the second becomes `%1`, and so on up to `%9`:

```
> &CMD_GIVE me = $+give * to *:@pemit %# = You give %0 to %1.
```

```
> +give sword to Morgan
You give sword to Morgan.
```

### Where $-Commands Live

$-commands work on any object in the same room as the player, or on the
player's own inventory, or on the player themselves. The server searches:

1. The player object.
2. Objects in the player's inventory.
3. Objects in the current room.
4. The current room itself.
5. The master room (#0) and zone objects.

### Command Conflicts

If multiple objects define the same command, only the first match is
executed (following the search order above). Choose distinctive command
names to avoid conflicts. The convention is to use a prefix like `+`:

```
+score      +combat     +mail       +roll
```

## User Functions: u()

The `u()` function calls an attribute as a function, passing arguments:

```
> &FN_DOUBLE me = mul(%0, 2)
> think u(me/FN_DOUBLE, 21)
42
```

Inside the called attribute, `%0` through `%9` contain the arguments.

### Why Use u()?

Functions let you reuse code. Instead of repeating the same formula
everywhere, write it once and call it:

```
> &FN_HP_BAR me = [repeat(|, %0)][repeat(., sub(%1, %0))]
  %b[%0]/[%1]
> think u(me/FN_HP_BAR, 7, 10)
|||||||...  7/10
> think u(me/FN_HP_BAR, 3, 10)
|||.......  3/10
```

### ulocal(): Protecting Registers

`u()` shares the caller's registers. If the called function changes a
register, the caller sees the change. `ulocal()` prevents this:

```
> &FN_HELPER me = [setq(temp, ucstr(%0))][r(temp)]
> think [setq(temp, important)][ulocal(me/FN_HELPER, hello)]
  %r temp is still: [r(temp)]
HELLO
 temp is still: important
```

With `u()` instead of `ulocal()`, the `temp` register would have been
overwritten to "HELLO."

**Rule of thumb:** Use `ulocal()` unless you specifically want to share
registers.

### default() and udefault()

The `default()` function reads an attribute, falling back to a default if
it does not exist:

```
> think default(me/TITLE, Untitled)
Untitled
```

`udefault()` calls a function, falling back to a default:

```
> think udefault(me/FN_MISSING, Default Value, arg1, arg2)
Default Value
```

## @trigger: Executing Attributes

The `@trigger` command executes an attribute as an action list:

```
> &DO_ANNOUNCE me = @emit [name(me)] announces: %0
> @trigger me/DO_ANNOUNCE = Hello everyone!
Sparrow announces: Hello everyone!
```

Unlike `u()`, `@trigger` runs in the command queue (like `@dolist`). It does
not return a value -- it runs commands.

### Passing Arguments to @trigger

```
> @trigger me/DO_SOMETHING = arg0, arg1, arg2
```

Inside the attribute, `%0` is "arg0", `%1` is "arg1", etc.

## Practical Example: A Dice Roller

Let's build a complete dice roller object:

```
> @create Dice Roller
> @desc Dice Roller = A small box with polished dice inside.
  Type '+roll <dice>' to roll (e.g., '+roll 2d6').

> &CMD_ROLL Dice Roller = $+roll *:@pemit %# =
  [u(me/FN_PARSE_ROLL, %0)]

> &FN_PARSE_ROLL Dice Roller =
  [if(regmatch(%0, ^(\d+)d(\d+)$, 0 1 2),
    u(me/FN_DO_ROLL, r(1), r(2)),
    Usage: +roll <count>d<sides>)]

> &FN_DO_ROLL Dice Roller =
  [setq(total, die(%0, %1))]
  Rolling %0d%1: [ansi(hc, r(total))]
```

```
> +roll 2d6
Rolling 2d6: 8
> +roll 3d10
Rolling 3d10: 17
> +roll banana
Usage: +roll <count>d<sides>
```

## Practical Example: A Simple Stat System

```
> @create Character Sheet
> @parent me = Character Sheet

> &HEALTH Character Sheet = 100
> &MAXHEALTH Character Sheet = 100
> &MANA Character Sheet = 50
> &MAXMANA Character Sheet = 50

> &CMD_STATUS Character Sheet = $+stat:@pemit %# =
  %r[ansi(hw, === Character Status ===)]%r
  Health: [u(me/FN_BAR, v(HEALTH), v(MAXHEALTH))]%r
  Mana:   [u(me/FN_BAR, v(MANA), v(MAXMANA))]

> &FN_BAR Character Sheet =
  [ansi(hg, repeat(#, div(mul(%0, 20), %1)))]
  [ansi(hr, repeat(-, sub(20, div(mul(%0, 20), %1))))]
  %b%0/%1
```

## Tips

- **Name your attributes clearly.** Use `CMD_` for commands, `FN_` for
  functions, `DO_` for triggered action lists.
- **Test with think.** Before putting code on an object, test the
  expression with `think`.
- **Use ulocal() by default.** Only use `u()` when you need register
  sharing.
- **Keep functions short.** Break complex operations into multiple small
  functions that call each other.
- **Comment your code** by adding attributes like `&HELP_ROLL object = This
  command rolls dice in NdS format.`
