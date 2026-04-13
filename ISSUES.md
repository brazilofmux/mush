# Issues

Consolidated issues from three independent reviews (Claude, Codex,
Gemini) cross-referencing the book against source code in `./src/`
(TinyMUSH 4.0 alpha, TinyMUX 2.14.0.7, RhostMUSH, PennMUSH 1.8.8p0)
and the comparative survey documents in `./surveys/`.

---

## Infrastructure

- [ ] **mdfix batch processing bug.** When processing multiple files in
  a single invocation, mdfix sometimes overwrites a file with the
  content of the preceding file. Affected 2-18, 2-21, 2-25 in this
  session. Workaround: process files one at a time. Root cause needs
  investigation in `mdfix.rl`.

- [ ] **Repository evidence framing in `ISSUES.md` drifted from the
  actual `./src` tree.** This file still described the bundled MUX tree
  as "TinyMUX 2.13", but `src/mux2.14/include/_build.h` identifies it as
  `2.14.0.7` with release date `2026-APR-03`. PennMUSH is also present in
  `src/pennmush/` with `Patchlevel` identifying `1.8.8p0`. Future review
  notes should anchor claims to the versions actually vendored in this
  repository, not older survey assumptions.

---

## Architectural / Framing Issues

These affect how the standard positions itself relative to the four
reference implementations.

- [ ] **The standard over-claims cross-engine consensus.** Several
  chapters present PennMUSH/TinyMUSH-oriented normalization as
  four-engine agreement. The channels system, power catalog, builder
  access model, and zone mechanisms all diverge more than the
  normative prose acknowledges. RhostMUSH has no hardcoded comsys
  (`POWER_COMPARE.TXT:13-15`); TinyMUSH's comsys is a module
  (`comsys.c:2100-2112`), not a universal core interface. Survey data
  deepens this: PennMUSH has 246 functions MUX lacks; RhostMUSH has
  310 functions MUX lacks; MUX has 106-115 functions each of the
  others lack. Claiming four-engine agreement on almost anything
  requires care. [Codex, Surveys]

- [x] **`#0` conflated as universal master room, start room, and
  global-command room.** MUX separates `player_starting_room` from
  `master_room` (`CONFIGURATION.md:49-55`). RhostMUSH has
  `player_starting_room` as a config parameter. Updated Ch 4 to
  separate the concepts. [Codex, Claude]

- [x] **"Every player can build" (2-01) is incorrect.** All four
  implementations gate building behind permissions: MUX marks @create,
  @dig, @open with `CA_GBL_BUILD` (`command.cpp:734-750`). PennMUSH
  has `restrict_building` and `Builder(x)`. Fixed in both 2-01
  (hedged to "subject to permissions") and the architectural framing
  issue. [Codex, Surveys]

- [ ] **Modernization Opportunity: Standardize MUX 2.14 features.** MUX
  2.14 has implemented many features (JSON, WebSockets, SQL cursors,
  printf, mailsend, @cron, letq) that are essential for modern MU*
  development. The standard should move these from "Optional" or
  "Future" to "Level 2" or provide a "Modern MUSH" conformance level.
  Source-backed examples now exist in the bundled help and code:
  `src/mux2.14/game/text/help.txt` has topics for `@cron`,
  `gmcp()`, `json()`, `json_query()`, `json_mod()`, `letq()`,
  `mailsend()`, and `printf()`, while `src/mux2.14/src/websocket.cpp`
  and `src/mux2.14/src/telnet.cpp` implement WebSocket and GMCP support.
  [Gemini, refreshed against current src]

- [ ] **Help system architecture is more implementation-defined than
  the books currently signal.** Volume 1 Chapter 19 says help "reads
  from text files maintained by the server administrator", which is true
  at a very high level but misses important structural divergence visible
  in `./src`: PennMUSH composes help from source directories like
  `game/txt/hlp` via `compose.sh` and configurable `help_command`
  entries (`src/pennmush/game/txt/README`, `src/pennmush/game/mushcnf.dst`,
  `src/pennmush/src/help.c`); TinyMUSH exposes configurable
  `helpfile`/`raw_helpfile` local help in `src/tinymush/src/docs/plushelp.txt`;
  RhostMUSH adds `/search`, `/query`, and `/syntax` help behaviors in
  `src/rhostmush/Server/game/txt/help.txt`; TinyMUX ships separate
  `help.txt`, `wizhelp.txt`, `plushelp.txt`, and `staffhelp.txt`.
  This deserves either a matrix or an explicit "help subsystem is
  implementation-defined" callout earlier in the books. [Codex]

- [ ] **The bundled help corpus is not uniformly current across
  implementations, which weakens it as direct evidence unless labeled.**
  `src/tinymush/README.md` describes TinyMUSH 4 alpha, but
  `src/tinymush/src/docs/help.txt` still opens with "This is the TinyMUSH 3
  online help facility" and says the help is "currently under revision."
  PennMUSH's repo snapshot includes the help composition machinery and the
  connect-screen text files, but not a generated `game/txt/help.txt`.
  The book project should distinguish "current code behavior", "bundled
  shipped help", and "historical help text" when citing implementation
  evidence. [Codex]

- [ ] **Powers catalog (1-08) is PennMUSH vocabulary, not neutral
  standard.** Book uses PennMUSH C macro names (CAN_BUILD, PEMIT_ALL,
  TEL_ANYWHERE). MUX uses: builder, announce, tel_anywhere. PennMUSH
  user-facing: Builder, Announce, Tport_Anywhere. RhostMUSH uses
  entirely different names (FREE_WALL, FREE_QUOTA, PCREATE,
  TEL_ANYTHING, SEARCH_ANY). Several powers (PEMIT_ALL, CREATE_PLAYER,
  GLOBAL_FUNCS, HUGE_QUEUE, LOGIN_ANYTIME, OPEN_ANYWHERE) are
  PennMUSH-only but not marked as such. Survey data shows the
  divergence is conceptual, not just naming: RhostMUSH has 3 power
  words (48 powers), 3 depower words, 8 toggle words (~200 toggles),
  and a totem system -- an entirely different permission architecture.
  [Claude, Codex, Gemini, Surveys]

