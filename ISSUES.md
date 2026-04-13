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

- [x] **1-01: Still cites "TinyMUX (version 2.13)."** Updated to 2.14.

- [x] **1-02: Terminology chapter conflates master room with start
  room.** Master room definition rewritten as implementation-defined
  with dbref noted as configurable; new "start room" term added.

- [x] **1-14: `iter()` appears twice in the Function Categories
  table.** Misc row updated to list `case()`/`null()` instead of the
  duplicates.

### Volume 1: Percent Codes (Ch 13)

- [x] **1-13: `%c` is a color code in MUX 2.14, not "last command."**
  Table entry rewritten with explicit per-engine caveats and a note
  recommending `%m` for portable last-command substitution.

- [x] **1-13: `%?` return format diverges.** Entry now describes
  PennMUSH's two-value return, TinyMUSH/RhostMUSH's single-value
  return, and TinyMUX's lack of `%?` substitution.

- [x] **1-13: `%=<N>` works as positional-arg reference in MUX.**
  Table entry extended to document TinyMUX's numeric positional-arg
  interpretation of `%=<N>`.

### Volume 1: Action Lists / Queue (Ch 11)

- [x] **1-11: Power names are PennMUSH flag names, not MUX powers.**
  Chapter now presents `HUGE_QUEUE`, `HALT_ANYTHING`, and `PS_ALL` as
  PennMUSH examples with cross-engine equivalents noted; `@allhalt`
  and `@halt/all` are now presented together.

- [x] **1-11: `@wait/until <epoch>` switch omitted.** New subsection
  documents the absolute-time form as implementation-defined.

- [x] **1-11: Semaphore-plus-timeout `@wait` syntax description is
  misleading.** Rewritten to describe the `<value>` slot's numeric-vs-
  attribute-name overload and the mutual exclusivity of the two uses.

### Volume 1: String Functions (Ch 20)

- [x] **1-20: `escape()` prefixes with `\`, not `%`.** Fixed.

- [x] **1-20: `secure()` replaces characters with spaces, does not
  remove them.** Fixed.

- [x] **1-20: `lpos()` returns all match positions 0-based, not "last
  occurrence."** Rewritten to describe actual behavior and argument
  order; Level 2 tag removed.

- [x] **1-20: `regedit()` accepts multiple regex/replacement pairs.**
  Signature and subgroup range updated.

- [x] **1-20: `speak()` has 2–7 arguments.** Extended signature
  documented with implementation-defined optional arguments.

- [x] **1-20/1-24: `comp()` accepts optional type argument.** Optional
  type arg added in both chapters; case-insensitivity claim replaced
  with per-engine notes.

### Volume 1: Math / Logic Functions (Ch 21)

- [x] **1-21: `mod()` semantics inverted.** Fixed: `mod()` now
  documented as floor division (divisor sign); `remainder()` as
  truncated division (dividend sign).

- [x] **1-21: `rand()` argument order reversed and range is
  inclusive.** Signature updated to `rand([<lower>,] <upper>)` with
  half-open one-arg form and closed two-arg range.

### Volume 1: List Functions (Ch 22)

- [x] **1-22: `sort()` type `i` is case-insensitive alphabetic, not
  integer.** Table corrected; type `n` clarified as numeric; portable
  usage note added.

- [x] **1-22: `sort()` missing MUX-only types.** TinyMUX types
  `u`/`c`/`a`/`?` now documented as engine-specific additions.

- [x] **1-22: `index()` 4th arg is field count, not end position.**
  Signature relabeled from `<end>` to `<count>` with clarifying prose.

- [x] **1-22: `foreach()` takes begin/end boundary args, not a list
  delimiter.** Rewritten in Ch 26 (where `foreach()` actually lives).

- [x] **1-22: `before()` and `after()` are not Level 2.** Level 2
  tags removed.

- [x] **1-22: `map()` supports pass-through arguments in MUX.**
  Signature extended with optional pass-through args as
  implementation-defined.

### Volume 1: Object / DB Functions (Ch 23)

- [x] **1-23: `hasattr()` does NOT include inherited attributes;
  `hasattrp()` does.** `hasattr()` description corrected;
  `hasattrp()` added as the inheriting variant; `hasattrval()` note
  added.

- [x] **1-23: `nattr()` is `attrcnt()` in MUX and RhostMUSH.** Entry
  retitled to show both names with per-engine notes.

- [x] **1-23: `lastcreate()` first argument optional in MUX.**
  Signature updated to show both arguments as optional with portable
  usage note.

### Volume 1: Side-Effect Functions (Ch 25)

- [x] **1-25: `lock()` returns the lock expression, not 1/0.**
  Signature rewritten with one-arg query form and two-arg set form;
  return-value note added to discourage boolean testing.

### Volume 1: Communication System (Ch 30)

- [x] **1-30: MUX channel commands use `@c*` prefix, not
  `@channel/<switch>`.** Chapter now introduces the two command
  families up front; examples throughout show both forms side-by-side.

- [x] **1-30: `@channel/on` / `@channel/off` do not exist in MUX.**
  Joining/leaving section rewritten: `/on`/`/off` attributed to
  PennMUSH; `addcom`/`delcom` presented as TinyMUX's exclusive
  mechanism and PennMUSH's preferred one.

- [x] **1-30: `@clock` is PennMUSH-only for channels.** Lock section
  rewritten with per-engine command surface noted.

### Volume 1: Mail System (Ch 31)

- [x] **1-31: `@malias/destroy` is wrong; MUX uses `/delete`.**
  Alias section now lists both spellings as implementation-defined.

- [x] **1-31: `@mailsignature` is a PennMUSH attribute name.**
  Signature section rewritten to attribute the name per-engine
  (PennMUSH `MAILSIGNATURE`; TinyMUX `SIGNATURE`).

- [x] **1-31: `@lock/mail` name is wrong for both engines.**
  Permissions section rewritten with `@lock/maillock` (TinyMUX) and
  `@lock/Mail` (PennMUSH) attributed explicitly.

- [x] **1-31: `MAILFORWARDLIST` and MailForward lock are
  PennMUSH-only.** Auto-forward now marked as PennMUSH-specific with
  no equivalent in other engines.

- [x] **1-31: `@mailquota <player> = <limit>` wizard command does
  not exist.** Quota section rewritten to show PennMUSH's
  attribute-based mechanism and note that other engines lack quotas.

- [x] **1-31: `/nosig` switch to `@mail/send` not in MUX.** Switch
  table now tags `/nosig` as PennMUSH-specific with a portability
  note.

### Volume 1: Networking / DB (Ch 32-33)

- [x] **1-33: `@dump/paranoid` is PennMUSH-only.** Dump command
  rewritten with per-engine switch sets noted.

- [x] **1-33: Global ACONNECT/ADISCONNECT come from `master_room`,
  not `#0`.** Fixed in Ch 32 (where the section actually lives):
  master room dbref now presented as implementation-defined and read
  from configuration.

