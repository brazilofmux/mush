# Issues and Opportunities for The MUSH Standard

This file tracks discrepancies between *The MUSH Standard* (Volume 1), *The MUSH User's Manual* (Volume 2), and the reference source code in `./src` (TinyMUX, TinyMUSH, PennMUSH, RhostMUSH).

## Volume 1: The MUSH Standard

### Chapter 5: Object Types

- **[BUG] `type()` return value for GARBAGE:**
  - **Standard Claim:** "A conforming implementation shall support ... GARBAGE for destroyed objects" and "`type(<obj>)` returns ... `GARBAGE`." It further claims this is "universal across all four implementations."
  - **Actual Behavior:**
    - **TinyMUX/TinyMUSH:** `fun_type` returns `#-1 ILLEGAL TYPE` for garbage because `Good_obj(it)` check fails for `TYPE_GARBAGE`.
    - **RhostMUSH:** `fun_type` returns `#-1 NOT FOUND` for similar reasons.
    - **PennMUSH:** Conforms to the standard (returns `GARBAGE`).
  - **Impact:** The standard is factually incorrect regarding the "universality" of this behavior and incorrectly describes the behavior of its primary target implementations (MUX/Tiny).

- **[OPPORTUNITY] Internal Type Codes:**
  - The standard notes TinyMUSH/RhostMUSH use type code 4 for ZONE. This is confirmed in RhostMUSH (`#define TYPE_ZONE 0x4`). Adding a note that MUX also reserves this space (though not explicitly used as a user-creatable type) would improve technical accuracy.

### Chapter 6: Attributes

- **[BUG] Attribute Flag Naming (AF_LOCKED vs AF_LOCK):**
  - **Standard Claim:** Uses `AF_LOCKED` as the standard flag name for "Only the attribute's creator can modify it."
  - **Actual Behavior:** All major implementations (TinyMUX, TinyMUSH, PennMUSH, RhostMUSH) use `AF_LOCK` internally and in user-visible flag displays.
  - **Impact:** Misleading for both implementors and users looking for the "standard" name.

- **[OPPORTUNITY] AF_NOPROG Flag:**
  - **Observation:** `AF_NOPROG` (preventing $-command search) is present in both TinyMUX and TinyMUSH but omitted from the standard attribute flags table.
  - **Recommendation:** Add `AF_NOPROG` to the standard to improve coverage of common implementation behavior.

- **[BUG] Standard Lock Attribute Names:**
  - **Standard Claim:** Uses names like `LENTER`, `LLEAVE`, `LOPEN`, `LCONTROL`, `LPARENT`.
  - **Actual Behavior (TinyMUSH/MUX):** Uses `EnterLock`, `LeaveLock`, `OpenLock`, `ControlLock`. `LPARENT` is often missing or named `ParentLock`.
  - **Impact:** Code written for the standard's names will fail on the most common servers unless aliases are provided.

- **[BUG] Attribute Visibility Flags (AF_DARK vs AF_MDARK):**
  - **Standard Claim:** `AF_DARK` is "Only the server (or God) can see this", `AF_MDARK` is "Only wizards can see this".
  - **Actual Behavior (MUX/Tiny):** `AF_DARK` is often "Only #1 can see it", but `AF_ODARK` is used for "owner only". The standard's definitions are slightly blurred compared to implementation reality (especially MUX's `AF_ODARK`).

### Chapter 7: Flags and Toggles

- **[BUG] Flag Character Codes:**
  - **Standard Claim:** Specifies character codes like `R` (ROOM), `E` (EXIT), `P` (PLAYER), `D` (DARK), `S` (STICKY), `W` (WIZARD), etc.
  - **Actual Behavior (MUX/Tiny):** While many match, there are significant omissions and differences. The standard claims THING has no character code, but implementations often use one (e.g., in some contexts). More importantly, many standard flags like `LIGHT`, `OPAQUE`, and `AUDIBLE` are listed with `--` (no character code), while they often have one in specific implementations (e.g., TinyMUSH uses `L` for LIGHT, but the standard uses `L` for LINK_OK).
  - **Impact:** Inconsistent for users trying to parse flags from object headers.

- **[BUG] Flag Function Naming (`hasflag` vs `has_flag`):**
  - **Standard Claim:** Specifies `hasflag(<object>, <flag-name>)` and `flags(<object>)`.
  - **Actual Behavior:**
    - **TinyMUX:** Uses `has_flag()` (with underscore). `flags()` exists but is often overshadowed by other ways to get flags.
    - **TinyMUSH:** Uses `hasflag()` (no underscore).
  - **Impact:** Softcode written using `hasflag()` will break on TinyMUX unless an alias is provided. The standard should note this common variation or recommend one definitively.

- **[OPPORTUNITY] SEETHRU vs TRANSPARENT:**
  - **Observation:** The standard calls the flag `TRANSPARENT` with an alias `SEETHRU`.
  - **Actual Behavior (MUX):** The internal constant and primary name is often `SEETHRU`.
  - **Recommendation:** Standardize on one and explicitly list the other as a required alias.