- [ ] **Channel system is not a universal core subsystem.** The issue
  goes beyond command syntax: 2 of 4 engines do not have a hardcoded
  channel system at all. RhostMUSH has no hardcoded comsys. TinyMUSH's
  comsys is a loadable module with minimal softcode access. Even the
  softcode function API diverges wildly: MUX has `channels()`,
  `cemit()`, `cwho()`, `comalias()`, `comtitle()`, `chanobj()`;
  PennMUSH has 10 channel function variants (`cbuffer`, `cdesc`,
  `cflags`, `cmsgs`...); Rhost has limited softcode access; TinyMUSH
  module has minimal softcode access. The book presents `@channel/join`
  and related commands as standard, but the concept of a standard
  channel command set doesn't apply to half the engines.
  [Claude, Codex, Surveys]

### Suggested Structural Improvements [Codex, Surveys]

- [ ] Add per-engine behavior matrices for chapters that normalize
  divergent behavior (especially Ch 4, 7, 8, 27, 30).
- [ ] Separate "common model" from "example command syntax" -- present
  abstract semantics, then engine-specific examples.
- [ ] Mark implementation-defined areas earlier and more aggressively,
  before normative prose rather than after.
- [ ] Consider a source-backed appendix listing which claims were
  verified against which source paths.
- [ ] Add a function name equivalence table as a structural element.
  The naming divergence is systemic (e.g., `dice()`/`die()`,
  `if()`/`ifelse()`, `nattr()`/`attrcnt()`, `hasflag()`/`has_flag()`),
  not isolated incidents. [Surveys]
- [ ] Lock type availability matrix. PennMUSH has 30+ lock types
  (Follow, Receive, Examine, Destroy, Interact, MailForward, Chown,
  Filter, InFilter) with no equivalents in other engines. The current
  lock chapters focus on naming differences but miss the scale of the
  divergence. [Surveys]

- [ ] **Clarify target MUX version.** The `src/` directory contains
  TinyMUX 2.14.0.7 (confirmed via `include/_build.h`), but
  `./surveys/` and previous notes reference MUX 2.13 features. The
  standard should target 2.14 behavior as the current reference. [Gemini]

---

## Volume 1: High-Impact Factual Errors

- [x] **1-05: Dropto behavior description is wrong.** STICKY on an
  object sends it HOME, not to the dropto. Room sweep behavior
  (objects to dropto when all players leave) requires the room itself
  to have STICKY -- omitted. (MUX `move.cpp:255-308`) [Claude]

- [x] **1-05: `type()` return for GARBAGE is not universal.** Book
  claims all four return `GARBAGE`. TinyMUX/TinyMUSH return
  `#-1 ILLEGAL TYPE`; RhostMUSH returns `#-1 NOT FOUND`. Only
  PennMUSH returns `GARBAGE`. [Gemini]

- [x] **1-06: `get()` inheritance claim is wrong.** Book says `get()`
  retrieves without inheritance. All four implementations walk the
  parent chain: MUX `functions.cpp:2066` calls `atr_pget_LEN`;
  PennMUSH `attrib.c:1184` calls `atr_get_with_parent()`. [Claude]

- [x] **1-06: Attribute flag `AF_LOCKED` should be `AF_LOCK`.** All
  four implementations use `AF_LOCK` internally and in user-visible
  displays, not `AF_LOCKED`. [Gemini]

- [x] **1-09: $-command search order is internally inconsistent.** The
  numbered list says Player > Inventory > Room > Objects-in-room. MUX
  source (`command.cpp:2645-2673`) shows Player > Objects-in-room >
  Room > Inventory. The implementation note at the bottom contradicts
  the list. [Claude]

- [x] **1-09, 1-11: `@force` described as immediate execution.** Both
  TinyMUSH and TinyMUX queue `@force` by default; only `@force/now`
  is immediate. (MUX `wiz.cpp:328-339`) [Claude]

- [x] **1-15: Movement message sequence is wrong.** LEAVE/OLEAVE/ALEAVE
  fire BEFORE `move_object`, not after. Steps 3-7 are misordered.
  Actual: SUCC/OSUCC/ASUCC on exit -> LEAVE/OLEAVE/ALEAVE + OXENTER
  -> move -> DROP/ODROP/ADROP -> MOVE/OMOVE/AMOVE on player ->
  ENTER/OENTER/AENTER + OXLEAVE. (MUX `move.cpp:358-367`) [Claude]

- [x] **1-15: MOVE/OMOVE/AMOVE attributes omitted entirely.** After
  DROP/ODROP/ADROP, the player's own MOVE, OMOVE, AMOVE fire. Not
  mentioned in the book. [Claude]

- [x] **1-15: Teleport message sequence is reversed.** OXTPORT fires
  BEFORE the move; TPORT/OTPORT/ATPORT fires AFTER. Book has it
  backwards. (MUX `move.cpp:432-441`) [Claude]

- [x] **1-16: HAVEN blocking @pemit is incorrect.** HAVEN blocks pages,
  not @pemit. No implementation checks HAVEN in the pemit path.
  PEMIT_ALL power is PennMUSH-only. [Claude]

- [x] **1-16: Nospoof format is reversed.** Book shows
  `[#42(Bob)] ...` but actual format is `[Bob(#42)]` -- name first,
  then dbref. (MUX `game.cpp:723-727`) [Claude]

- [x] **1-18: @verb syntax is significantly oversimplified.** The
  actual arguments are attribute names for the did_it pipeline, not
  direct text messages. Argument count and meaning are wrong.
  (TinyMUSH `predicates.c:3068-3194`) [Claude]

