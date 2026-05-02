# Boolean and Comparison Functions

## Overview

Boolean and comparison functions evaluate truth values and compare operands.
MUSHcode uses a simple truthiness model: the values `0`, an empty string, and
the special dbrefs `#-1`, `#-2`, and `#-3` are false. All other values are
true.

## Truth Testing

### t()

```
t(<value>)
```

Returns 1 if \<value\> is true, and 0 if it is false. This is the canonical
way to normalize a value to a boolean.

### isnum()

```
isnum(<string>)
```

Returns 1 if \<string\> is a valid number (integer or floating-point), and 0
otherwise.

### isint()

```
isint(<string>)
```

Returns 1 if \<string\> is a valid integer, and 0 otherwise. Level 2.

### isdbref()

```
isdbref(<string>)
```

Returns 1 if \<string\> is a valid dbref that refers to an existing object,
and 0 otherwise.

### isobjid()

```
isobjid(<string>)
```

Returns 1 if \<string\> is a valid object identifier (dbref or
dbref:timestamp), and 0 otherwise. Level 2.

### isword()

```
isword(<string>)
```

Returns 1 if \<string\> contains only alphabetic characters, and 0 otherwise.

## Logical Operators

### and()

```
and(<value1>, <value2>, ...)
```

Returns 1 if all arguments are true, and 0 otherwise. All arguments are
evaluated regardless of the results. Accepts two or more arguments.

### or()

```
or(<value1>, <value2>, ...)
```

Returns 1 if any argument is true, and 0 otherwise. All arguments are
evaluated regardless of the results. Accepts two or more arguments.

### not()

```
not(<value>)
```

Returns 1 if \<value\> is false, and 0 if \<value\> is true.

### xor()

```
xor(<value1>, <value2>, ...)
```

Returns 1 if an odd number of arguments are true, and 0 otherwise.

## Short-Circuit Operators

### cand()

```
cand(<expression1>, <expression2>, ...)
```

Conditional AND. Evaluates each expression in order. If any expression
evaluates to false, immediately returns 0 without evaluating the remaining
expressions. Returns 1 if all expressions are true.

This is the MUSHcode equivalent of C's `&&` operator. Use `cand()` instead
of `and()` when later arguments have side effects or depend on earlier
conditions being true.

### cor()

```
cor(<expression1>, <expression2>, ...)
```

Conditional OR. Evaluates each expression in order. If any expression
evaluates to true, immediately returns 1 without evaluating the remaining
expressions. Returns 0 if all expressions are false.

This is the MUSHcode equivalent of C's `||` operator.

## Numeric Comparison

### eq()

```
eq(<number1>, <number2>)
```

Returns 1 if \<number1\> equals \<number2\>, and 0 otherwise. Both arguments
are treated as numbers.

### neq()

```
neq(<number1>, <number2>)
```

Returns 1 if \<number1\> does not equal \<number2\>, and 0 otherwise.

### gt()

```
gt(<number1>, <number2>)
```

Returns 1 if \<number1\> is greater than \<number2\>, and 0 otherwise.

### gte()

```
gte(<number1>, <number2>)
```

Returns 1 if \<number1\> is greater than or equal to \<number2\>, and 0
otherwise.

### lt()

```
lt(<number1>, <number2>)
```

Returns 1 if \<number1\> is less than \<number2\>, and 0 otherwise.

### lte()

```
lte(<number1>, <number2>)
```

Returns 1 if \<number1\> is less than or equal to \<number2\>, and 0
otherwise.

## String Comparison

### comp()

```
comp(<string1>, <string2> [, <type>])
```

Performs lexicographic comparison of two strings. Returns -1 if
\<string1\> sorts before \<string2\>, 0 if they are equal, or 1 if
\<string1\> sorts after \<string2\>. The optional \<type\> argument
selects the comparison algorithm; both the default and the set of
accepted type codes are implementation-defined (see Chapter 20 for
per-engine codes). Default case-sensitivity therefore varies across
implementations: TinyMUX defaults to Unicode collation
(case-sensitive at the tertiary weight level), while PennMUSH defaults
to a case-sensitive byte-order comparison.

### streq()

```
streq(<string1>, <string2>)
```

Returns 1 if \<string1\> and \<string2\> are identical (case-insensitive),
and 0 otherwise. Level 2.

### strmatch()

```
strmatch(<string>, <pattern>)
```

Returns 1 if \<string\> matches \<pattern\> using wildcard matching (`*`
matches any sequence of characters, `?` matches any single character). The
match is case-insensitive and must cover the entire string.

### match()

```
match(<list>, <pattern> [, <delimiter>])
```

Returns the 1-based position of the first element in \<list\> that matches
\<pattern\> using wildcard matching, or 0 if no match is found. See also
Chapter 22 (List Functions).

## Lexicographic Comparison

### alphamax()

```
alphamax(<string1>, <string2>, ...)
```

Returns the argument that sorts last in alphabetical order. Accepts two or
more arguments.

### alphamin()

```
alphamin(<string1>, <string2>, ...)
```

Returns the argument that sorts first in alphabetical order. Accepts two or
more arguments.

## Conditional Functions

### ifelse()

```
ifelse(<condition>, <true-value>, <false-value>)
```

If \<condition\> is true, evaluates and returns \<true-value\>;
otherwise evaluates and returns \<false-value\>. Only the selected
branch is evaluated. `ifelse()` is the **portable** form, available
in all four reference engines.

### if()

```
if(<condition>, <true-value> [, <false-value>])
```

A shorter alias for `ifelse()`, with the third argument optional
(defaulting to an empty string). Available in PennMUSH and TinyMUX
only; **not** available in TinyMUSH or RhostMUSH. For maximum
portability, use `ifelse()` and pass an empty third argument when no
false branch is needed: `ifelse(<cond>, <true>,)`.

### switch()

```
switch(<expression>, <pattern1>, <result1> [, <pattern2>, <result2>, ...] [, <default>])
```

Evaluates \<expression\> and compares it against each \<pattern\> using
wildcard matching. Returns the \<result\> corresponding to the first matching
pattern. If no pattern matches and a \<default\> is provided (an odd final
argument), returns the default.

Within patterns, `#$` is replaced by the value of \<expression\>.

### case()

```
case(<expression>, <value1>, <result1> [, <value2>, <result2>, ...] [, <default>])
```

Like `switch()`, but uses exact string comparison instead of wildcard
matching. Level 2.

## Grep Functions

### grep()

```
grep(<object>, <pattern>, <search-string>)
```

Searches all attributes on \<object\> whose names match \<pattern\> for
\<search-string\>. Returns a space-separated list of attribute names
containing the string.

### grepi()

```
grepi(<object>, <pattern>, <search-string>)
```

Case-insensitive version of `grep()`.

## Implementation Notes

The short-circuit operators `cand()` and `cor()` are essential for safe
coding patterns. For example:

```
cand(hasattr(%0, DATA), gt(get(%0/DATA), 10))
```

Without short-circuit evaluation, `get(%0/DATA)` would be evaluated even
when the attribute does not exist, potentially causing errors.

Conforming implementations shall ensure that `if()`, `ifelse()`, `switch()`,
and `case()` evaluate only the selected branch. Unevaluated branches shall
not produce side effects.
