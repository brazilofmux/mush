# Lists and Iteration

## What Is a List?

In MUSHcode, a list is simply a string of values separated by spaces. There
is no special list type -- the string `apple banana cherry` is a list of
three elements.

```
> think words(apple banana cherry)
3
> think first(apple banana cherry)
apple
> think rest(apple banana cherry)
banana cherry
> think last(apple banana cherry)
cherry
```

## Accessing Elements

### By Position

```
> think extract(red green blue yellow, 2, 1)
green
> think extract(red green blue yellow, 2, 2)
green blue
```

`extract()` takes a list, a 1-based starting position, and a count.

### By Index List

```
> think elements(alpha beta gamma delta, 2 4)
beta delta
```

Returns elements at the specified positions.

## Modifying Lists

### Adding and Removing

```
> think ldelete(a b c d e, 3)
a b d e
> think insert(a b d e, 3, c)
a b c d e
> think replace(a b c d e, 3, X)
a b X d e
> think remove(a b c d e, c)
a b d e
```

### Searching

```
> think member(red green blue, green)
2
> think match(red green blue, gr*)
2
> think grab(cat dog fish, d*)
dog
```

`member()` does exact matching and returns the position. `match()` uses
wildcards. `grab()` returns the matching element itself.

## Sorting

```
> think sort(cherry apple banana)
apple banana cherry
> think sort(10 5 3 8 1, i)
1 3 5 8 10
```

The second argument specifies sort type: `a` for alphabetic (default),
`i` for integer, `f` for floating-point, `d` for dbref.

## Set Operations

```
> think setunion(a b c, b c d)
a b c d
> think setinter(a b c, b c d)
b c
> think setdiff(a b c, b c d)
a
```

`setunion()` returns all unique elements from both lists. `setinter()`
returns elements common to both. `setdiff()` returns elements in the
first list but not the second.

## Iterating with iter()

The `iter()` function is the workhorse of list processing:

```
> think iter(1 2 3 4 5, add(##, 10))
11 12 13 14 15
```

Within the pattern, `##` is the current element. The results are collected
into a new list.

### Filtering with iter()

```
> think iter(1 2 3 4 5 6, if(gt(##, 3), ##))
4 5 6
```

Elements that do not produce output are omitted (empty strings are squeezed
out by the space-separated output).

## Higher-Order Functions

### filter()

Returns only elements that pass a test:

```
> &FN_ISLONG me = gt(strlen(%0), 4)
> think filter(me/FN_ISLONG, cat dog elephant fish hippopotamus)
elephant hippopotamus
```

The filter function is called with each element as `%0` and should return
true or false.

### map()

Transforms each element through a function:

```
> &FN_SHOUT me = ucstr(%0)
> think map(me/FN_SHOUT, hello world goodbye)
HELLO WORLD GOODBYE
```

### fold()

Reduces a list to a single value:

```
> &FN_ADD me = add(%0, %1)
> think fold(me/FN_ADD, 1 2 3 4 5)
15
```

The function receives the accumulator as `%0` and the current element as
`%1`.

### sortby()

Sorts using a custom comparison function:

```
> &FN_BYLENGTH me = sub(strlen(%0), strlen(%1))
> think sortby(me/FN_BYLENGTH, cat elephant dog fish)
cat dog fish elephant
```

The comparison function receives two elements and returns negative (first
is smaller), zero (equal), or positive (first is larger).

## Custom Delimiters

Many list functions accept a custom delimiter. Use pipes instead of spaces:

```
> think words(red|green|blue, |)
3
> think first(red|green|blue, |)
red
> think iter(a|b|c, ucstr(##), |)
A B C
```

The input delimiter is specified as an extra argument. The output delimiter
defaults to the input delimiter unless specified separately.

## Practical Examples

### Formatting a Scoreboard

```
> &FN_SCORE_LINE me = [ljust(name(%0), 20)][rjust(get(%0/SCORE), 5)]
> &CMD_SCORES me = $+scores:@pemit %# =
  [ansi(hu, [ljust(Player, 20)][rjust(Score, 5)])]%r
  [iter(lattr(me/PLAYER_*), u(me/FN_SCORE_LINE, v(##)), , %r)]
```

### Building a List Incrementally

```
> think [setq(list,)]
  [iter(1 2 3 4 5,
    if(gt(##, 2),
      setq(list, cat(r(list), ##))))]
  Result: [r(list)]
Result: 3 4 5
```

### Processing Player Inventory

```
> &CMD_INVENTORY me = $+inv:@pemit %# =
  You are carrying:%r
  [iter(lcon(me), %b%b[name(##)]%r)]
```

## Quick Reference

| Function | What It Does |
|----------|-------------|
| `words(list)` | Count elements. |
| `first(list)` | First element. |
| `rest(list)` | All but first. |
| `last(list)` | Last element. |
| `extract(list, pos, count)` | Extract elements by position. |
| `elements(list, positions)` | Extract by index list. |
| `member(list, element)` | Find position of element. |
| `match(list, pattern)` | Find position by wildcard. |
| `grab(list, pattern)` | Return matching element. |
| `sort(list [, type])` | Sort a list. |
| `setunion(list1, list2)` | Union of two lists. |
| `setdiff(list1, list2)` | Difference of two lists. |
| `setinter(list1, list2)` | Intersection of two lists. |
| `iter(list, pattern)` | Iterate and transform. |
| `filter(func, list)` | Keep elements passing test. |
| `map(func, list)` | Transform each element. |
| `fold(func, list)` | Reduce to single value. |