### Chapter 12: Expression Evaluation

- **[BUG] Evaluation Order for Functions:**
  - **Standard Claim:** "evaluation proceeds strictly left to right... no operator precedence among special characters."
  - **Actual Behavior (TinyMUX/TinyMUSH):** While largely true, functions are identified by looking *backwards* from a `(` character. This means a word is only treated as a function if it is immediately followed by an opening parenthesis. The standard's description of a simple scanner doesn't fully capture this "lookahead/lookback" dependency for function calls.
  - **Impact:** Technical inaccuracy in the description of the evaluation algorithm.

- **[BUG] Space Compression Defaults:**
  - **Standard Claim:** "By default, the evaluator compresses consecutive spaces in the output to a single space."
  - **Actual Behavior:** This is highly configurable (`mudconf.space_compress`) and depends on evaluation flags (`EV_NO_COMPRESS`). In many modern MUSH setups, space compression is often disabled or handled differently than the "always on by default" description suggests.
  - **Impact:** Misleading for users expecting specific formatting behavior.

- **[OPPORTUNITY] Evaluation Limits:**
  - **Observation:** The standard mentions a nesting depth of at least 50.
  - **Actual Behavior:** TinyMUX/TinyMUSH implement multiple limits: `func_nest_lim` (function nesting), `func_invk_lim` (total invocations), and `nStackLimit` (stack depth).
  - **Recommendation:** The standard should explicitly define these separate limits as they are all present in the reference implementations to prevent different types of resource exhaustion.

### Chapter 13: Substitution and Percent Codes

- **[BUG] Case-Sensitivity of Formatting Codes (%r, %t, %b):**
  - **Standard Claim:** "The uppercase variants %R, %T, and %B are equivalent to their lowercase forms."
  - **Actual Behavior (TinyMUX):** Uppercase %R, %T, and %B trigger capitalization of the first character of the *next* substitution result (due to `cType_L2 & 0x80` logic). They are NOT equivalent to their lowercase forms in terms of overall evaluator state, although they produce the same whitespace character.
  - **Impact:** Misleading for users who expect identical behavior.

- **[BUG] Missing Standard Substitutions:**
  - **Observation:** Several common and useful substitutions in TinyMUX/TinyMUSH are missing from the standard:
    - `%|` -- Piped command output (`mudstate.pout`).
    - `%k` or `%K` -- Moniker (ANSI-colored name).
    - `%=<attr>` -- Variable attribute substitution (similar to `v()`).
    - `%+` -- Number of arguments (marked as Level 2 in table but logic is present in core).
    - `%:` -- Enactor ObjID (dbref + creation time).
  - **Recommendation:** These should be added to the standard to reflect actual implementation capabilities.

- **[OPPORTUNITY] itext() Substitutions (%i0-%i9):**
  - **Observation:** The standard marks `%i<n>` as Level 2. In TinyMUX, this is handled directly in the evaluator via `mudstate.itext`.
  - **Recommendation:** Move this to Level 1 as it is a core feature for modern MUSH coding and widely supported.

### Chapter 9: Command Parsing and Dispatch

- **[BUG] Command Matching Order (Exits vs Built-ins):**
  - **Standard Claim:** "Step 2: Built-in Commands ... Step 3: Exit Matching".
  - **Actual Behavior (TinyMUX):** Exits are generally matched *before* built-in commands in many common configurations (to allow "north" to be an exit even if there's a "north" command). The internal `process_command` logic in TinyMUX/TinyMUSH is more complex and often prioritizes local exits over global commands.
  - **Impact:** Misleading for builders who expect built-in commands to always "win" over exits.

- **[BUG] Special Command Handling (QUIT, WHO, LOGOUT):**
  - **Standard Claim:** QUIT and WHO are "checked after built-in commands" (implied by Step 2/Step 4 structure).
  - **Actual Behavior (TinyMUX):** `QUIT`, `WHO`, `LOGOUT`, and `SESSION` are checked very early in `process_command` (before most other matching) as they are connection-level commands.
  - **Impact:** Technical inaccuracy in the dispatch pipeline description.

- **[OPPORTUNITY] Piped Commands (%|):**
  - **Observation:** The standard does not mention command piping or the `%|` substitution for the result of a piped command.
  - **Actual Behavior:** This is a core feature in TinyMUX/TinyMUSH for chaining commands and passing output.
  - **Recommendation:** Add a section on command piping to Chapter 9 or 11.

- **[BUG] Prefix Command '&' (Attribute Set):**
  - **Standard Claim:** Lists `&` as a Step 1 prefix command.
  - **Actual Behavior (TinyMUX):** `&` is often handled as a special case within the attribute system rather than a top-level prefix command in the same way as `"` or `:`. Its behavior with respect to spaces (`& attr object=value`) is more flexible in implementations than the standard implies.
