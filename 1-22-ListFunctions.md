# List Functions

## Overview

Lists are the primary compound data structure in MUSHcode. A list is a string
of elements separated by a delimiter, with space as the default delimiter.
List functions provide operations for creating, accessing, modifying,
searching, sorting, and iterating over lists.

Many list functions accept optional input and output delimiter parameters.
When an input delimiter (\<idelim\>) is specified, the function uses that
character instead of space to separate list elements. When an output delimiter
(\<odelim\>) is specified, results use that character as the separator
(defaulting to the input delimiter).

## Element Access

### first()

```
first(<list> [, <delimiter>])
```

Returns the first element of \<list\>.

### rest()

```
rest(<list> [, <delimiter>])
```

Returns all elements of \<list\> except the first.

### last()

```
last(<list> [, <delimiter>])
```

Returns the last element of \<list\>.

### extract()

```
extract(<list>, <start>, <length> [, <idelim> [, <odelim>]])
```

Returns \<length\> elements from \<list\> beginning at position \<start\>
(1-based).

### index()

```
index(<string>, <delimiter>, <start>, <end>)
```

Returns the substring between field positions \<start\> and \<end\>, where
fields are separated by \<delimiter\>.

### elements()

```
elements(<list>, <positions> [, <idelim> [, <odelim>]])
```

Returns the elements of \<list\> at the specified \<positions\> (a
space-separated list of 1-based indices).

## List Information

### words()

```
words(<list> [, <delimiter>])
```

Returns the number of elements in \<list\>.

### member()

```
member(<list>, <element> [, <delimiter>])
```

Returns the 1-based position of \<element\> in \<list\>, or 0 if not found.
Comparison is case-insensitive and uses exact word matching.

### match()

```
match(<list>, <pattern> [, <delimiter>])
```

Returns the 1-based position of the first element in \<list\> that matches
\<pattern\> using wildcard matching (`*` and `?`), or 0 if no match is found.

### matchall()

```
matchall(<list>, <pattern> [, <idelim> [, <odelim>]])
```

Returns a list of 1-based positions of all elements in \<list\> that match
\<pattern\>.

## List Modification

### ldelete()

```
ldelete(<list>, <position> [, <delimiter>])
```

Returns \<list\> with the element at 1-based \<position\> removed.

### replace()

```
replace(<list>, <position>, <new-element> [, <delimiter>])
```

Returns \<list\> with the element at 1-based \<position\> replaced by
\<new-element\>.

### insert()

```
insert(<list>, <position>, <element> [, <delimiter>])
```

Returns \<list\> with \<element\> inserted before 1-based \<position\>.

### remove()

```
remove(<list>, <element> [, <delimiter>])
```

Returns \<list\> with the first occurrence of \<element\> removed.

## Searching

### grab()

```
grab(<list>, <pattern> [, <delimiter>])
```

Returns the first element of \<list\> that matches \<pattern\> using wildcard
matching, or an empty string if no match is found.

### graball()

```
graball(<list>, <pattern> [, <idelim> [, <odelim>]])
```

Returns all elements of \<list\> that match \<pattern\>.

## Reordering

### revwords()

```
revwords(<list> [, <idelim> [, <odelim>]])
```

Returns \<list\> with its elements in reverse order.

### sort()

```
sort(<list> [, <sort-type> [, <idelim> [, <odelim>]]])
```

Returns \<list\> sorted in ascending order. The \<sort-type\> parameter
controls how elements are compared:

| Type | Description |
|------|-------------|
| `a`  | Alphabetic (case-insensitive, default) |
| `i`  | Integer (numeric) |
| `f`  | Floating-point |
| `d`  | Dbref |
| `n`  | Name (sort by object name) |

### sortby()

```
sortby(<sort-function>, <list> [, <delimiter>])
```

Sorts \<list\> using \<sort-function\> as a comparator. The sort function is
called with two elements as `%0` and `%1` and shall return a negative number,
zero, or positive number indicating relative order.

### shuffle()

