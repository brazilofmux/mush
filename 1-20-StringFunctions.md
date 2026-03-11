# String Functions

## Overview

String functions manipulate text values: extracting substrings, changing case,
searching for patterns, formatting output, and transforming characters. These
functions form the backbone of text processing in MUSHcode.

All string functions follow the calling conventions described in Chapter 14.
Positions are 0-based for character functions unless otherwise noted.

## Extraction and Substrings

### mid()

```
mid(<string>, <start>, <length>)
```

Returns a substring of \<string\> beginning at character position \<start\>
(0-based) and extending for \<length\> characters. If \<start\> is beyond the
end of the string, returns an empty string. If \<length\> extends beyond the
end, returns characters through the end of the string.

### left()

```
left(<string>, <length>)
```

Returns the leftmost \<length\> characters of \<string\>. Equivalent to
`mid(<string>, 0, <length>)`.

### right()

```
right(<string>, <length>)
```

Returns the rightmost \<length\> characters of \<string\>.

### strlen()

```
strlen(<string>)
```

Returns the number of characters in \<string\>. ANSI color codes are not
counted.

### delete()

```
delete(<string>, <start>, <length>)
```

Returns \<string\> with \<length\> characters removed beginning at position
\<start\> (0-based).

## Concatenation

### cat()

```
cat(<string1>, <string2>, ...)
```

Concatenates all arguments, separated by spaces. Accepts a variable number
of arguments.

### strcat()

```
strcat(<string1>, <string2>, ...)
```

Concatenates all arguments with no separator. Accepts a variable number of
arguments.

### join()

```
join(<delimiter>, <string1>, <string2>, ...)
```

Concatenates all arguments after the first, separated by \<delimiter\>. Level 2.

## Case Conversion

### capstr()

```
capstr(<string>)
```

Returns \<string\> with the first character capitalized.

### lcstr()

```
lcstr(<string>)
```

Returns \<string\> converted entirely to lowercase.

### ucstr()

```
ucstr(<string>)
```

Returns \<string\> converted entirely to uppercase.

## Searching and Position

### pos()

```
pos(<substring>, <string>)
```

Returns the 1-based position of the first occurrence of \<substring\> in
\<string\>. Returns `#-1` if \<substring\> is not found. The search is
case-sensitive.

### lpos()

```
lpos(<substring>, <string>)
```

Returns the 1-based position of the last occurrence of \<substring\> in
\<string\>. Returns `#-1` if not found. Level 2.

### strmatch()

```
strmatch(<string>, <pattern>)
```

Returns 1 if \<string\> matches \<pattern\> using wildcard matching (`*` and
`?`), and 0 otherwise. The match is case-insensitive and must match the
entire string.

## Regular Expressions

### regmatch()

```
regmatch(<string>, <regexp> [, <register-list>])
```

Returns 1 if \<string\> matches the regular expression \<regexp\>, and 0
otherwise. The match is case-sensitive. If \<register-list\> is provided, it
specifies a space-separated list of register names to store captured
subexpressions (0 for the entire match, 1-9 for subgroups).

### regmatchi()

```
regmatchi(<string>, <regexp> [, <register-list>])
```

Case-insensitive version of `regmatch()`.

### regedit()

```
regedit(<string>, <regexp>, <replacement>)
```

Replaces the first occurrence of \<regexp\> in \<string\> with \<replacement\>.
Case-sensitive. In the replacement string, `$0` refers to the entire match and
`$1` through `$9` refer to captured subgroups.

### regeditall()

```
regeditall(<string>, <regexp>, <replacement>)
```

Replaces all occurrences of \<regexp\> in \<string\> with \<replacement\>.
Case-sensitive.

### regediti()

```
regediti(<string>, <regexp>, <replacement>)
```

Case-insensitive version of `regedit()`.

### regeditalli()

```
regeditalli(<string>, <regexp>, <replacement>)
```

Case-insensitive version of `regeditall()`.

## Editing and Transformation

### edit()

```
edit(<string>, <from>, <to> [, <from2>, <to2>, ...])
```

Performs literal string replacement on \<string\>, replacing all occurrences of
\<from\> with \<to\>. Multiple find/replace pairs may be specified and are
applied in order.

### tr()

```
tr(<string>, <from-chars>, <to-chars>)
```

Performs character-by-character translation. Each character in \<from-chars\> is
replaced by the corresponding character in \<to-chars\>. If \<to-chars\> is
shorter than \<from-chars\>, the last character in \<to-chars\> is used for
remaining translations.

### reverse()

```
reverse(<string>)
```

Returns \<string\> with its characters in reverse order.

### scramble()

```
scramble(<string>)
```

Returns \<string\> with its characters in random order.

### merge()

```
merge(<string1>, <string2>, <char>)
```

Merges two strings by replacing each occurrence of \<char\> in \<string1\> with
the character at the corresponding position in \<string2\>.

## Padding and Justification

### ljust()

```
ljust(<string>, <width> [, <fill-char>])
```

Left-justifies \<string\> within a field of \<width\> characters. If the string
is shorter than \<width\>, the remaining space is filled with \<fill-char\>
(default: space). If the string is longer, it is not truncated.

