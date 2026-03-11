# Substitution and Percent-Codes

## Overview

Percent-codes are substitution sequences recognized by the expression
evaluator. When the evaluator encounters the `%` character, it reads the
following character(s) to determine which value to substitute. Percent-codes
provide quick access to context information, arguments, registers, and
formatting characters without requiring function calls.

## Formatting Codes

The following percent-codes produce literal characters useful for formatting:

| Code    | Produces | Description |
|---------|----------|-------------|
| `%r`    | newline  | A carriage return / line feed. Equivalent to a line break in output. |
| `%t`    | tab      | A horizontal tab character. |
| `%b`    | space    | A single space. Useful where a literal space might be compressed or stripped. |
| `%%`    | `%`      | A literal percent character. |
| `%\`    | `\`      | A literal backslash. |

The uppercase variants `%R`, `%T`, and `%B` are equivalent to their lowercase
forms.

## Enactor Information

These codes provide information about the enactor -- the player or object that
originally triggered the current chain of execution:

| Code    | Value | Description |
|---------|-------|-------------|
| `%#`    | dbref | The dbref of the enactor (e.g., `#42`). |
| `%n`    | name  | The name of the enactor. |
| `%N`    | Name  | The name of the enactor, with the first letter capitalized. |

### Pronoun Substitutions

These codes produce pronouns based on the enactor's SEX attribute:

| Code | Male   | Female  | Neuter | Plural  | Description |
|------|--------|---------|--------|---------|-------------|
| `%s` | he     | she     | it     | they    | Subjective pronoun. |
| `%S` | He     | She     | It     | They    | Subjective, capitalized. |
| `%o` | him    | her     | it     | them    | Objective pronoun. |
| `%O` | Him    | Her     | It     | Them    | Objective, capitalized. |
| `%p` | his    | her     | its    | their   | Possessive pronoun. |
| `%P` | His    | Her     | Its    | Their   | Possessive, capitalized. |
| `%a` | his    | hers    | its    | theirs  | Absolute possessive. |
| `%A` | His    | Hers    | Its    | Theirs  | Absolute possessive, capitalized. |

The server determines pronouns from the enactor's SEX attribute. If the SEX
attribute is not set, the neuter forms are used. The following SEX values
shall be recognized:

- **Male:** `male`, `m`, or any value beginning with `m`.
- **Female:** `female`, `f`, or any value beginning with `f`.
- **Neuter:** `neuter`, `n`, or any value beginning with `n`.
- **Plural:** `plural`, `p`, or any value beginning with `p`.

**Compatibility Note:** Some implementations support additional gender
options. The four listed above are the minimum required by this standard.

## Context Information

These codes provide information about the execution context:

| Code    | Value | Description |
|---------|-------|-------------|
| `%!`    | dbref | The dbref of the executor -- the object whose attribute is being evaluated. |
| `%@`    | dbref | The dbref of the caller -- the object that directly invoked the current function or trigger. In a chain of `u()` calls, this is the object containing the calling `u()`. |
| `%l`    | dbref | The dbref of the enactor's location. |
| `%?`    | number | The current function invocation depth. |
| `%+`    | number | The number of positional arguments passed to the current function. Level 2. |
| `%c`    | text  | The last command executed. Implementation-defined. |
| `%m`    | text  | The last command executed. Implementation-defined. |

### Understanding %!, %#, and %@

These three context codes are the most important and most commonly confused:

- **%#** (enactor) is the player who started the entire chain. It is preserved
  across `@trigger`, `u()`, and action list execution. It answers the
  question: "Who originally caused this to happen?"

- **%!** (executor) is the object whose code is currently running. It changes
  when `u()` calls code on a different object or when `@trigger` fires an
  attribute. It answers the question: "Whose code is running right now?"

- **%@** (caller) is the object that directly invoked the current code. In a
  chain `A — u(B/ATTR) — u(C/ATTR)`, when C's code runs: `%#` is A (the
  original enactor), `%!` is C (the executor), and `%@` is B (the caller).

Example:

```
Player #42 types: use gadget

Gadget #100 has:
  &AUSE = @trigger #200/DO_THING

Object #200 has:
  &DO_THING = think enactor=%# executor=%! caller=%@

Output: enactor=#42 executor=#200 caller=#100
```

## Positional Parameters

Positional parameters provide access to arguments passed by $-command pattern
matching, `@trigger`, or function calls:

| Code      | Value | Description |
|-----------|-------|-------------|
| `%0`      | arg 0 | The first argument (or first wildcard match). |
| `%1`      | arg 1 | The second argument. |
| `%2`      | arg 2 | The third argument. |
| ...       | ...   | ... |
| `%9`      | arg 9 | The tenth argument. |

A conforming implementation shall support at least 10 positional parameters
(`%0` through `%9`).

### How Arguments Are Populated

The source of positional parameter values depends on context:

- **$-commands:** Each `*` wildcard in the pattern captures a value. The
  first `*` capture is `%0`, the second is `%1`, and so on.

  ```
  &CMD me = $give * to *: @pemit %#=You give %0 to %1.
  > give sword to Bob
  You give sword to Bob.
  ```