- [x] **1-29: Zone lock mechanism varies drastically but only one model
  is described.** PennMUSH uses `@lock/zone`; TinyMUX uses the enter
  lock on the ZMO; TinyMUSH uses the control lock + CONTROL_OK.
  All three mechanisms now documented. [Claude, Codex]

- [x] **1-09: Exit matching vs built-in command order may vary.** Book
  says Step 2 is built-ins, Step 3 is exits. Added compatibility note
  about configurable ordering. [Gemini]

- [x] **1-09: QUIT/WHO/LOGOUT/SESSION are connection-level commands,
  checked before most other matching.** Book implies they are checked
  after built-in commands (Step 2/Step 4). They are actually checked
  very early in `process_command`. [Gemini]

- [x] **1-11: `@trigger` execution model -- disputed.** MUX source
  confirms: without `/now`, `@trigger` calls `did_it()` which queues.
  With `/now`, it calls `process_command()` inline. Book is correct
  that `@trigger` queues by default. [Gemini, verified]

- [x] **1-12: Function identification mechanism not described.** The
  evaluator identifies functions by looking backwards from a `(`
  character. The standard correctly states "encounters a word
  immediately followed by `(`" which captures the user-visible
  behavior. The backward-scan implementation detail is not relevant
  to a standards document. [Gemini]

- [x] **1-12: Space compression described as always-on default.** In
  practice, `mudconf.space_compress` is configurable and `EV_NO_COMPRESS`
  evaluation flags exist. Many modern setups disable space compression.
  [Gemini]

- [x] **1-13: Uppercase `%R`/`%T`/`%B` are NOT equivalent to lowercase
  in MUX.** Investigation of MUX 2.13 `isSpecial_L2` table shows
  `%R`, `%T`, `%B` have the same code as lowercase (no 0x80 bit).
  The capitalization behavior applies to `%N`, `%S`, `%P`, `%O`,
  `%A`, `%M` -- NOT to `%R`/`%T`/`%B`. Issue was incorrect. [Gemini]

- [x] **1-13: Several common percent-code substitutions missing.** `%|`
  (piped command output), `%k`/`%K` (moniker/ANSI-colored name),
  `%=<attr>` (variable attribute substitution), `%+` (already listed),
  `%:` (enactor ObjID). All added to Ch 13. [Gemini]

- [x] **1-28: INHERIT flag behavior description is wrong.** Book says
  objects need INHERIT to get wizard privileges from their owner. In
  MUX, objects owned by wizards inherit by default if they own
  themselves. Added self-ownership and owner-INHERIT cases. [Gemini]

- [x] **1-28: `control_all` power not architecturally God-only.** Book
  is correct: MUX source uses `ph_god` handler for `control_all`,
  restricting it to God. No change needed. [Gemini]

- [x] **1-28: MISTRUST/TRUST flags described as Level 2 but don't exist
  in MUX/TinyMUSH/PennMUSH.** TRUST and MISTRUST are PennMUSH-specific.
  TRUST is an alias for INHERIT. Not in MUX or TinyMUSH. [Gemini]

---

## Volume 1: Medium-Impact Issues

### Flags (Ch 7)

- [x] **1-07: Several flags incorrectly listed with no display
  character.** OPAQUE='O', LIGHT='l', AUDIBLE='a', ROYALTY='Z',
  PARENT_OK='Y', OPEN_OK='z' in MUX. All fixed. [Claude, Gemini]

- [x] **1-07: IMMORTAL permission listed as "God" but source shows
  "Wizard".** Both TinyMUSH and MUX use `fh_wiz`. Fixed. [Claude]

- [x] **1-07: ZONE_MASTER, ZONE_CONTENTS, ZONE_PARENT flags do not
  exist with those names.** Replaced with actual engine-specific
  zone flag descriptions. [Claude]

- [x] **1-07: CONTROL_OK does not exist in TinyMUX.**
  TinyMUSH-only. Noted. [Claude]

- [x] **1-07: GUEST is a power in TinyMUX, not a flag.**
  Noted in flag table. [Claude]

- [x] **1-07: INDESTRUCTIBLE listed as RhostMUSH-only but exists in
  TinyMUX too.** Fixed. [Claude]

- [x] **1-07: `hasflag()` vs `has_flag()` naming.** Investigation
  shows all four engines use `hasflag()` (no underscore). The issue
  claim was incorrect. No change needed. [Gemini]

- [x] **1-07: SEETHRU vs TRANSPARENT naming.** MUX user-facing name is
  `TRANSPARENT` (internal constant is `SEETHRU`). Book correctly uses
  `TRANSPARENT`. No change needed. [Gemini]

### Attributes (Ch 6)

- [x] **1-06: Standard lock attribute names don't match
  implementations.** Book uses LENTER, LLEAVE, LOPEN, LCONTROL.
  TinyMUSH/MUX use EnterLock, LeaveLock, OpenLock, ControlLock.
  PennMUSH uses named locks. Added explanatory note. [Gemini, Claude]

- [x] **1-06: `AF_DARK` vs `AF_MDARK` vs `AF_ODARK` definitions are
  blurred.** The standard already lists all three with correct
  definitions matching MUX source. No change needed. [Gemini]

- [x] **1-06: `AF_NOPROG` flag omitted.** Already present in the
  attribute flags table (line 328). No fix needed. [Gemini]

### Commands (Ch 15-19)

- [x] **1-15: Fallback home described as "#0" is inaccurate.** MUX
  falls back to `default_home`, then `start_home`, then `start_room`.
  (`object.cpp:371-382`) [Claude]

- [x] **1-15: TOFAIL/OTOFAIL/ATOFAIL teleport failure attributes not
  mentioned.** [Claude]

- [x] **1-16: @femit does not exist in PennMUSH.** Should be marked
  Level 2 or noted. [Claude]

- [x] **1-16: LSPEECH lock requires Auditorium flag in MUX/TinyMUSH.**
  Without the flag, the lock is ignored. (`speech.cpp:75-82`) [Claude]

- [x] **1-17: @name does not require password for player renaming.**
  None of the four implementations require it. May be legacy. [Claude]

