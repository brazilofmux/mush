# Control Flow

## Making Decisions

MUSHcode provides several ways to make decisions and repeat actions. Since
MUSHcode is functional (no statements, only expressions), control flow is
handled through functions.

## ifelse() and if()

The `ifelse()` function evaluates a condition and returns one of two values:

```
> think ifelse(gt(10, 5), Big, Small)
Big
> think ifelse(gt(3, 5), Big, Small)
Small
```

The syntax is `ifelse(<condition>, <true-value>, <false-value>)`. Only the
selected branch is evaluated -- the other is completely skipped.

`if()` is a shorter synonym available in PennMUSH and TinyMUX:

```
> think if(eq(%#, #1), You are God, You are not God)
You are not God
```

**Compatibility Note:** `ifelse()` is available across all four reference
implementations. `if()` is available in PennMUSH and TinyMUX but not in
TinyMUSH or RhostMUSH. For maximum portability, use `ifelse()`.

### Practical Example: A Guard

```
> &CMD_ENTER guard = $enter gate:@pemit %# =
  [if(strmatch(get(%#/FACTION), Alliance),
    The guard nods and lets you pass.,
    The guard blocks your path. "Alliance only.")]
```

## switch()

The `switch()` function compares a value against multiple patterns:

```
> think switch(red, red, Roses, blue, Sky, Unknown)
Roses
```

The syntax is:
`switch(<expression>, <pattern1>, <result1>, <pattern2>, <result2>, ..., <default>)`

Patterns use wildcard matching (`*` and `?`):

```
> think switch(apple, a*, Starts with A, b*, Starts with B, Other)
Starts with A
```

### Practical Example: A Vending Machine

```
> &CMD_BUY machine = $buy *:@pemit %# =
  [switch(%0,
    coffee, You get a steaming cup of coffee.,
    tea, You get a cup of tea.,
    water, You get a bottle of water.,
    Sorry%, we don't have that.)]
```

Note the `%,` to include a literal comma without it being treated as an
argument separator.

## The @switch Command

The command version of `switch()` executes commands instead of returning
values:

```
> @switch %0 = red, {say Red!}, blue, {say Blue!}, {say Unknown!}
```

Braces group each action. The `/all` switch executes **all** matching
cases instead of just the first:

```
> @switch/all fruit = *apple*, {say Has apple!}, *berry*,
  {say Has berry!}
```

## @if / @ifelse

The command version of conditional evaluation (available in PennMUSH and
TinyMUX; not available in TinyMUSH or RhostMUSH):

```
> @if gt(%0, 10) = {say Big number!}, {say Small number.}
```

## @dolist: Iterating Over Lists

`@dolist` executes a command once for each item in a list:

```
> @dolist apple banana cherry = {say I like ##!}
You say, "I like apple!"
You say, "I like banana!"
You say, "I like cherry!"
```

Within the action, `##` is replaced by the current item and `#@` by the
position (starting at 1).

### Practical Example: Greet Everyone

```
> &CMD_GREETALL me = $greetall:@dolist lcon(loc(me)) =
  {@pemit ## = [name(me)] waves hello to you!}
```

This sends a greeting to every object in the room.

## iter(): Functional Iteration

The `iter()` function is the expression equivalent of `@dolist`. It
evaluates a pattern for each list element and returns the results:

```
> think iter(apple banana cherry, ucstr(##))
APPLE BANANA CHERRY
```

Within the pattern, `##` is the current element and `#@` is the position.

```
> think iter(1 2 3 4 5, mul(##, ##))
1 4 9 16 25
```

## Nested Iteration

You can nest `iter()` calls. Use `itext()` and `inum()` to access outer
loop values:

```
> think iter(A B, iter(1 2, [itext(1)][itext(0)]))
A1 A2 B1 B2
```

`itext(0)` is the innermost loop's current element; `itext(1)` is the
next outer loop's element.

## @wait: Delayed Execution

The `@wait` command queues an action for later:

```
> @wait 5 = say Five seconds have passed.
```

After 5 seconds, your character says the message. This is useful for timed
events, delays between actions, and dramatic pauses.

### Practical Example: A Ticking Bomb

```
> &CMD_LIGHT bomb = $light bomb:@emit The fuse is lit!;
  @wait 3 = {@emit Tick...};
  @wait 6 = {@emit Tick... tick...};
  @wait 10 = {@emit BOOM! The bomb explodes!}
```

## Recursion with u()

Since MUSHcode has no traditional loops beyond `@dolist` and `iter()`, more
complex iteration uses recursion -- a function that calls itself:

```
> &FN_COUNTDOWN me = [if(gt(%0, 0),
  %0... [u(me/FN_COUNTDOWN, sub(%0, 1))],
  Go!)]
> think u(me/FN_COUNTDOWN, 5)
5... 4... 3... 2... 1... Go!
```

The function calls itself with a smaller number until it reaches zero.
Be careful with recursion -- there is a nesting limit to prevent infinite
loops.

## Combining Techniques

Real MUSHcode often combines several control flow tools:

```
> &CMD_STATUS me = $+status *:@pemit %# =
  [switch(%0,
    health, Your health: [v(HEALTH)]/[v(MAXHEALTH)],
    mana, Your mana: [v(MANA)]/[v(MAXMANA)],
    all, Health: [v(HEALTH)]/[v(MAXHEALTH)]%r
         Mana: [v(MANA)]/[v(MAXMANA)]%r
         Gold: [v(GOLD)],
    Unknown status type. Try: health%, mana%, or all)]
```

## Quick Reference

| Tool | Use |
|------|-----|
| `if(cond, true, false)` | Inline conditional. |
| `switch(val, pat, result, ...)` | Multi-way pattern match. |
| `@if cond = {true}, {false}` | Command conditional. |
| `@switch val = pat, {action}, ...` | Command multi-way branch. |
| `@dolist list = {action}` | Command iteration. |
| `iter(list, pattern)` | Functional iteration. |
| `@wait secs = {action}` | Delayed execution. |
