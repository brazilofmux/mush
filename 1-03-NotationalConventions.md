# Notational Conventions

## Syntax Notation

This standard uses a modified BNF (Backus-Naur Form) to describe the syntax of
commands, functions, and expressions. The following conventions apply:

### Terminal and Non-Terminal Symbols

- **`monospaced text`** -- Literal characters that shall appear exactly as
  shown. For example, `@dig` means the four characters `@`, `d`, `i`, `g`.

- **\<angle brackets\>** -- A non-terminal symbol representing a class of
  values. For example, \<name\> represents any valid object name.

- **UPPERCASE** -- A keyword that shall be typed as shown, though matching is
  case-insensitive unless otherwise specified. For example, `WHO` matches
  `who`, `Who`, and `WHO`.

### Grouping and Repetition

- **[ ]** -- Optional elements. The enclosed elements may be present or absent.
  For example, `@dig <name> [= <exit-list>]` means the `= <exit-list>` portion
  is optional.

- **{ }** -- Grouping. The enclosed elements are treated as a unit.
  For example, `{, <arg>}` means a comma followed by an argument.

- **...** -- Repetition. The preceding element may be repeated zero or more
  times. For example, `<arg>{, <arg>}...` means one or more comma-separated
  arguments.

- **|** -- Alternation. Exactly one of the separated alternatives shall be
  chosen. For example, `<room> | <thing>` means either a room or a thing.

### Common Non-Terminals

The following non-terminal symbols are used throughout this standard:

```
<dbref>         ::= "#" <integer>
<integer>       ::= ["-"] <digit> {<digit>}...
<digit>         ::= "0" | "1" | "2" | "3" | "4" | "5"
                   | "6" | "7" | "8" | "9"
<name>          ::= <printable-char> {<printable-char>}...
<attr-name>     ::= <letter> {<letter> | <digit> | "_" | "-"
                   | "." | "'" | "`"}...
<pattern>       ::= any string, possibly containing wildcard characters
<command-list>  ::= <command> {";" <command>}...
<command>       ::= any valid MUSH command
<expression>    ::= any valid MUSHcode expression
<boolean>       ::= "0" | "1"
<object>        ::= <dbref> | <name> | "me" | "here"
<flag-name>     ::= <letter> {<letter> | <digit> | "_"}...
<player-name>   ::= "*" <name>
<switch>        ::= "/" <word>
```

## Command Syntax

Built-in commands are described using the following format:

```
@command[/<switch>]... <arguments>
```

Where:

- **@command** is the command name. Commands beginning with `@` are traditional
  MUSH builder and administrative commands. Commands without `@` are short-form
  commands used in everyday interaction (e.g., `say`, `pose`, `look`).

- **/\<switch\>** is an optional modifier that alters the command's behavior.
  Multiple switches may be combined. For example, `@set/quiet` applies the
  `/quiet` switch to the `@set` command.

- **\<arguments\>** are the command's arguments, whose syntax varies by
  command. Arguments separated by `=` typically have a left-hand side (target)
  and a right-hand side (value). For example: `@desc me = A tall figure.`

### Argument Conventions

In command descriptions:

- A `,` in the argument list indicates that the arguments are separated by
  commas.
- A `=` in the argument list separates the target from the value.
- A `/` after an object reference introduces an attribute name. For example,
  `<object>/<attribute>` means an object followed by a slash and an attribute
  name.
- Whitespace around `=` and `,` delimiters is stripped unless otherwise noted.

## Function Syntax

Built-in functions are described using the following format:

```
function(<arg1>, <arg2>, ..., <argN>)
```

Where:

- **function** is the function name, matched case-insensitively.
- Arguments are separated by commas.
- Arguments enclosed in **[ ]** are optional and may be omitted.
- Arguments followed by **...** indicate that additional arguments of the same
  type may be provided.

Each function description specifies:

- **Arguments:** The number, type, and meaning of each argument.
- **Returns:** The string value returned by the function.
- **Side effects:** Any changes to server state caused by the function, if
  applicable.
- **Errors:** Error conditions and the values returned when they occur.
- **Level:** Whether the function is Level 1 (Core) or Level 2 (Extended).

## Attribute Notation

Attributes are referenced in this standard using the notation:

```
<object>/<attribute-name>
```

For example, `#42/DESC` refers to the DESC attribute on object `#42`.

When describing the content of attributes, the following conventions apply:

- **$-command format:** `$<pattern>:<action-list>`
- **^-listen format:** `^<pattern>:<action-list>`
- **Message attributes:** Plain text, possibly containing substitutions.
- **Action list attributes:** A semicolon-separated list of commands.

## Examples

Throughout this standard, examples are presented in fenced code blocks. Input
typed by a user is shown prefixed with `>`. Output produced by the server is
shown without a prefix.

Example:

```
> say Hello, world!
You say, "Hello, world!"
```

In this example, `> say Hello, world!` is user input and
`You say, "Hello, world!"` is server output.

When illustrating MUSHcode evaluation, the notation `=>` indicates the result
of evaluating an expression:

```
> think add(2, 3)
5
```

## Cross-References

References to other chapters and sections within this standard use the form
"see Chapter N" or "see Section N.M." References to specific requirements use
the requirement identifiers defined in Chapter 34.

## Implementation Notes

Paragraphs marked **Implementation Note** provide non-normative guidance to
implementors. These notes explain rationale, suggest implementation strategies,
or highlight common pitfalls. They do not impose requirements.

## Compatibility Notes

Paragraphs marked **Compatibility Note** document areas where existing
implementations diverge from each other or from this standard. These notes
help implementors and users understand the practical implications of
standardization.