- [x] **1-18: @undestroy is PennMUSH-only.** Others clear the GOING
  flag with `@set`. [Claude]

- [x] **1-19: @shutdown/abort does not cancel pending shutdown.**
  TinyMUSH `/abort` means "dump core." MUX has no switches. PennMUSH
  has /panic, /reboot, /paranoid but not /abort. [Claude]

- [x] **1-19: @dump/paranoid is PennMUSH-only.** [Claude]

- [x] **1-19: @allhalt is PennMUSH-only.** Others use
  `@halt/all`. [Claude]

- [x] **1-19: @uptime does not exist in MUX or TinyMUSH.** [Claude]

- [x] **1-19: @if/@ifelse availability varies.** MUX has `@if`.
  PennMUSH has `@ifelse`. TinyMUSH and RhostMUSH have
  neither. [Claude]

- [x] **1-19: @dolist `#@` starts from 1, not 0.** `number` is
  incremented before use. (`walkdb.cpp:82`) [Claude]

- [x] **1-19: @doing does not exist in PennMUSH.** Uses `@poll` and
  the DOING logged-out command. [Claude]

- [x] **1-19: @function permission described as GLOBAL_FUNCS power.**
  MUX and TinyMUSH require GOD. RhostMUSH requires WIZARD. PennMUSH
  has the Global_Funcs power. [Claude]

### Locks and Systems (Ch 27-33)

- [x] **1-27: Lock attribute names diverge.** Book uses TinyMUSH/MUX
  naming (LENTER, LLEAVE). Ch 6 updated with naming note. Ch 27
  updated with PennMUSH-specific lock types. [Claude]

- [x] **1-27: LTELOUT does not exist in PennMUSH.** [Claude]

- [x] **1-30: `@channel/add` syntax is PennMUSH-specific.** TinyMUX
  uses `@channel/create`. [Claude]

- [x] **1-33: Exits field in database table says "rooms only."** Exits
  can be attached to things and players too. [Claude]

### Help System / Admin Model (Ch 19)

- [ ] **1-19: Help system description is too generic to guide
  implementors.** The current text treats help as a plain text-file
  subsystem, but the implementations in `./src` expose materially
  different admin models: PennMUSH has configurable `help_command` and
  `ahelp_command` entries plus build-time composition from source
  fragments; TinyMUSH documents `helpfile` and `raw_helpfile`; RhostMUSH
  supports `/search`, `/query`, and `/syntax`; TinyMUX ships multiple
  parallel help namespaces (`help`, `wizhelp`, `plushelp`, `staffhelp`).
  The chapter should either standardize only minimal semantics
  ("topic-based reference system") or explicitly classify file layout,
  indexing, and search capabilities as implementation-defined. [Codex]

- [ ] **1-19: `wizhelp` as a universal wizard-help command is too
  strong without a configurability note.** MUX, TinyMUSH, and RhostMUSH
  all ship `wizhelp`, but PennMUSH models help commands through config
  (`help_command` / `ahelp_command`) rather than a fixed two-command
  architecture. The current prose risks implying a more uniform command
  surface than the Penn sources support. [Codex]

---

## Volume 1: Low-Impact Issues

- [x] **1-04: `#-4` NOPERM described as TinyMUX-only but also exists
  in RhostMUSH.** (`db.h:146`) [Claude]

- [ ] **1-37: Unicode support listed as "Future Direction" but is fully
  implemented in MUX 2.14.** Move to "Optional Features" or "Level 2"
  and specify UTF-8 requirements. [Gemini]

- [x] **1-05: TYPE_ZONE (type code 4) reserved by RhostMUSH.** Book
  already has a compatibility note covering this. No change needed.
  [Gemini]

- [x] **1-09: `#` prefix command behaves differently in PennMUSH.**
  Goes through `parse_force()` requiring `Mobile(player)` and
  control. Added note. [Claude]

- [x] **1-16: Page recipient separator supports comma separation too,
  not just spaces.** (`speech.cpp:607-660`) [Claude]

- [x] **1-18: @pemit target list supports comma separation, not just
  spaces.** (`speech.cpp:1315`) [Claude]

- [x] **1-18: examine /owner switch is TinyMUSH-only, not just
  Level 2.** MUX has /brief, /debug, /full, /parent. [Claude]

- [x] **1-19: DARK flag with CAN_HIDE power for WHO visibility is
  oversimplified.** Already fixed when rewriting the WHO section
  to note implementation-defined visibility. [Claude]

- [x] **1-29: CONTROL_OK requirement for TinyMUSH zone control not
  mentioned.** Added to zone lock section. [Claude]

- [x] **1-29: Zone event attributes (ZENTER, OZENTER, AZENTER) may be
  PennMUSH-specific.** Confirmed PennMUSH-only. Noted. [Claude]

- [x] **1-32: IDLE power name varies.** MUX: `idle`.
  PennMUSH: `Idle`. Text already says "IDLE power (or equivalent)."
  Cosmetic naming difference. [Claude]

- [x] **1-09: `&` prefix behavior more flexible than described.** `&`
  with spaces (`& attr object=value`) works in implementations; the
  standard implies stricter parsing. Added note. [Gemini]

- [x] **1-09: Command piping (`%|`) not mentioned.** Core feature in
  MUX/TinyMUSH for chaining commands and passing output. Added to
  Ch 9. [Gemini]

- [x] **1-12: Evaluation limits are multiple separate limits, not one.**
  MUX/TinyMUSH have `func_nest_lim` (function nesting),
  `func_invk_lim` (total invocations), and `nStackLimit` (stack
  depth). Updated Ch 12 to reference all three. [Gemini]

- [x] **1-13: `%i<n>` (itext) marked Level 2 but is core in MUX.**
  itext() function exists in all four engines. Removed Level 2 tag,
  added note about %i<n> being MUX shorthand. [Gemini]

---

## Volume 1: Functions (Ch 20-26)

