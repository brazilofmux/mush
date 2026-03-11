# Functions -- Overview and Calling Convention

## Overview

Functions are the computational building blocks of MUSHcode. A function
accepts zero or more string arguments, performs an operation, and returns a
string result. Functions are invoked within expressions using the syntax:

```
function_name(arg1, arg2, ..., argN)
```

This chapter specifies the general rules that govern all functions. The
specific functions available in a conforming implementation are cataloged in
Chapters 20 through 26.

## Function Invocation

### Syntax

A function call consists of a function name immediately followed (with no
intervening space) by an opening parenthesis, a comma-separated list of
arguments, and a closing parenthesis:

```
add(2, 3)
mid(Hello World, 0, 5)
u(me/MY_FUNC, arg1, arg2)
```

Function names are case-insensitive. `ADD(2,3)`, `add(2,3)`, and `Add(2,3)`
are all equivalent.

### Argument Parsing

Arguments are separated by commas at the same nesting depth. The following
nesting delimiters are respected:

- `[` and `]` -- Square brackets.
- `(` and `)` -- Parentheses (including nested function calls).
- `{` and `}` -- Braces.

A comma inside any of these delimiter pairs is not treated as an argument
separator:

```
add(mul(2, 3), 4)
```

This is parsed as two arguments: `mul(2, 3)` and `4`, not four arguments.

### Argument Evaluation

By default, each argument is evaluated (percent-codes expanded, functions
called) before being passed to the function. The function receives the
evaluated result strings.

Some functions suppress evaluation of certain arguments. These are called
**no-eval** arguments. The function receives the literal, unevaluated text
and evaluates it internally at the appropriate time. Functions with no-eval
arguments are documented as such.

Common functions with no-eval arguments include:

- `iter(<list>, <expression>, ...)` -- The \<expression\> argument is not
  evaluated initially; `iter()` evaluates it once for each element of the
  list, setting `##` (or `itext()`) to the current element.

- `switch(<value>, <pattern>, <result>, ...)` -- The \<result\> arguments
  are not evaluated initially; only the matching branch is evaluated.

- `u(<object/attr>, <args>...)` -- The attribute value is not passed as an
  argument; `u()` retrieves and evaluates the attribute separately.

### Whitespace in Arguments

Leading and trailing whitespace in arguments is significant by default.
However, many functions strip leading and trailing whitespace from their
arguments. Whether a specific function strips whitespace is noted in its
specification.

When space compression is active (the default in most evaluation contexts),
consecutive spaces within arguments are compressed to a single space.

## Return Values

Every function returns a string. Functions that conceptually return numbers
return the number as a string (e.g., `add(2, 3)` returns the string `5`).
Functions that conceptually return booleans return `1` for true and `0` for
false.

Functions that fail or encounter errors return one of:

| Return Value | Meaning |
|--------------|---------|
| (empty string) | No result, or an error in a context where empty is appropriate. |
| `#-1`        | Error indicator. Typically followed by a space and an error message in uppercase (e.g., `#-1 NO MATCH`). |
| `#-1 <MESSAGE>` | Specific error. The message describes the error condition. |
| `#-2`        | Ambiguous result. |

The specific error strings returned by each function are listed in the
function's specification. Softcode should test for errors by checking whether
the result begins with `#-1`.

## Argument Count

Each function specifies its expected number of arguments:

- **Fixed:** The function accepts exactly N arguments. Providing more or fewer
  arguments is an error.
- **Variable:** The function accepts a range of arguments (e.g., 1 to 3, or
  1 or more). Optional arguments have default values when omitted.
- **Unlimited:** The function accepts any number of arguments (e.g., `cat()`
  concatenates all its arguments).

When too few arguments are provided, missing arguments are treated as empty
strings (for most functions) or an error is returned. When too many arguments
are provided, extra arguments are typically ignored or an error is returned.
The exact behavior is specified per function.

## Side-Effect Functions

Most functions are **pure** -- they compute a result without modifying server
state. Some functions, called **side-effect functions**, modify the database
or server state as a side effect of being called.

Side-effect functions include:

| Function    | Side Effect |
|-------------|-------------|
| `set()`     | Sets a flag or attribute on an object. |
| `create()`  | Creates a new object. |
| `tel()`     | Teleports an object. |
| `pemit()`   | Sends a message to a player. |
| `remit()`   | Sends a message to a room. |
| `oemit()`   | Sends a message to a room, excluding one player. |
| `trigger()` | Triggers an attribute on an object. |
| `link()`    | Links an exit to a destination. |
| `parent()`  | Sets an object's parent. |
| `setq()`    | Sets a register value. |
| `setr()`    | Sets a register value (and returns it). |

