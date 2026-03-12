# Expression Evaluation

## Overview

The expression evaluator is the core of the MUSHcode programming language. It
transforms a string containing literal text, function calls, and substitution
codes into a result string. Every attribute value that is "executed" -- action
lists, \$-command responses, function arguments -- passes through the expression
evaluator.

Understanding the evaluator is essential for writing correct MUSHcode. This
chapter specifies the evaluation algorithm, the special characters it
recognizes, and the rules governing their interaction.

## The Evaluation Algorithm

The evaluator scans the input string character by character, copying literal
text to the output buffer and processing special characters as they are
encountered. The special characters are:

| Character | Meaning |
|-----------|---------|
| `%`       | Begins a substitution code (see Chapter 13). |
| `[`       | Begins a function call or inline evaluation. |
| `]`       | Ends a function call or inline evaluation. |
| `{`       | Begins a brace-delimited group (suppresses evaluation). |
| `}`       | Ends a brace-delimited group. |
| `(`       | Begins a function argument list (after a function name). |
| `)`       | Ends a function argument list. |
| `,`       | Separates function arguments. |
| `\`       | Escape character; the following character is treated literally. |
| `;`       | Command separator in action lists. |

### Processing Rules

The evaluator applies the following rules in order of priority:

1. **Escape sequences:** When `\` is encountered, the next character is
   copied to the output literally, regardless of whether it is a special
   character. The backslash itself is consumed. `\\` produces a literal `\`.

2. **Percent substitutions:** When `%` is encountered, the evaluator reads
   the following character(s) to determine the substitution code and replaces
   the sequence with the appropriate value (see Chapter 13).

3. **Square brackets:** When `[` is encountered, the evaluator recursively
   evaluates the text between `[` and the matching `]`, then replaces the
   entire bracketed expression (including the brackets) with the result. This
   is the primary mechanism for calling functions inline:

   ```
   > think The answer is [add(2, 3)].
   The answer is 5.
   ```

4. **Braces:** When `{` is encountered, the evaluator copies the text between
   `{` and the matching `}` to the output **without evaluation**. The braces
   themselves are stripped (in most contexts). Braces are used to protect text
   from evaluation:

   ```
   > think {[add(2, 3)]}
   [add(2, 3)]
   ```

5. **Function calls:** When the evaluator encounters a word immediately
   followed by `(`, it checks whether the word is a known function name. If
   so, it parses the argument list (comma-separated, respecting nesting),
   evaluates each argument, calls the function, and replaces the entire
   expression with the function's return value.

6. **Literal text:** Characters that are not special are copied to the output
   unchanged.

### Nesting and Recursion

The evaluator is recursive. Function arguments, bracketed expressions, and
substitution codes may themselves contain special characters that trigger
further evaluation. For example:

```
> think [add([mul(2, 3)], [sub(10, 5)])]
11
```

The inner `mul(2, 3)` and `sub(10, 5)` are evaluated first, producing `6`
and `5`, which become the arguments to `add(6, 5)`, producing `11`.

The maximum recursion depth is limited to prevent infinite loops (see Chapter
11, "Execution Limits"). A conforming implementation shall support a function
nesting depth of at least 50.

### Space Compression

By default, the evaluator compresses consecutive spaces in the output to a
single space. This behavior can be suppressed by the calling context (some
functions preserve spaces in their arguments).

**Compatibility Note:** Space compression behavior varies across
implementations and contexts. TinyMUSH compresses spaces by default in most
contexts. PennMUSH provides finer-grained control. Softcode that depends on
multiple consecutive spaces should use explicit space-generating functions
or substitutions.

## Evaluation Contexts

Not all text is evaluated in the same way. The evaluator's behavior is
controlled by **evaluation flags** that specify which features are active.
The following flags are significant:

| Flag              | Effect |
|-------------------|--------|
| Evaluate          | Enable function calls, substitutions, and bracket processing. When off, the string is treated as literal text. |
| Strip braces      | Remove the outer pair of braces from the result, if present. |
| No compress       | Disable space compression. |
| Function check    | Report an error if a word followed by `(` is not a recognized function name. |

Different commands and functions set different evaluation flags on their
arguments. For example:

- `think` evaluates its argument with all features enabled.
- `@switch` evaluates the expression being tested, but does not evaluate
  the branch bodies until one is selected.
- Functions with "no-eval" arguments (like `iter()`) receive certain
  arguments unevaluated and evaluate them internally.

## The think Command

The `think` command is the primary tool for testing expressions. It evaluates
its argument and displays the result to the player:

```
> think Hello, %n! The time is [time()].
Hello, Bob! The time is Wed Mar 11 09:42:00 2026.
```

`think` sends output only to the executing player; other players do not see
it. It is functionally equivalent to `@pemit %# = <expression>` but more
convenient for interactive use and debugging.

## Common Evaluation Patterns

### Inline Evaluation

Square brackets evaluate their contents and insert the result:

```
> say I have [money(%#)] coins.
You say, "I have 150 coins."
```

### Nested Function Calls

Functions can be nested to arbitrary depth (within the recursion limit):

```
> think [ucstr(left(Hello World, 5))]
HELLO
```

### Conditional Evaluation with Braces

Braces protect text from premature evaluation. This is critical in control
flow constructs:

```
> @switch color = red, {say It is red!}, blue, {say It is blue!}
```

Without braces, both `say` commands would be evaluated (triggering side
effects) before `@switch` selects a branch.

### Escaping Special Characters

The backslash escapes the character that follows it:

```
> think 100\% complete
100% complete
> think brackets: \[not evaluated\]
brackets: [not evaluated]
```

To produce a literal backslash:

```
> think path\\to\\file
path\to\file
```

## Evaluation Order

Within a single expression, evaluation proceeds strictly left to right. There
is no operator precedence among the special characters; they are processed in
the order they are encountered during the left-to-right scan.

This has important implications for side-effect functions:

```
> think [setq(0, hello)] - %q0
 - hello
```

In this example, `setq(0, hello)` is evaluated first (returning an empty
string), then `%q0` is evaluated, finding the value `hello` that was just
set. If the order were reversed, `%q0` would be empty.

## Error Handling

The evaluator does not produce exceptions or halt on errors. Instead, error
conditions produce specific string results:

| Condition | Result |
|-----------|--------|
| Unknown function name | The text is passed through literally (with parentheses), or an error message is returned, depending on evaluation flags. |
| Too many function arguments | Implementation-defined; typically the extra arguments are ignored or an error string is returned. |
| Too few function arguments | Implementation-defined; missing arguments are treated as empty strings or an error is returned. |
| Recursion depth exceeded | Function calls return empty strings. |
| Function invocation limit exceeded | Function calls return empty strings. |

A conforming implementation should not crash, hang, or corrupt state on any
input to the evaluator, no matter how malformed.