- [x] **1-20: `squish()` described without optional character argument.**
  Ch 26 correctly shows the optional arg. Both MUX and PennMUSH
  support it. [Claude]

- [x] **1-26: `while()` marked Level 2 but only in TinyMUSH and
  RhostMUSH.** Not in MUX or PennMUSH. [Claude]

- [x] **1-24/1-26: Duplicate listings of `isnum()`, `isint()`,
  `isdbref()`, `isobjid()`, `isword()`, `valid()`.** Content is
  consistent but redundant across both chapters. Removed duplicates
  from Ch 26, added cross-reference. [Claude]

---

## Volume 2: Technical Accuracy

- [x] **2-01: "Every player can build" is incorrect.** Building is
  gated behind permissions in all four implementations. [Codex]

- [x] **2-06: STICKY flag description is incorrect.** Same dropto issue
  as 1-05. STICKY sends object HOME, not to dropto. [Claude]

- [x] **2-07: CONFORMAT and EXITFORMAT presented as universal but are
  PennMUSH-specific.** Actually in both MUX and PennMUSH, but not
  TinyMUSH or RhostMUSH. Noted availability. [Claude]

- [x] **2-10: `first()` example with 3 arguments is incorrect.**
  `first()` accepts at most 2 arguments (list, delimiter). [Claude]

- [x] **2-12: `#@` position counter described as starting at 0;
  starts at 1.** Same issue as 1-19. [Claude]

- [x] **2-12: `if()` function not universal.** PennMUSH and MUX have
  `if()`; TinyMUSH and RhostMUSH only have `ifelse()`. The chapter
  should present `ifelse()` as the more universal function and note
  that `if()` is available on PennMUSH and MUX. [Claude, Surveys]

- [x] **2-12: `@if`/`@ifelse` command does not exist on TinyMUSH or
  RhostMUSH.** [Claude]

- [x] **2-13: `repeat()` example output has wrong character count.**
  `repeat(=-, 20)` should produce 40 characters, not 44. [Claude]

- [x] **2-14: Sort type `i` described as "integer" but means
  "case-insensitive."** Correct type for numeric sort is `n`.
  (`funlist.c:168`) [Claude]

- [x] **2-15: $-command search order lists master room as "#0".**
  PennMUSH master room is configurable. [Claude]

- [x] **2-16: ACONNECT example uses `mail(me)` which is a loadable
  module in TinyMUSH, not core.** [Claude]

---

## Volume 2: Coverage Gaps

- [ ] **No coverage of zones.** Mentioned briefly in Ch 15-16
  references but never introduced or explained. [Claude]

- [ ] **No coverage of @power command.** Ch 23 uses `@power Morgan =
  announce` but powers are never explained as a concept. [Claude]

- [ ] **No coverage of @force command.** Mentioned in security warnings
  (Ch 23) but never formally documented. [Claude]

- [ ] **No dedicated explanation of how help systems differ across
  servers.** Volume 2 tells users to type `help`, which is reasonable,
  but it never explains that "extra help" is server-specific:
  TinyMUX ships `plushelp` and `staffhelp`; TinyMUSH documents local
  `+help` via configured helpfiles; RhostMUSH supports wildcard help
  search/query and `/syntax`; PennMUSH lets administrators add arbitrary
  help-style commands with `help_command`. A short chapter or appendix on
  "Using the Help System on Real Servers" would make the manual more
  accurate and more useful. [Codex]

- [ ] **Opportunity: Add a "Modern Features" chapter to Volume 2.** This
  should cover JSON manipulation, SQL queries (using the MUX cursor
  API as a model), and WebSockets/GMCP for modern client integration.
  The current repository provides concrete examples for this chapter:
  TinyMUX 2.14 help includes `@cron`, `gmcp()`, `json()`, `json_query()`,
  `json_mod()`, `letq()`, `mailsend()`, and `printf()`, and the source
  contains WebSocket support. Right now Volume 1 often treats these as
  optional or future-facing while Volume 2 barely mentions them. [Gemini,
  refreshed against current src]

- [ ] **Opportunity: Add a "Scheduled Tasks" chapter to Volume 2.**
  Introduce the `@cron` command system for automated maintenance and
  game-world events. [Gemini]

---

## Survey-Revealed Issues

These were identified by cross-referencing the `./surveys/` comparative
documents against the book and existing issues.

- [ ] **1-31, 2-18: Mail softcode function API diverges across all four
  engines.** RhostMUSH has `mailread()`, `mailsend()`, `mailquick()`,
  `mailquota()`, `mailalias()`, `mailstatus()`. PennMUSH has
  `maillist`, `mailsend`, `mailstats`. MUX has `mail()`, `mailfrom()`,
  `mailreview()`, `mailsubj()`, `mailsize()`, `malias()`. TinyMUSH
  mail is a loadable module. If the standard covers mail functions,
  the sets are completely different. [Surveys]

- [ ] **1-30: Comsys softcode function API diverges wildly.** MUX has
  `channels()`, `cemit()`, `cwho()`, `comalias()`, `comtitle()`,
  `chanobj()`. PennMUSH has 10 channel function variants. RhostMUSH
  has limited softcode access. TinyMUSH comsys module has minimal
  softcode access. ISSUES.md previously addressed channel command
  syntax but not the function API divergence. [Surveys]

- [ ] **Reality levels are a MUX-specific feature not addressed.** MUX
  has a full reality level system (`hasrxlevel`, `hastxlevel`,
  `rxlevel`, `txlevel`, `listrlevels`) that no other engine fully
  matches. RhostMUSH has optional support. If the book discusses
  visibility or perception, this needs to be noted. [Surveys]

- [x] **1-19: `@function` permission model diverges more than
  documented.** The @function section now says the exact mechanism is
  "implementation-defined" after listing per-engine requirements.
  [Surveys]

---

## 2026-04-12 Review Pass — New Findings

Fresh source-cross-reference pass against `./src/` (MUX 2.14.0.7,
PennMUSH 1.8.8p0, TinyMUSH 4 alpha, RhostMUSH). These are NEW items
not already tracked above.