### rjust()

```
rjust(<string>, <width> [, <fill-char>])
```

Right-justifies \<string\> within a field of \<width\> characters.

### center()

```
center(<string>, <width> [, <fill-char>])
```

Centers \<string\> within a field of \<width\> characters.

### space()

```
space(<count>)
```

Returns a string of \<count\> space characters.

### repeat()

```
repeat(<string>, <count>)
```

Returns \<string\> repeated \<count\> times.

## Whitespace

### trim()

```
trim(<string> [, <trim-style> [, <trim-char>]])
```

Removes leading and/or trailing characters from \<string\>. The \<trim-style\>
parameter specifies which end to trim: `b` for both (default), `l` for left
only, `r` for right only. The \<trim-char\> parameter specifies the character
to trim (default: space).

### squish()

```
squish(<string>)
```

Returns \<string\> with all runs of multiple spaces collapsed to a single
space, and leading/trailing spaces removed.

## Escaping and Security

### escape()

```
escape(<string>)
```

Prefixes the special characters `%`, `[`, `]`, `{`, `}`, `,`, `;`, `\`,
and `(` with `%` to prevent the evaluator from interpreting them.

### secure()

```
secure(<string>)
```

Removes the characters `%`, `[`, `]`, `{`, `}`, `,`, `;`, `\`, and `(`
from \<string\>. This is more aggressive than `escape()` and is used when
untrusted input must be embedded in expressions.

### lit()

```
lit(<string>)
```

Returns \<string\> without evaluating its contents. The argument is not
parsed by the expression evaluator.

## ANSI Color

### ansi()

```
ansi(<color-code>, <string>)
```

Applies ANSI color formatting to \<string\>. The \<color-code\> parameter
specifies foreground and/or background colors using letter codes:

| Code | Color |
|------|-------|
| `x`  | Black (dark) |
| `r`  | Red |
| `g`  | Green |
| `y`  | Yellow |
| `b`  | Blue |
| `m`  | Magenta |
| `c`  | Cyan |
| `w`  | White |

Uppercase letters (`R`, `G`, etc.) select bright/bold variants. Prefix with
`X`, `R`, `G`, etc. preceded by a capital letter for background colors.
Additional codes: `h` (highlight/bold), `u` (underline), `f` (flash/blink),
`i` (inverse).

### stripansi()

```
stripansi(<string>)
```

Removes all ANSI color codes from \<string\>, returning plain text.

## Character Conversion

### chr()

```
chr(<number>)
```

Returns the character corresponding to ASCII code \<number\>. The number shall
be in the range 32-126 (printable ASCII). Implementations may support extended
ranges.

### ord()

```
ord(<character>)
```

Returns the ASCII code of the first character of the argument.

## Encryption

### encrypt()

```
encrypt(<string>, <key>)
```

Encrypts \<string\> using \<key\>. The algorithm is implementation-defined but
shall be reversible with `decrypt()` using the same key.

### decrypt()

```
decrypt(<string>, <key>)
```

Decrypts \<string\> that was encrypted with `encrypt()` using the same
\<key\>.

### encode64()

```
encode64(<string>)
```

Returns the Base64 encoding of \<string\>. Level 2.

### decode64()

```
decode64(<string>)
```

Returns the decoded value of a Base64-encoded \<string\>. Level 2.

### digest()

```
digest(<algorithm>, <string>)
```

Returns a cryptographic hash of \<string\> using the specified algorithm.
Common algorithms include `sha1`, `md5`, and `sha256`. The set of supported
algorithms is implementation-defined. Level 2.

## Miscellaneous String Functions

### art()

```
art(<word>)
```

Returns the appropriate English indefinite article (`a` or `an`) for \<word\>.

### speak()

```
speak(<speaker>, <string>)
```

Formats \<string\> as speech from \<speaker\>, applying the say/pose
formatting conventions.

### valid()

```
valid(<category>, <string>)
```

Returns 1 if \<string\> is valid for the specified \<category\>, and 0
otherwise. Common categories include `name` (object name), `attrname`
(attribute name), and `playername` (player name).

### comp()

```
comp(<string1>, <string2>)
```

Performs lexicographic comparison of two strings. Returns -1 if \<string1\>
sorts before \<string2\>, 0 if they are equal, or 1 if \<string1\> sorts after
\<string2\>. The comparison is case-insensitive.

### before()

```
before(<string>, <delimiter>)
```

Returns the portion of \<string\> before the first occurrence of
\<delimiter\>. If \<delimiter\> is not found, returns the entire string.
Level 2.

### after()

```
after(<string>, <delimiter>)
```

Returns the portion of \<string\> after the first occurrence of
\<delimiter\>. If \<delimiter\> is not found, returns an empty string.
Level 2.

## Implementation Notes

String function behavior with ANSI color codes varies by implementation.
Conforming implementations should handle embedded ANSI codes transparently
in positional functions (`mid()`, `left()`, `right()`, `strlen()`), counting
only visible characters.

The `escape()` and `secure()` functions are critical for preventing code
injection when incorporating user-supplied text into expressions or commands.
Builders should use `secure()` for untrusted input in all contexts.