**Security Note:** Side-effect functions are subject to the same permission
checks as their command equivalents. The `set()` function enforces the same
permissions as `@set`; the `tel()` function enforces the same permissions as
`@teleport`.

Some implementations require the SIDEFX flag on an object before side-effect
functions can be used by its attributes. Whether this restriction applies is
implementation-defined.

## The u() Function

The `u()` function is the primary mechanism for calling user-defined
functions (softcode subroutines). It deserves special attention due to its
central role in MUSHcode programming.

### Syntax

```
u(<object>/<attribute>, <arg0>, <arg1>, ..., <arg9>)
u(<attribute>, <arg0>, <arg1>, ..., <arg9>)
```

### Behavior

1. The attribute value is retrieved from the specified object (or from the
   executor if no object is specified).
2. The attribute value is evaluated as an expression, with:
   - `%0` through `%9` set to the provided arguments.
   - `%!` set to the object containing the attribute.
   - `%@` set to the object that called `u()`.
   - `%#` preserved from the calling context.
3. The result of evaluation is returned as the function's result.

### Example

```
&DOUBLE me = [mul(%0, 2)]

> think [u(me/DOUBLE, 7)]
14
```

### Scope and Side Effects

The `u()` function executes inline -- it does not create a queue entry. This
means:

- Registers (`%q0`-`%qz`) are shared with the calling context. Changes to
  registers in the called function are visible to the caller.
- Side-effect functions in the called code take effect immediately.
- The function invocation counter is incremented, contributing to the
  per-command limit.

## Function Permissions

Functions may be restricted by permission level:

| Level       | Who May Call |
|-------------|-------------|
| Any         | Any object. |
| Wizard      | Only wizards. |
| God         | Only God (`#1`). |
| Admin       | Wizards and royalty. |
| No-guest    | Any object except guests. |
| No-slave    | Any object except slaves. |

When a restricted function is called by an object without the required
permission, the function returns an error string (typically
`#-1 PERMISSION DENIED`).

## User-Defined Global Functions

Wizards may create global user-defined functions using the `@function`
command:

```
@function <name> = <object>/<attribute>
```

This registers a new function name that, when called, evaluates the specified
attribute on the specified object, passing the function arguments as `%0`
through `%9`. The function behaves identically to calling
`u(<object>/<attribute>, args...)` but with a custom function name.

### Example

```
@function double = #100/FN_DOUBLE

&FN_DOUBLE #100 = [mul(%0, 2)]

> think double(7)
14
```

Global functions require the GLOBAL_FUNCS power to register.

## Function Invocation Limits

To prevent runaway computation, the evaluator tracks two counters:

### Nesting Depth

Each function call increments the nesting depth counter. Nested calls (a
function calling another function via `u()`, brackets, or direct nesting)
increase the depth further. When the maximum depth is reached, additional
function calls return empty strings.

A conforming implementation shall support a nesting depth of at least 50.

### Invocation Count

Each function call increments a per-command invocation counter. This counter
is not reset between nested calls -- it accumulates across the entire
evaluation of a single command. When the maximum count is reached, additional
function calls return empty strings.

A conforming implementation shall support an invocation count of at least
2,500.

### Reporting

The `%?` substitution code returns the current nesting depth. Some
implementations provide a function (e.g., `invocation()`) to query the
current invocation count. These are useful for debugging performance issues
in complex softcode.

## Function Categories

The built-in functions specified by this standard are organized into the
following categories, each covered in a separate chapter:

| Category          | Chapter | Examples |
|-------------------|---------|----------|
| String functions  | 20      | `mid()`, `strlen()`, `ucstr()`, `cat()`, `edit()` |
| Math and logic    | 21      | `add()`, `sub()`, `mul()`, `div()`, `mod()`, `gt()` |
| List functions    | 22      | `iter()`, `map()`, `filter()`, `sort()`, `words()` |
| Object/database   | 23      | `name()`, `loc()`, `owner()`, `get()`, `type()` |
| Boolean/comparison | 24     | `and()`, `or()`, `not()`, `eq()`, `match()` |
| Side-effect       | 25      | `set()`, `create()`, `tel()`, `pemit()`, `trigger()` |
| Miscellaneous     | 26      | `time()`, `rand()`, `switch()`, `iter()`, `u()` |
