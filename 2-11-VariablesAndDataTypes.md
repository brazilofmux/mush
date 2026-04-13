# Variables and Data Types

## Everything Is a String

MUSHcode has a single data type: the string. Numbers, dbrefs, lists, boolean
values -- everything is represented as text. The function `add(2, 3)` takes
two strings that look like numbers, treats them as numbers, and returns the
string `5`.

This simplicity means you never have to worry about type declarations,
casting, or type errors. But it also means you need to be aware of how
functions interpret their arguments.

## Registers: Temporary Variables

Registers are temporary storage slots that persist for the duration of an
action list. You set them with `setq()` and read them with `r()`:

```
> think [setq(0, Hello World)][r(0)]
Hello World
```

The `setq()` function stores a value in a register and returns nothing
(empty string). The `r()` function retrieves the stored value.

### Named and Numbered Registers

Most servers support both numbered registers (0-9) and named registers:

```
> think [setq(0, Alice)][setq(1, Bob)]%r[r(0)] and [r(1)]
Alice and Bob
```

Named registers are clearer:

```
> think [setq(name, Alice)][setq(greeting, Hello)]
  [r(greeting)], [r(name)]!
Hello, Alice!
```

### setr(): Set and Return

The `setr()` function sets a register and returns the value at the same
time:

```
> think The answer is [setr(result, add(6, 7))], stored as [r(result)].
The answer is 13, stored as 13.
```

This is useful when you need to both display and store a computed value.

### Register Scope

Registers are scoped to a single interactive command invocation.
They are cleared at the start of each command you type, but they
**persist** across queued continuations of that command — so a
`@trigger` or `@dolist` launched from the same command sees the
registers you set, and later `@wait`-delayed steps continue to share
them until the command's queue entries drain. If you call a user
function with `u()`, the called function **shares** your registers.
If you call with `ulocal()`, the called function gets its own copy --
changes it makes do not affect your registers.

## Attributes: Persistent Storage

For data that needs to persist beyond a single action list, store it in
attributes:

```
> &SCORE me = 0
> think v(SCORE)
0
```

To change it from code, use the `set()` side-effect function:

```
> think [set(me/SCORE, add(v(SCORE), 10))]Score is now [v(SCORE)]
Score is now 10
```

Or use the `&` attribute-set shorthand in an action list:

```
> &CMD_ADDSCORE me = $+score:&SCORE me=
  [add(v(SCORE), 1)]; @pemit %# = Score: [v(SCORE)]
```

> **Watch out:** `@set <obj>/<attr> = <value>` does **not** write the
> attribute's value — in every major engine, that form sets an
> attribute *flag* whose name is `<value>`. To update an attribute's
> value you want either `&<attr> <obj> = <new-value>` (as shown above)
> or the attribute-value form of `@set`, `@set <obj> = <attr>:<value>`.
> If your code is silently doing nothing, check which form you used.

## Numeric Operations

Even though everything is a string, MUSHcode provides full numeric support:

```
> think add(10, 5)
15
> think sub(10, 5)
5
> think mul(3, 7)
21
> think div(20, 3)
6
> think fdiv(20, 3)
6.666667
> think mod(20, 3)
2
```

### Floating-Point Numbers

MUSHcode handles decimals:

```
> think add(3.14, 2.86)
6
> think fdiv(22, 7)
3.142857
> think round(3.14159, 2)
3.14
```

### Comparisons

Comparisons return 1 (true) or 0 (false):

```
> think gt(10, 5)
1
> think lt(10, 5)
0
> think eq(7, 7)
1
```

## Boolean Values

MUSHcode treats these values as false:

- `0` (zero)
- Empty string (nothing)
- `#-1` and other negative dbrefs

Everything else is true. The `t()` function normalizes any value to 1 or 0:

```
> think t(42)
1
> think t(0)
0
> think t(hello)
1
> think t()
0
```

## Dbrefs as Data

Dbrefs are just strings that start with `#`:

```
> think loc(me)
#5
> think name(loc(me))
Town Square
> think owner(me)
#42
```

You can store dbrefs in registers and attributes and pass them to functions
like any other data:

```
> think [setq(here, loc(me))]I am in [name(r(here))]
I am in Town Square
```

## Type Checking Functions

Since everything is a string, MUSHcode provides functions to check what
a value looks like:

```
> think isnum(42)
1
> think isnum(hello)
0
> think isdbref(#42)
1
> think isdbref(#-1)
0
> think isword(hello)
1
> think isword(hello123)
0
```

## Working with Object Data

The most common pattern in MUSHcode is reading data from objects:

```
> think get(me/DESC)
A tall woman with short dark hair.
```

`get()` returns the raw (unevaluated) value of an attribute. `v()` is a
shortcut for getting attributes on the current object:

```
> think v(DESC)
A tall woman with short dark hair.
```

To get an attribute from another object:

```
> think get(#5/DESC)
A bustling town square...
```

## Summary

| Concept | How To |
|---------|--------|
| Set a register | `setq(name, value)` |
| Read a register | `r(name)` |
| Set and return | `setr(name, value)` |
| Store permanently | `&ATTR object = value` |
| Read an attribute | `v(ATTR)` or `get(obj/ATTR)` |
| Check type | `isnum()`, `isdbref()`, `isword()` |
| Boolean test | `t(value)` |