### Volume 1: Foundational / Framing

- [ ] **1-00, 1-01: Over-claims cross-engine consensus in the
  introduction.** The intro asserts the engines "agree far more often
  than they disagree." Survey data (PennMUSH has 246 functions MUX
  lacks; RhostMUSH has 310 MUX lacks; MUX has ~110 each of the others
  lack) contradicts that framing. Should be hedged or scoped to "core
  object and evaluation mechanics."

- [ ] **1-01: Still cites "TinyMUX (version 2.13)."** Vendored source
  is 2.14.0.7 (`src/mux2.14/include/_build.h`). ISSUES.md infra note
  was marked resolved but the chapter text was not updated.

- [ ] **1-02: Terminology chapter conflates master room with start
  room.** Line ~113 defines "master room" as `#0` and also "the
  starting location for newly created players." Same issue that was
  fixed in Ch 4 (marked `[x]` above) — the correction did not
  propagate to the Terminology chapter.

- [ ] **1-14: `iter()` appears twice in the Function Categories
  table.** Listed under both "List functions (Ch 22)" and
  "Miscellaneous (Ch 26)." One should be removed.

### Volume 1: Percent Codes (Ch 13)

- [ ] **1-13: `%c` is a color code in MUX 2.14, not "last command."**
  The standard calls `%c` "last command executed, implementation-
  defined." MUX 2.14 `ast.cpp:1189-1193` dispatches `%c`/`%C` as
  foreground/background ANSI color; `%m` is the last-command code
  (`ast.cpp:1049-1053`). PennMUSH `parse.c:2499` uses `%c` for the
  command line. TinyMUSH `eval.c:1005-1012` makes `%c` configurable.
  "Implementation-defined" is too soft — softcode using `%c` for
  last-command will produce color escapes on MUX 2.14.

- [ ] **1-13: `%?` return format diverges.** Standard says `%?`
  returns a single depth number. PennMUSH `parse.c:2443-2450` returns
  TWO space-separated integers (invocations and recursions). MUX 2.14
  `ast.cpp` has no `case '?'` handler in `ast_eval_subst` — appears
  unimplemented or pass-through.

- [ ] **1-13: `%=<N>` works as positional-arg reference in MUX.** The
  standard documents `%=<attr>` only as attribute-value lookup. MUX
  2.14 `ast.cpp:1139-1165` also handles `%=<0>`…`%=<999>` as positional
  args. Syntax extension undocumented.

### Volume 1: Action Lists / Queue (Ch 11)

- [ ] **1-11: Power names are PennMUSH flag names, not MUX powers.**
  Chapter references `HUGE_QUEUE`, `HALT_ANYTHING`, `PS_ALL`. These
  are PennMUSH object flags (`pennmush/hdrs/flags.h:237-239`). MUX
  equivalents are `halt` (POW_HALT) and `see_queue` (POW_SEE_QUEUE,
  `powers.cpp:99`); MUX has no `@allhalt` at all.

- [ ] **1-11: `@wait/until <epoch>` switch omitted.** MUX 2.14 has
  `@wait/until` for absolute-time scheduling
  (`command.cpp:611`, `cque.cpp:1364`). Only the relative form is
  documented.

- [ ] **1-11: Semaphore-plus-timeout `@wait` syntax description is
  misleading.** Given as `@wait <object>/<timeout>`; actual MUX syntax
  is `@wait <object>/<value>` where `<value>` is interpreted as a
  number (timeout) OR an attribute name (alternate semaphore attr) —
  mutually exclusive, not combinable (`cque.cpp:1400-1437`).

### Volume 1: String Functions (Ch 20)