### Volume 1: Conformance (Ch 34-37)

- [x] **1-34: Level 1 attribute flags list uses `AF_LOCKED`.** Fixed
  to `AF_LOCK`.

- [x] **1-34: `@switch`/`@if`/`@dolist` bundled as a single Level 2
  bullet.** Split: `@switch`/`@dolist` remain Level 2; `@if`/`@ifelse`
  noted as engine-specific with a pointer to function forms.

- [x] **1-34: MISTRUST listed in Level 2 Extended Permissions.**
  Removed from the Level 2 list; added a note marking MISTRUST/TRUST
  as an optional PennMUSH-specific feature.

- [x] **1-35: `push()`/`pop()`/`peek()` stack ops unattributed.**
  Entry rewritten to attribute the API to TinyMUSH's stack module
  and note non-portability.

- [x] **1-37: `@log` and `@mail` listed as "reserved for future
  standardization" but implemented in MUX 2.14.** Reserved-command
  section now acknowledges existing per-engine implementations with
  cross-references.

- [x] **1-37: `mod*()` function-name reservation is ambiguous.**
  Reservation now explicitly scoped to MUSHcode softcode names and
  grandfathers existing `mod()`.

### Volume 2: Technical Accuracy

- [x] **2-11: `@set me/SCORE = value` attribute-value syntax is
  wrong.** Example rewritten to use `&SCORE me = <value>` with an
  explicit warning about `@set obj/attr=value` being the flag-setting
  form.

- [x] **2-11: Register scope description is subtly wrong.** Scope
  section rewritten to describe clear-on-new-command, persist-across-
  queue behavior.

- [x] **2-13, 2-24: Uppercase ANSI codes described as "bright."**
  Both chapters corrected: uppercase is background, `h` is highlight.

- [x] **2-14: `filter()` requires exact `1`, not truthy.** Description
  rewritten with the exact-1 requirement and pointers to `t()` and
  PennMUSH's `filterbool()`.

- [x] **2-17: `@channel/emit` does not exist in any engine.** Replaced
  with `@cemit` in the talking-without-alias section.

- [x] **2-17: `@channel/mute` vs `@channel/gag` conflated.** Muting
  section rewritten: TinyMUX uses alias on/off; PennMUSH's `gag` vs
  `mute` distinction clarified.

- [x] **2-17: `@channel/add`, `@clock/join`, `@clock/speak`,
  `@channel/priv` are all PennMUSH-specific syntax.** Channel-creation,
  lock, and settings sections rewritten with per-engine attribution
  (PennMUSH `@channel/*` vs TinyMUX `@c*`/`@cset`).

- [x] **2-18: MUX mail aliases require `*` prefix when used.** Alias
  section shows both `*staff` (TinyMUX) and `+staff` (PennMUSH) with
  a note about engine dispatch.

- [x] **2-18: `@mail/forward` is spelled `/fwd`.** Corrected; note
  added that `/forward` is not recognized.

- [x] **2-18: `@mail/status` does not exist.** Entire subsection
  removed.

- [x] **2-18: Multi-line mail composition terminator is `--`, not
  `.`.** TinyMUX composition example rewritten to use `--` with an
  explicit warning that `.` does not send.

- [x] **2-19: BBS chapter's command set is Myrddin's BBS, not
  standard.** Overview paragraph rewritten to attribute the example
  commands to Myrddin's BBS with a pointer to local help for other
  packages.

- [x] **2-20: Binary name `netmush` with config `mush.conf` is a
  cross-engine jumble.** Config-file section lists per-engine
  filenames; start-command examples show per-engine invocations.

- [x] **2-20: `fork_dump yes` description is outdated for MUX 2.14.**
  Fixed in the appropriate chapter (2-22, which owns the
  `fork_dump` discussion): note added explaining MUX 2.14's WAL
  checkpoint model.

- [x] **2-22: `@find =THING` is not valid syntax.** Example replaced
  with a name-substring usage and a note explaining the correct form.