- **@trigger:** Arguments after the `=` are comma-separated and assigned to
  `%0` through `%9`.

  ```
  @trigger me/DO_IT = apple, banana, cherry
  ```

  `%0` is `apple`, `%1` is `banana`, `%2` is `cherry`.

- **u() function calls:** Arguments after the attribute name are assigned to
  `%0` through `%9`.

  ```
  think [u(me/FORMAT, hello, world)]
  ```

  Inside FORMAT, `%0` is `hello` and `%1` is `world`.

## Registers

Registers are temporary storage slots that persist across commands within the
same action list or evaluation chain. They are the primary mechanism for
passing intermediate values between expressions.

### Numbered Registers

| Code      | Register | Description |
|-----------|----------|-------------|
| `%q0`     | r(0)     | Register 0. |
| `%q1`     | r(1)     | Register 1. |
| ...       | ...      | ... |
| `%q9`     | r(9)     | Register 9. |

### Named Registers

| Code      | Register | Description |
|-----------|----------|-------------|
| `%qa`     | r(a)     | Register a. |
| `%qb`     | r(b)     | Register b. |
| ...       | ...      | ... |
| `%qz`     | r(z)     | Register z. |

A conforming implementation shall support at least 36 registers: 10 numbered
(`%q0` through `%q9`) and 26 named (`%qa` through `%qz`).

### Setting Registers

Registers are set using the `setq()` and `setr()` functions:

- `setq(<register>, <value>)` -- Sets the register and returns an empty
  string.
- `setr(<register>, <value>)` -- Sets the register and returns the value.

The `r()` function retrieves a register value: `r(0)` is equivalent to `%q0`.

Example:

```
> think [setq(0, Hello)][setq(1, World)]%q0, %q1!
Hello, World!
```

### Register Scope

Registers are scoped to the current queue entry (action list execution).
They persist across commands within a single action list separated by
semicolons, and across `u()` calls within the same queue entry:

```
&TEST me = [setq(0, saved)] ; think %q0
```

Outputs: `saved`

Registers are **not** preserved across `@trigger` or `@wait` boundaries
by default. Each new queue entry starts with empty registers, except that
`@trigger` and `@wait` capture the current register values at the time they
are called.

**Compatibility Note:** Register preservation across `@trigger` varies by
implementation. TinyMUSH and TinyMUX preserve registers. PennMUSH provides
the `@trigger/spoof` and `@trigger/inline` switches for different scoping.
This standard specifies that registers are captured at queue entry creation
time.

## Attribute Shortcut Substitutions

| Code        | Value | Description |
|-------------|-------|-------------|
| `%va`-`%vz` | attribute value | Equivalent to `v(VA)` through `v(VZ)`. Returns the value of the named shortcut attribute on the executor (`%!`). |

Example:

```
&VA me = Hello World
> think %va
Hello World
```

## Iteration Substitutions (Level 2)

These codes provide access to iteration context in `iter()`, `@dolist`, and
similar constructs:

| Code      | Value | Description |
|-----------|-------|-------------|
| `%i0`     | text  | The current iteration value at nesting level 0 (innermost). Equivalent to `itext(0)`. |
| `%i1`     | text  | The current iteration value at nesting level 1 (next outer). |
| `%i<n>`   | text  | The current iteration value at nesting level \<n\>. |

## ANSI Color Codes (Level 2)

Some implementations support ANSI color substitutions:

| Code        | Value | Description |
|-------------|-------|-------------|
| `%xn`       | ANSI  | Normal (reset). |
| `%xh`       | ANSI  | Hilite (bold). |
| `%xu`       | ANSI  | Underline. |
| `%xi`       | ANSI  | Inverse. |
| `%xf`       | ANSI  | Flash (blink). |
| `%xr`       | ANSI  | Red foreground. |
| `%xg`       | ANSI  | Green foreground. |
| `%xb`       | ANSI  | Blue foreground. |
| `%xy`       | ANSI  | Yellow foreground. |
| `%xm`       | ANSI  | Magenta foreground. |
| `%xc`       | ANSI  | Cyan foreground. |
| `%xw`       | ANSI  | White foreground. |
| `%xx`       | ANSI  | Black foreground. |
| `%xR`       | ANSI  | Red background. |
| `%xG`       | ANSI  | Green background. |
| (etc.)      | ANSI  | Uppercase for background colors. |

The exact set of supported ANSI codes and the syntax for extended color
(256-color, 24-bit) is implementation-defined. ANSI support is a Level 2
feature.

## Substitution Processing Order

When the evaluator encounters `%`, it reads the next character to determine
the substitution type:

1. If the next character is a digit (`0`-`9`), it is a positional parameter.
2. If the next character is `q` followed by a digit or letter, it is a
   register.
3. If the next character is `v` followed by a letter (`a`-`z`), it is an
   attribute shortcut.
4. If the next character is `x` followed by a color code letter, it is an
   ANSI code.
5. Otherwise, the single character determines the substitution (e.g., `%n`,
   `%#`, `%r`, `%b`).

Unknown percent-codes shall be passed through literally (the `%` and
following character are both output).