```
shuffle(<list> [, <delimiter>])
```

Returns \<list\> with its elements in random order.

## Set Operations

### setunion()

```
setunion(<list1>, <list2> [, <idelim> [, <odelim>]])
```

Returns the sorted union of two lists (all unique elements from both lists).

### setdiff()

```
setdiff(<list1>, <list2> [, <idelim> [, <odelim>]])
```

Returns the sorted difference of two lists (elements in \<list1\> that are not
in \<list2\>).

### setinter()

```
setinter(<list1>, <list2> [, <idelim> [, <odelim>]])
```

Returns the sorted intersection of two lists (elements present in both lists).

### unique()

```
unique(<list> [, <idelim> [, <odelim>]])
```

Returns \<list\> with duplicate elements removed, preserving the order of
first occurrence.

## Iteration

### iter()

```
iter(<list>, <pattern> [, <idelim> [, <odelim>]])
```

Evaluates \<pattern\> once for each element of \<list\> and returns the
results as a list. Within the pattern, `##` is replaced by the current
element, and `#@` is replaced by the 1-based iteration number.

### itext()

```
itext(<depth>)
```

Returns the current iteration element at the specified nesting depth. Depth 0
is the innermost `iter()`, depth 1 is the next outer, and so on.

### inum()

```
inum(<depth>)
```

Returns the current 1-based iteration number at the specified nesting depth.

### ilev()

```
ilev()
```

Returns the current nesting level of `iter()` calls (0 for the outermost).

## Higher-Order Functions

### map()

```
map(<function>, <list> [, <idelim> [, <odelim>]])
```

Applies \<function\> (an \<object\>/\<attribute\> reference) to each element of
\<list\>. The current element is passed as `%0`. Returns the list of results.

### filter()

```
filter(<function>, <list> [, <idelim> [, <odelim>]])
```

Returns elements of \<list\> for which \<function\> returns a true (non-zero,
non-empty) value. The current element is passed as `%0`.

### fold()

```
fold(<function>, <list> [, <base> [, <delimiter>]])
```

Reduces \<list\> to a single value by repeatedly applying \<function\>. The
function receives the accumulator as `%0` and the current element as `%1`.
If \<base\> is provided, it is the initial accumulator value; otherwise, the
first element is used.

### munge()

```
munge(<function>, <list1>, <list2> [, <delimiter>])
```

Applies \<function\> to \<list1\> to produce a reordered/filtered list, then
rearranges \<list2\> to match the resulting order. This enables sorting one
list by the values of another.

### mix()

```
mix(<function>, <list1>, <list2> [, ... [, <delimiter>]])
```

Applies \<function\> element-wise to corresponding elements from two or more
lists. The function receives elements from each list as `%0`, `%1`, etc.
Returns the list of results.

### step()

```
step(<function>, <list>, <step-size> [, <idelim> [, <odelim>]])
```

Applies \<function\> to groups of \<step-size\> consecutive elements from
\<list\>. Elements within each group are passed as `%0`, `%1`, etc. Level 2.

## Formatting

### table()

```
table(<list>, <field-width> [, <line-length> [, <idelim> [, <odelim>]]])
```

Formats \<list\> as a table with columns of \<field-width\> characters,
wrapping at \<line-length\> (default 78). Level 2.

### columns()

```
columns(<list>, <width> [, <idelim> [, <line-length>]])
```

Formats \<list\> into columns of the specified width. Level 2.

## Implementation Notes

List positions in MUSHcode are universally 1-based, unlike character positions
which are 0-based. This convention applies to all list functions:
`extract()`, `ldelete()`, `replace()`, `insert()`, `member()`, `match()`,
`matchall()`, `elements()`, and the `#@` substitution in `iter()`.

The default delimiter for all list functions is a single space character.
Leading and trailing delimiters are not significant; an empty string and a
string of spaces both represent an empty list.

Set operation functions (`setunion()`, `setdiff()`, `setinter()`) return
their results in sorted order. The sort type used is implementation-defined
but is typically case-insensitive alphabetic.
