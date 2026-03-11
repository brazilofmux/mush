# String Manipulation

## Why Strings Matter

Since everything in MUSHcode is a string, string manipulation is the most
fundamental skill. Whether you are formatting output, parsing player input,
building messages, or processing data, you are working with strings.

## Basic String Functions

### Length

```
> think strlen(Hello World)
11
```

### Extracting Parts

```
> think mid(Hello World, 0, 5)
Hello
> think left(Hello World, 5)
Hello
> think right(Hello World, 5)
World
```

`mid()` takes a start position (0-based) and a length. `left()` takes
characters from the beginning. `right()` takes characters from the end.

### Finding Text

```
> think pos(World, Hello World)
7
```

Returns the 1-based position of the first occurrence.

### Concatenation

```
> think cat(Hello, World)
Hello World
> think strcat(Hello, World)
HelloWorld
```

`cat()` joins with spaces. `strcat()` joins with nothing.

## Case Conversion

```
> think ucstr(hello world)
HELLO WORLD
> think lcstr(HELLO WORLD)
hello world
> think capstr(hello world)
Hello world
```

## Search and Replace

### edit()

```
> think edit(The quick brown fox, brown, red)
The quick red fox
```

Replaces all occurrences of the search string with the replacement.
Multiple pairs can be chained:

```
> think edit(Hello World, Hello, Goodbye, World, Planet)
Goodbye Planet
```

### tr()

Character-by-character translation:

```
> think tr(Hello, Helo, HELO)
HELLO
```

Each character in the first set is replaced by the corresponding character
in the second set.

## Padding and Alignment

### ljust(), rjust(), center()

```
> think [ljust(Name, 15)]Score
Name           Score
> think [rjust(42, 10)]
        42
> think [center(Title, 20)]
       Title
```

These are essential for building tables and formatted output.

### space() and repeat()

```
> think A[space(5)]B
A     B
> think repeat(=-,20)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
```

## Trimming and Squishing

### trim()

```
> think trim(  Hello World  )
Hello World
```

Removes leading and trailing spaces. You can trim other characters:

```
> think trim(***Hello***, b, *)
Hello
```

### squish()

```
> think squish(Hello    World)
Hello World
```

Collapses runs of multiple spaces into single spaces.

## Pattern Matching

### strmatch()

```
> think strmatch(Hello World, Hello*)
1
> think strmatch(Hello World, *llo*rld)
1
> think strmatch(Hello World, Goodbye*)
0
```

Wildcards: `*` matches any sequence; `?` matches any single character.

### Regular Expressions

For complex patterns, use `regmatch()`:

```
> think regmatch(Error 404, Error (\d+))
1
```

With register capture:

```
> think [regmatch(Error 404, Error (\d+), 0 1)]Code: [r(1)]
Code: 404
```

And `regeditall()` for regex-based replacement:

```
> think regeditall(Hello World, [aeiou], *)
H*ll* W*rld
```

## Formatting Output

### Building a Table

```
> &FN_ROW me = [ljust(%0, 15)][rjust(%1, 8)]
> think [u(me/FN_ROW, Name, Score)]%r
  [u(me/FN_ROW, Alice, 150)]%r
  [u(me/FN_ROW, Bob, 89)]%r
  [u(me/FN_ROW, Carol, 220)]
Name              Score
Alice               150
Bob                  89
Carol               220
```

### ANSI Color

```
> think ansi(hr, Warning!) Normal text.
```

The `h` means highlight (bold), `r` means red. The result is "Warning!" in
bright red followed by normal text.

Common color codes: `r` red, `g` green, `y` yellow, `b` blue, `m` magenta,
`c` cyan, `w` white. Uppercase for bright, lowercase for dim.

## Escaping and Security

When incorporating player input into code, always escape it:

```
> &CMD_ECHO me = $echo *:@pemit %# = You said: [secure(%0)]
```

The `secure()` function strips characters that could be interpreted as code
(`%`, `[`, `]`, `{`, `}`, `,`, `;`). Without it, a malicious player could
inject MUSHcode into your object.

The `escape()` function is less aggressive -- it prefixes special characters
with `%` instead of removing them.

**Rule of thumb:** Use `secure()` for untrusted input. Use `escape()` when
you want to preserve the text but prevent evaluation.

## Practical Example: A Name Formatter

```
> &FN_FANCY_NAME me = [ansi(hc, capstr(lcstr(%0)))]
> think u(me/FN_FANCY_NAME, jOHN sMITH)
John smith
```

## Quick Reference

| Function | What It Does |
|----------|-------------|
| `strlen(str)` | Length of string. |
| `mid(str, start, len)` | Extract substring. |
| `left(str, len)` | Left N characters. |
| `right(str, len)` | Right N characters. |
| `pos(sub, str)` | Find position of substring. |
| `cat(a, b, ...)` | Join with spaces. |
| `strcat(a, b, ...)` | Join with nothing. |
| `ucstr(str)` | Uppercase. |
| `lcstr(str)` | Lowercase. |
| `capstr(str)` | Capitalize first letter. |
| `edit(str, old, new)` | Search and replace. |
| `ljust(str, width)` | Left-justify. |
| `rjust(str, width)` | Right-justify. |
| `center(str, width)` | Center. |
| `trim(str)` | Remove leading/trailing whitespace. |
| `squish(str)` | Collapse multiple spaces. |
| `ansi(code, str)` | Apply color. |
| `secure(str)` | Strip dangerous characters. |
