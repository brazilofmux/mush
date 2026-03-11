# Name Matching and Resolution

## Overview

Many commands and functions require an object reference as an argument. The
process of converting a text string into a specific object dbref is called
**name matching** or **name resolution**. This chapter specifies the rules
by which names are resolved to objects.

## Match Tokens

Before attempting name-based matching, the server checks for special tokens
that resolve to specific objects without a name search:

| Token          | Resolves To | Description |
|----------------|-------------|-------------|
| `me`           | The executor | The object executing the current command. For interactive commands, this is the connected player. |
| `here`         | The executor's location | The room or object containing the executor. |
| `home`         | HOME (`#-3`) | The virtual home reference. |
| `#<number>`    | The object with that dbref | Absolute reference by database number (e.g., `#42`). |
| `*<name>`      | The named player | Player lookup by name (e.g., `*Bob`). Only matches player objects. |

Token matching is case-insensitive for `me`, `here`, and `home`. The `*`
prefix for player matching strips the asterisk and searches for a player with
the given name.

Token matching takes priority over name-based matching. If the input exactly
matches a token form, no further matching is performed.

## Name-Based Matching

When the input is not a special token, the server searches for objects whose
name matches the input string. The search scope depends on the context of the
match.

### Match Contexts

Different commands search different sets of objects. The standard match
contexts are:

| Context       | Objects Searched |
|---------------|-----------------|
| **Nearby**    | Contents of the executor's location, plus the executor's inventory, plus the location itself. This is the most common context, used by `look`, `get`, `examine`, and most other commands. |
| **Possession** | The executor's inventory only. Used by `drop`, `give`, and similar commands. |
| **Exit**      | Exits in the executor's location, plus exits inherited from parent rooms and the master room. |
| **Player**    | All player objects in the database. Used with the `*` prefix and by `page`, `@mail`, and similar commands. |
| **Absolute**  | The entire database (by dbref only). Used with `#<number>` references. |

### Search Procedure

When performing a name-based match, the server follows this procedure:

1. **Collect candidates:** Gather all objects in the match context.

2. **Test each candidate:** Compare the input string against each candidate's
   name using the string matching rules below. For exits, compare against
   each alias in the exit's semicolon-delimited name.

3. **Classify matches:** Each match is classified by confidence:
   - **Exact match:** The input is identical to the full object name (case-
     insensitive).
   - **Partial match:** The input matches the beginning of the object name at
     a word boundary (case-insensitive).
   - **No match:** The input does not match the candidate.

4. **Select the result:** Apply the priority rules described below.

### String Matching Rules

Name comparison uses the following algorithm:

1. Compare the input string against the object name, case-insensitively.
2. If the input exactly matches the full name, the match is **exact**.
3. If the input matches the beginning of the name, starting at a word
   boundary, the match is **partial**. A word boundary occurs at the
   beginning of the string or after a non-alphanumeric character.

Examples:

```
Input: "sword"
  "Magic Sword"  → partial match (matches at word boundary "Sword")
  "Swordfish"    → partial match (matches at start)
  "sword"        → exact match

Input: "ma"
  "Magic Sword"  → partial match (matches at start "Ma...")
  "Hammer"       → no match ("ma" does not start at a word boundary)

Input: "n"
  "North;north;n" → exact match (matches alias "n")
```

### Match Priority

When multiple objects match, the following priority rules determine the result:

1. **Exact matches beat partial matches.** If any candidate is an exact match,
   all partial matches are discarded.

2. **Local matches beat remote matches.** An object in the executor's inventory
   or room takes priority over an object found through inheritance or the
   master room.

3. **Token matches beat name matches.** If the input matches both a special
   token and an object name, the token takes priority.

4. **Single match succeeds.** If exactly one candidate remains after applying
   priority rules, that object is the result.

5. **Multiple matches produce AMBIGUOUS.** If multiple candidates remain with
   equal priority, the match result is AMBIGUOUS (`#-2`). The server should
   display a message such as "I don't know which one you mean!" to the player.

6. **No matches produce NOTHING.** If no candidates match, the match result
   is NOTHING (`#-1`). The server should display a message such as "I don't
   see that here." to the player.

**Compatibility Note:** Some implementations resolve ambiguous matches by
selecting randomly rather than returning AMBIGUOUS. This standard permits
either behavior; implementations should document their choice.

### Exit Matching

Exit matching follows the same string matching rules but searches exit alias
lists. An exit's name is a semicolon-delimited list of aliases:

```
North;north;n
```

Each alias is tested independently. If the input matches any alias, the exit
matches. The first alias (the display name) is used for display purposes;
all aliases are equally valid for matching.

Exit matching uses the following search order:

1. Exits attached to the player's current room.
2. Exits on parent rooms of the current room (following the parent chain).
3. Exits attached to objects in the master room (`#0`), providing global
   exits.

If exactly one exit matches across all levels, the player traverses it. If
multiple exits match at the same level, the behavior is implementation-defined
(select randomly, use the first match, or report ambiguity).

## Object Locating Functions

A conforming implementation shall provide the following functions for
resolving names to dbrefs:

| Function | Arguments | Returns | Level |
|----------|-----------|---------|-------|
| `num(<name>)` | An object name or token. | The dbref of the matched object, using the same matching rules as interactive commands. | 1 |
| `pmatch(<name>)` | A player name. | The dbref of the named player, or `#-1` if not found. | 1 |
| `locate(<executor>, <name>, <scope>)` | An executor, a name, and a scope specification. | The dbref of the matched object, searching the specified scope. | 1 |
| `objid(<object>)` | An object reference. | The object's dbref and creation timestamp, providing a unique identifier that survives dbref recycling. Level 2. | 2 |

### The locate() Function

The `locate()` function provides precise control over name resolution. Its
third argument specifies which match contexts to search using a string of
flag characters:

| Character | Meaning |
|-----------|---------|
| `*`       | Match everything (all contexts). |
| `a`       | Match absolute dbrefs (`#number`). |
| `e`       | Match exits. |
| `h`       | Match "here" token. |
| `i`       | Match inventory (possessions). |
| `l`       | Match objects in the executor's location (neighbors). |
| `m`       | Match "me" token. |
| `n`       | Match nearby (location + inventory + location itself). |
| `p`       | Match players by `*name`. |

Additional flag characters may control type restrictions:

| Character | Meaning |
|-----------|---------|
| `E`       | Prefer exits. |
| `L`       | Prefer objects in the executor's location. |
| `P`       | Prefer players. |
| `R`       | Prefer rooms. |
| `T`       | Prefer things. |
| `X`       | Return `#-1` on failure (don't report errors to the player). |

Example:

```
> think locate(me, north, e)
#55
> think locate(me, Bob, p)
#42
> think locate(me, sword, in)
#100
```

## Pronoun and Reference Resolution

Some commands accept object references using contextual pronouns:

- **it** or **them:** May refer to the last object the player interacted
  with. Support for this feature is implementation-defined.

- **\<number\>:** In commands like `get`, a bare number may refer to an object
  by dbref without the `#` prefix, depending on the command and
  implementation.

## Name Matching and Permissions

Name matching does not bypass the permission model. Even if an object is
matched by name, the player must have appropriate permissions to interact
with it. However, the matching process itself does not check permissions --
it only locates the object. Permission checks occur when the matched command
is executed.

Exceptions:

- Objects with the DARK flag are excluded from the contents list display but
  are still matchable by name by their owner and by wizards.
- Some implementations exclude DARK objects from name matching for non-owners.
  This behavior is implementation-defined.