- [ ] **1-20: `escape()` prefixes with `\`, not `%`.** Standard says
  `escape()` "prefixes special characters with `%`." MUX
  `help.txt:7770` and PennMUSH `funstr.c:1244` use backslash and also
  prepend `\` to the whole string.

- [ ] **1-20: `secure()` replaces characters with spaces, does not
  remove them.** Standard says "removes." Actual behavior preserves
  string length (MUX `help.txt:14643`; PennMUSH `funstr.c:1233`).

- [ ] **1-20: `lpos()` returns all match positions 0-based, not "last
  occurrence."** Entirely wrong description. MUX `help.txt:11092`,
  TinyMUSH `funstring.c:2393`, PennMUSH `function.c:565`. Also
  incorrectly marked Level 2 — exists in all four engines.

- [ ] **1-20: `regedit()` accepts multiple regex/replacement pairs.**
  MUX `help.txt:13827`: `regedit(<str>, <re1>, <rep1> [, …, <reN>,
  <repN>])`. Also supports `$0`–`$99` and named groups, not just
  `$0`–`$9`.

- [ ] **1-20: `speak()` has 2–7 arguments.** Standard shows only
  `speak(<speaker>, <string>)`. PennMUSH `function.c:755` and TinyMUSH
  `functions.c:887` accept transform fn, null fn, open/close
  delimiters, fragment index.

- [ ] **1-20/1-24: `comp()` accepts optional type argument.** MUX
  `help.txt:6473`: `comp(<s1>, <s2>[, <type>])` with types `u`/`c`/`a`.
  PennMUSH `funstr.c:453` accepts types `A`/`I`/`N`/`F`. Default in
  MUX is Unicode collation, not "case-insensitive" as stated.

### Volume 1: Math / Logic Functions (Ch 21)

- [ ] **1-21: `mod()` semantics inverted.** Standard says `mod()`
  follows dividend sign. MUX `help.txt:12017` defines `mod()` with
  floor semantics (result takes divisor sign) and `remainder()` as the
  dividend-sign variant. PennMUSH `funmath.c:369` has the same split.

- [ ] **1-21: `rand()` argument order reversed and range is
  inclusive.** Standard: `rand(<upper>[, <lower>])`. MUX
  `help.txt:13520` and PennMUSH `funmisc.c:812`:
  `rand(<lower>, <upper>)` with inclusive range on both ends. TinyMUSH
  `functions.c:827` accepts only 1 arg.

### Volume 1: List Functions (Ch 22)

- [ ] **1-22: `sort()` type `i` is case-insensitive alphabetic, not
  integer.** TinyMUSH `funlist.c:167`; MUX `help.txt:15056`. Numeric
  sort is type `n`. Direct factual error in the table.

- [ ] **1-22: `sort()` missing MUX-only types.** MUX adds `u`
  (Unicode collation, default), `c` (case-insensitive UCA), `a`
  (legacy ASCII byte-order), `?` (auto-detect). Standard lists only 5
  types (`a`, `i`, `f`, `d`, `n`).

- [ ] **1-22: `index()` 4th arg is field count, not end position.**
  MUX `help.txt:9365`: "returns `<length>` items starting from the
  `<first>` position." PennMUSH `funlist.c:1658-1701` matches.

- [ ] **1-22: `foreach()` takes begin/end delimiter args in MUX, not
  a list delimiter.** MUX `help.txt:8325`:
  `foreach([obj/]attr, string[, begin, end])`. Begin/end mark
  tokenizing boundaries for selective char processing.

- [ ] **1-22: `before()` and `after()` are not Level 2.** Marked
  Level 2 but exist in all four engines (MUX `help.txt:4748, 5409`;
  PennMUSH `function.c:354, 376`; TinyMUSH `functions.c:508, 529`;
  RhostMUSH `functions.c:30931`).

- [ ] **1-22: `map()` supports pass-through arguments in MUX.**
  Additional args beyond the list pass as `%1`, `%2`, … to the mapped
  attribute (MUX `help.txt:11748`). Enables parameterized mapping
  without globals.

### Volume 1: Object / DB Functions (Ch 23)

- [ ] **1-23: `hasattr()` does NOT include inherited attributes;
  `hasattrp()` does.** MUX `help.txt:8911` is explicit. Standard
  omits `hasattrp()` entirely.

- [ ] **1-23: `nattr()` is `attrcnt()` in MUX and RhostMUSH.** Naming
  divergence not mentioned (MUX `help.txt:5169`; RhostMUSH
  `functions.c:42124`).

- [ ] **1-23: `lastcreate()` first argument optional in MUX.** MUX
  `help.txt:10095`: `lastcreate([<object>[, <type>]])`, defaults to
  executor. Standard shows `<player>` as required.

### Volume 1: Side-Effect Functions (Ch 25)

- [ ] **1-25: `lock()` returns the lock expression, not 1/0.** With
  one arg it returns the current lock; with two args it sets and
  returns the resulting lock string. MUX `help.txt:10861`; PennMUSH
  `function.c:556`.

### Volume 1: Communication System (Ch 30)

- [ ] **1-30: MUX channel commands use `@c*` prefix, not
  `@channel/<switch>`.** Actual MUX commands: `@ccreate`, `@cdestroy`,
  `@cwho`, `@clist`, `@cemit`, `@cset`, `@cboot`, `@cchown`,
  `@coflags`, `@cpflags`, `@ccharge`
  (`src/mux2.14/modules/engine/command.cpp:764-768, 842-851`). The
  chapter presents the PennMUSH `@channel/<switch>` form as an
  alternative/equivalent.

- [ ] **1-30: `@channel/on` / `@channel/off` do not exist in MUX.**
  Joining/leaving uses `addcom <alias>=<channel>` and `delcom <alias>`
  (`command.cpp:903`).

- [ ] **1-30: `@clock` is PennMUSH-only for channels.** MUX has no
  `@clock` command; channel access is via `@cset`/`@coflags`/`@cpflags`
  and the channel-object lock.

### Volume 1: Mail System (Ch 31)

- [ ] **1-31: `@malias/destroy` is wrong; MUX uses `/delete`.** Switch
  constant `MALIAS_DELETE` (`command.cpp:390`, `mail.cpp:5357`).

- [ ] **1-31: `@mailsignature` is a PennMUSH attribute name.** MUX
  uses `SIGNATURE` (`attrs.h:182`, A_SIGNATURE=203). Not interchangeable.

- [ ] **1-31: `@lock/mail` name is wrong for both engines.** MUX:
  `@lock/maillock` (`command.cpp:326`, A_LMAIL). PennMUSH:
  `@lock/Mail` (capital M, `lock.c:73`).

- [ ] **1-31: `MAILFORWARDLIST` and MailForward lock are
  PennMUSH-only.** Presented generically in the chapter
  (`extmail.c:1483`, `lock.c:82`). MUX has no auto-forward mechanism.

- [ ] **1-31: `@mailquota <player> = <limit>` wizard command does
  not exist.** PennMUSH reads `MAILQUOTA` as an attribute on the
  player (`extmail.c:1539`). MUX has no mail quota at all.

- [ ] **1-31: `/nosig` switch to `@mail/send` not in MUX.** MUX
  switch table (`command.cpp:346-383`) has `/safe` and `/unsafe` but
  no `/nosig`. Likely PennMUSH-only, not labeled as such.

### Volume 1: Networking / DB (Ch 32-33)

- [ ] **1-33: `@dump/paranoid` is PennMUSH-only.** MUX 2.14 switches
  are `/flatfile`, `/structure`, `/text` (`command.cpp:164-170`).

- [ ] **1-33: Global ACONNECT/ADISCONNECT come from `master_room`,
  not `#0`.** MUX reads `mudconf.master_room`, configurable
  (`engine_com.cpp:4287, 4450`). Same root cause as the `#0` conflation
  issue but in a different chapter.

### Volume 1: Conformance (Ch 34-37)

- [ ] **1-34: Level 1 attribute flags list uses `AF_LOCKED`.** Should
  be `AF_LOCK` (fix applied to Ch 1-06 did not propagate here). MUX
  `attrs.h:16`; `look.cpp:795`.

