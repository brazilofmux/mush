# Miscellaneous Functions

## Overview

This chapter covers functions that do not fit neatly into the preceding
categories: time and date functions, type validation, server information,
control flow functions, and utility functions.

## Time and Date

### time()

```
time()
```

Returns the current time as a human-readable string in the server's local
time zone. The format is implementation-defined but typically resembles
`Tue Mar 11 14:30:00 2026`.

### secs()

```
secs()
```

Returns the current time as a Unix timestamp (seconds since
January 1, 1970 00:00:00 UTC).

### convsecs()

```
convsecs(<seconds>)
```

Converts a Unix timestamp to a human-readable time string.

### convtime()

```
convtime(<time-string>)
```

Converts a human-readable time string to a Unix timestamp. Returns -1 if the
string cannot be parsed.

### timefmt()

```
timefmt(<format> [, <seconds>])
```

Formats a time value according to the \<format\> string, using `strftime()`
conventions. If \<seconds\> is omitted, the current time is used.

Common format specifiers:

| Specifier | Description |
|-----------|-------------|
| `%Y`      | Four-digit year |
| `%m`      | Two-digit month (01-12) |
| `%d`      | Two-digit day (01-31) |
| `%H`      | Hour in 24-hour format (00-23) |
| `%M`      | Minute (00-59) |
| `%S`      | Second (00-59) |
| `%A`      | Full weekday name |
| `%B`      | Full month name |
| `%Z`      | Time zone abbreviation |
| `%s`      | Unix timestamp |

### starttime()

```
starttime()
```

Returns the Unix timestamp of when the server was last started.

### uptime()

```
uptime()
```

Returns the number of seconds the server has been running since its last
restart. Level 2.

## Server Information

### version()

```
version()
```

Returns a string identifying the server software and version.

### mudname()

```
mudname()
```

Returns the configured name of the MUSH.

### ports()

```
ports()
```

Returns information about the ports on which the server is listening. The
format is implementation-defined. Level 2.

### config()

```
config(<parameter>)
```

Returns the value of a server configuration parameter. The set of queryable
parameters is implementation-defined. Level 2.

## Type Validation

The type testing functions (`isnum()`, `isint()`, `isdbref()`, `isobjid()`,
`isword()`) are specified in Chapter 24, "Boolean and Comparison Functions."

### valid()

```
valid(<category>, <string>)
```

Returns 1 if \<string\> is valid for the specified \<category\>, and 0
otherwise. Common categories include `attrname`, `objectname`, `playername`,
and `password`. The set of categories is implementation-defined.

## Control Flow

### switch()

```
switch(<expression>, <pattern1>, <result1>, ... [, <default>])
```

Compares \<expression\> against each pattern using wildcard matching and
returns the result for the first match. See Chapter 24 for the full
specification.

### case()

```
case(<expression>, <value1>, <result1>, ... [, <default>])
```

Like `switch()` but uses exact comparison instead of wildcard matching.
Level 2.

### if() / ifelse()

```
if(<condition>, <true-value> [, <false-value>])
```

Evaluates and returns the appropriate branch based on the condition. See
Chapter 24 for the full specification.

### while()

`while()` exists in three of the four reference engines, but with
**incompatible signatures**. There is no portable form; choose the
form that matches your target engine.

**TinyMUX 2.14:**

```
while(<eval-attr>, <cond-attr>, <list>, <compval> [, <isep> [, <osep>]])
```

Iterates over \<list\>. For each element, evaluates \<eval-attr\>
with the element as `%0` and appends the result to the output. After
each element it evaluates \<cond-attr\>; iteration stops when the
result string-equals \<compval\>. The list is split by \<isep\>
(default space) and the output joined with \<osep\>.

**TinyMUSH / RhostMUSH:**

```
while(<condition-function>, <body-function>, <initial-value> [, <limit>])
```

Repeatedly evaluates \<body-function\> as long as
\<condition-function\> returns true; the result of each iteration is
passed to the next as `%0`. The optional \<limit\> caps the number
of iterations (default implementation-defined).

**PennMUSH:** does not provide `while()`.

In all engines the iteration cap and the function-invocation budget
described in Chapter 12 still apply. For portable code, prefer
`@dolist` or recursive `u()` over `while()`. Level 2.

### foreach()

```
foreach(<function>, <string> [, <begin>, <end>])
```

Applies \<function\> to each character of \<string\> in turn. The
current character is passed to \<function\> as `%0`. The optional
\<begin\> and \<end\> arguments are single characters that mark the
boundaries of a region within \<string\> for selective processing:
characters outside a matching \<begin\>/\<end\> pair are passed
through unchanged. The third and fourth arguments are *not* list
delimiters — `foreach()` operates on characters, not on delimited
list elements. Level 2.

## Null and Utility

### null()

```
null(<expression>)
```

Evaluates \<expression\> and discards the result, returning an empty string.
This is used to call side-effect functions without displaying their return
values.

### objeval()

```
objeval(<object>, <expression>)
```

Evaluates \<expression\> as though \<object\> were the executor. See
Chapter 23 for details.

### squish()

```
squish(<string> [, <character>])
```

Collapses runs of \<character\> (default: space) into single instances.

### translate()

```
translate(<string>, <type>)
```

Translates special characters in \<string\>. The \<type\> parameter controls
the translation. Level 2.

## WHO and Connection Functions

### lwho()

```
lwho()
```

Returns a space-separated list of dbrefs of all connected players. DARK
players are included if the caller is a wizard.

### mwho()

```
mwho()
```

Returns a space-separated list of dbrefs of connected players who are not
DARK. Level 2.

### nwho()

```
nwho()
```

Returns the number of currently connected players.

### conn()

```
conn(<player>)
```

Returns the number of seconds \<player\> has been connected. Returns -1 if
not connected.

### idle()

```
idle(<player>)
```

Returns the number of seconds since \<player\> last issued a command. Returns
-1 if not connected.

### doing()

```
doing(<player>)
```

Returns \<player\>'s DOING string from the WHO list.

### poll()

```
poll()
```

Returns the current poll question displayed in the WHO header. Level 2.

## Debugging

### think()

Note: `think` is a command, not a function. It evaluates its argument and
displays the result only to the executor. It is the primary debugging tool
for MUSHcode development.

### trace()

Setting the TRACE flag on an object causes all function evaluations on that
object to produce verbose debugging output showing each function call, its
arguments, and its return value. The output is sent only to the object's
owner.

## Implementation Notes

Time functions depend on the server's system clock and time zone
configuration. Conforming implementations shall support at minimum the
`time()`, `secs()`, `convsecs()`, `convtime()`, and `timefmt()` functions.

The `while()` function shall enforce an iteration limit to prevent infinite
loops. The default limit is implementation-defined but shall not exceed
10,000 iterations without explicit configuration.

The set of parameters queryable through `config()` varies by implementation.
Conforming implementations should document their supported parameters.