- [ ] **1-34: `@switch`/`@if`/`@dolist` bundled as a single Level 2
  bullet.** `@switch` and `@dolist` exist in TinyMUSH
  (`nametabs.c:647, 710`); `@if` does not exist in TinyMUSH or
  RhostMUSH. Should be split — otherwise a Level 2 implementor must
  ship all three as a unit, which no single existing engine does.

- [ ] **1-34: MISTRUST listed in Level 2 Extended Permissions.**
  MISTRUST/TRUST are PennMUSH-only (already established in Ch 1-28).
  Cannot be a Level 2 requirement if only one of four engines has it.

- [ ] **1-35: `push()`/`pop()`/`peek()` stack ops unattributed.**
  Chapter says "some implementations." MUX 2.14 `functions.cpp` does
  not register these. Likely TinyMUSH module features — needs
  per-engine attribution.

- [ ] **1-37: `@log` and `@mail` listed as "reserved for future
  standardization" but implemented in MUX 2.14.**
  `src/mux2.14/modules/engine/command.cpp:871-872` registers both.
  Contradicts the intro's claim that the standard codifies shared
  behavior.

- [ ] **1-37: `mod*()` function-name reservation is ambiguous.** The
  carve-out "(excluding `mod()` for modulo)" does not clarify whether
  the reservation applies to MUSH softcode names or to implementation
  internals. Also intersects Lua's `modf()` in MUX's bundled
  `lua54/lmathlib.c:738`.

### Volume 2: Technical Accuracy

- [ ] **2-11: `@set me/SCORE = value` attribute-value syntax is
  wrong.** `@set obj/attr = value` sets an attribute FLAG in all four
  engines. To set a value: `@set me = SCORE:<value>` or
  `&SCORE me = <value>`. Example would silently attempt to set a flag
  whose name is the computed value.

- [ ] **2-11: Register scope description is subtly wrong.** Chapter
  says registers clear "when the action list finishes." MUX help for
  `setq` says registers are cleared at the start of each interactive
  command but persist across queued actions. Distinction matters for
  `@trigger`/`@dolist` chains.

- [ ] **2-13, 2-24: Uppercase ANSI codes described as "bright."**
  Uppercase codes (`R`, `G`, `Y`, `B`, `M`, `C`, `W`, `X`) are
  BACKGROUND colors in MUX (`help ANSI CODES`, lines 4934-4960).
  Brightness is `h`. Error appears in Ch 2-13 and the Quick Reference
  Card (Ch 2-24).

- [ ] **2-14: `filter()` requires exact `1`, not truthy.** MUX
  `help filter`, line 8048. `2` or `yes` would fail. Should either
  clarify or steer readers to `filterbool()` (PennMUSH).

- [ ] **2-17: `@channel/emit` does not exist in any engine.** MUX:
  `@cemit[/noheader] <channel>=<message>`. PennMUSH:
  `@cemit[/noisy|/silent] <channel>=<message>`. The command as used
  in the chapter is invented.

- [ ] **2-17: `@channel/mute` vs `@channel/gag` conflated.** Both are
  PennMUSH-only. `@channel/gag` suppresses messages; `@channel/mute`
  suppresses connect/disconnect notices. The chapter attributes gag
  behavior to the mute command. MUX uses `<alias> off` / `<alias> on`.

- [ ] **2-17: `@channel/add`, `@clock/join`, `@clock/speak`,
  `@channel/priv` are all PennMUSH-specific syntax.** Presented as
  generic. MUX equivalents use `@ccreate`, `@cset`, `@coflags`,
  `@cpflags` (`pennchat.hlp` 185, 371, 383 vs `help @ccreate`,
  `@cset`, `@cpflags`).

- [ ] **2-18: MUX mail aliases require `*` prefix when used.**
  Chapter shows `@mail staff = ...` after `@malias staff = ...`. Must
  be `@mail *staff = ...` in MUX (`help @malias`, line 2734). Without
  `*`, MUX resolves to a player name.

- [ ] **2-18: `@mail/forward` is spelled `/fwd`.** Both MUX and
  PennMUSH use the short form (`help mail-sending2`, line 11490). No
  `/forward` switch exists.

- [ ] **2-18: `@mail/status` does not exist.** Not in MUX help, not
  in PennMUSH help. Likely confused with PennMUSH `mailstats()`
  function or third-party softcode.

- [ ] **2-18: Multi-line mail composition terminator is `--`, not
  `.`.** Chapter uses `.` to send; MUX uses `--`
  (`help mail-sending`, line 11455). A lone `.` is not recognized.

- [ ] **2-19: BBS chapter's command set is Myrddin's BBS, not
  standard.** `+bblist`, `+bbread`, `+bbpost`, etc. are Myrddin's
  specific command names — not universal MUSH behavior. Anomaly Jobs
  and RhostMUSH native `+bb` use different syntaxes. No attribution
  is given; readers will assume standard.

- [ ] **2-20: Binary name `netmush` with config `mush.conf` is a
  cross-engine jumble.** MUX uses `netmux -c netmux.conf`
  (`Startmux:49`, `game/netmux.conf`). PennMUSH uses `netmush`. The
  example combines PennMUSH's binary name with an arbitrary config
  filename. Should note per-engine binary and config conventions.

- [ ] **2-20: `fork_dump yes` description is outdated for MUX 2.14.**
  Chapter says it avoids player lag during DB saves. MUX 2.14 uses
  WAL checkpoints for periodic saves, which never fork regardless of
  this setting (`src/mux2.14/game/text/wizhelp.txt:2704`;
  `src/mux2.14/UPGRADING.md:143`). `fork_dump` now only affects
  `@dump/flatfile` exports.

- [ ] **2-22: `@find =THING` is not valid syntax.** `@find` takes a
  name substring: `@find <name>[,<low>[,<high>]]` (`help @find`, line
  1835). Finding objects by type requires
  `@search type=THING owner=me`. The example on the same line works;
  the `@find` form does not.
