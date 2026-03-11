# Issues

Consolidated issues from three independent reviews (Claude, Codex,
Gemini) cross-referencing the book against source code in `./src/`
(TinyMUSH 4.0, TinyMUX 2.13, RhostMUSH, PennMUSH) and the comparative
survey documents in `./surveys/`.

---

## Infrastructure

- [ ] **mdfix batch processing bug.** When processing multiple files in
  a single invocation, mdfix sometimes overwrites a file with the
  content of the preceding file. Affected 2-18, 2-21, 2-25 in this
  session. Workaround: process files one at a time. Root cause needs
  investigation in `mdfix.rl`.

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

- [ ] **`#0` conflated as universal master room, start room, and
  global-command room.** MUX separates `player_starting_room` from
  `master_room` (`CONFIGURATION.md:49-55`). RhostMUSH has
  `player_starting_room` as a config parameter. The book hardcodes one
  deployment pattern as a family-wide invariant. Should be
  implementation-defined or "common default." [Codex, Claude]

- [ ] **"Every player can build" (2-01) is incorrect.** All four
  implementations gate building behind permissions: MUX marks @create,
  @dig, @open with `CA_GBL_BUILD` (`command.cpp:734-750`). PennMUSH
  has `restrict_building` and `Builder(x)` (`conf.c:1295`,
  `mushdb.h:15-18`). The granularity also varies: MUX uses a global
  flag, PennMUSH uses per-player powers and config, RhostMUSH has its
  own model. [Codex, Surveys]

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

---

## Volume 1: High-Impact Factual Errors

- [ ] **1-05: Dropto behavior description is wrong.** STICKY on an
  object sends it HOME, not to the dropto. Room sweep behavior
  (objects to dropto when all players leave) requires the room itself
  to have STICKY -- omitted. (MUX `move.cpp:255-308`) [Claude]

- [ ] **1-05: `type()` return for GARBAGE is not universal.** Book
  claims all four return `GARBAGE`. TinyMUX/TinyMUSH return
  `#-1 ILLEGAL TYPE`; RhostMUSH returns `#-1 NOT FOUND`. Only
  PennMUSH returns `GARBAGE`. [Gemini]

- [ ] **1-06: `get()` inheritance claim is wrong.** Book says `get()`
  retrieves without inheritance. All four implementations walk the
  parent chain: MUX `functions.cpp:2066` calls `atr_pget_LEN`;
  PennMUSH `attrib.c:1184` calls `atr_get_with_parent()`. [Claude]

- [ ] **1-06: Attribute flag `AF_LOCKED` should be `AF_LOCK`.** All
  four implementations use `AF_LOCK` internally and in user-visible
  displays, not `AF_LOCKED`. [Gemini]

- [ ] **1-09: $-command search order is internally inconsistent.** The
  numbered list says Player > Inventory > Room > Objects-in-room. MUX
  source (`command.cpp:2645-2673`) shows Player > Objects-in-room >
  Room > Inventory. The implementation note at the bottom contradicts
  the list. [Claude]

- [ ] **1-09, 1-11: `@force` described as immediate execution.** Both
  TinyMUSH and TinyMUX queue `@force` by default; only `@force/now`
  is immediate. (MUX `wiz.cpp:328-339`) [Claude]

- [ ] **1-15: Movement message sequence is wrong.** LEAVE/OLEAVE/ALEAVE
  fire BEFORE `move_object`, not after. Steps 3-7 are misordered.
  Actual: SUCC/OSUCC/ASUCC on exit -> LEAVE/OLEAVE/ALEAVE + OXENTER
  -> move -> DROP/ODROP/ADROP -> MOVE/OMOVE/AMOVE on player ->
  ENTER/OENTER/AENTER + OXLEAVE. (MUX `move.cpp:358-367`) [Claude]

- [ ] **1-15: MOVE/OMOVE/AMOVE attributes omitted entirely.** After
  DROP/ODROP/ADROP, the player's own MOVE, OMOVE, AMOVE fire. Not
  mentioned in the book. [Claude]

- [ ] **1-15: Teleport message sequence is reversed.** OXTPORT fires
  BEFORE the move; TPORT/OTPORT/ATPORT fires AFTER. Book has it
  backwards. (MUX `move.cpp:432-441`) [Claude]

- [ ] **1-16: HAVEN blocking @pemit is incorrect.** HAVEN blocks pages,
  not @pemit. No implementation checks HAVEN in the pemit path.
  PEMIT_ALL power is PennMUSH-only. [Claude]

- [ ] **1-16: Nospoof format is reversed.** Book shows
  `[#42(Bob)] ...` but actual format is `[Bob(#42)]` -- name first,
  then dbref. (MUX `game.cpp:723-727`) [Claude]

- [ ] **1-18: @verb syntax is significantly oversimplified.** The
  actual arguments are attribute names for the did_it pipeline, not
  direct text messages. Argument count and meaning are wrong.
  (TinyMUSH `predicates.c:3068-3194`) [Claude]

- [ ] **1-29: Zone lock mechanism varies drastically but only one model
  is described.** PennMUSH uses `@lock/zone`; TinyMUX uses the enter
  lock on the ZMO; TinyMUSH uses the control lock + requires
  CONTROL_OK. These are fundamentally different. [Claude, Codex]

---

## Volume 1: Medium-Impact Issues

### Flags (Ch 7)

- [ ] **1-07: Several flags incorrectly listed with no display
  character.** OPAQUE='O', LIGHT='l', AUDIBLE='a', ROYALTY='Z',
  PARENT_OK='Y', OPEN_OK='z' in MUX. (`flags.cpp:340-381`)
  [Claude, Gemini]

- [ ] **1-07: IMMORTAL permission listed as "God" but source shows
  "Wizard".** Both TinyMUSH and MUX use `fh_wiz`.
  (`flags.cpp:361`) [Claude]

- [ ] **1-07: ZONE_MASTER, ZONE_CONTENTS, ZONE_PARENT flags do not
  exist with those names.** TinyMUSH has "ZONE"; PennMUSH has
  "SHARED" (aliased "ZONE") for players only. [Claude]

- [ ] **1-07: CONTROL_OK does not exist in TinyMUX.**
  TinyMUSH-only. [Claude]

- [ ] **1-07: GUEST is a power in TinyMUX, not a flag.**
  (`powers.h:41`) [Claude]

- [ ] **1-07: INDESTRUCTIBLE listed as RhostMUSH-only but exists in
  TinyMUX too.** (`flags.h:111`) [Claude]

- [ ] **1-07: `hasflag()` vs `has_flag()` naming.** TinyMUX uses
  `has_flag()` (with underscore); TinyMUSH uses `hasflag()`. Softcode
  using one will break on the other. The standard should note the
  variation or recommend one with the other as required alias.
  [Gemini]

- [ ] **1-07: SEETHRU vs TRANSPARENT naming.** MUX primary name is
  often `SEETHRU` internally. Standard calls it `TRANSPARENT` with
  `SEETHRU` as alias. Should standardize clearly. [Gemini]

### Attributes (Ch 6)

- [ ] **1-06: Standard lock attribute names don't match
  implementations.** Book uses LENTER, LLEAVE, LOPEN, LCONTROL.
  TinyMUSH/MUX use EnterLock, LeaveLock, OpenLock, ControlLock.
  PennMUSH uses named locks ("Enter", "Leave"). [Gemini, Claude]

- [ ] **1-06: `AF_DARK` vs `AF_MDARK` vs `AF_ODARK` definitions are
  blurred.** MUX has `AF_ODARK` (owner only) which the standard
  doesn't account for. [Gemini]

- [ ] **1-06: `AF_NOPROG` flag omitted.** Present in both TinyMUX and
  TinyMUSH (prevents $-command search). Should be in the standard
  attribute flags table. [Gemini]

### Commands (Ch 15-19)

- [ ] **1-15: Fallback home described as "#0" is inaccurate.** MUX
  falls back to `default_home`, then `start_home`, then `start_room`.
  (`object.cpp:371-382`) [Claude]

- [ ] **1-15: TOFAIL/OTOFAIL/ATOFAIL teleport failure attributes not
  mentioned.** [Claude]

- [ ] **1-16: @femit does not exist in PennMUSH.** Should be marked
  Level 2 or noted. [Claude]

- [ ] **1-16: LSPEECH lock requires Auditorium flag in MUX/TinyMUSH.**
  Without the flag, the lock is ignored. (`speech.cpp:75-82`) [Claude]

- [ ] **1-17: @name does not require password for player renaming.**
  None of the four implementations require it. May be legacy. [Claude]

- [ ] **1-18: @undestroy is PennMUSH-only.** Others clear the GOING
  flag with `@set`. [Claude]

- [ ] **1-19: @shutdown/abort does not cancel pending shutdown.**
  TinyMUSH `/abort` means "dump core." MUX has no switches. PennMUSH
  has /panic, /reboot, /paranoid but not /abort. [Claude]

- [ ] **1-19: @dump/paranoid is PennMUSH-only.** [Claude]

- [ ] **1-19: @allhalt is PennMUSH-only.** Others use
  `@halt/all`. [Claude]

- [ ] **1-19: @uptime does not exist in MUX or TinyMUSH.** [Claude]

- [ ] **1-19: @if/@ifelse availability varies.** MUX has `@if`.
  PennMUSH has `@ifelse`. TinyMUSH and RhostMUSH have
  neither. [Claude]

- [ ] **1-19: @dolist `#@` starts from 1, not 0.** `number` is
  incremented before use. (`walkdb.cpp:82`) [Claude]

- [ ] **1-19: @doing does not exist in PennMUSH.** Uses `@poll` and
  the DOING logged-out command. [Claude]

- [ ] **1-19: @function permission described as GLOBAL_FUNCS power.**
  MUX and TinyMUSH require GOD. RhostMUSH requires WIZARD. PennMUSH
  has the Global_Funcs power. [Claude]

### Locks and Systems (Ch 27-33)

- [ ] **1-27: Lock attribute names diverge.** Book uses TinyMUSH/MUX
  naming (LENTER, LLEAVE). PennMUSH uses named locks. PennMUSH has
  additional types not mentioned: Listen, From, Pay, Chzone, Dropto,
  Interact, MailForward, Take, InFilter, DropIn. [Claude]

- [ ] **1-27: LTELOUT does not exist in PennMUSH.** [Claude]

- [ ] **1-30: `@channel/add` syntax is PennMUSH-specific.** TinyMUX
  uses `@channel/create`. [Claude]

- [ ] **1-33: Exits field in database table says "rooms only."** Exits
  can be attached to things and players too. [Claude]

---

## Volume 1: Low-Impact Issues

- [ ] **1-04: `#-4` NOPERM described as TinyMUX-only but also exists
  in RhostMUSH.** (`db.h:146`) [Claude]

- [ ] **1-05: TYPE_ZONE (type code 4) reserved by RhostMUSH.** MUX
  also reserves this space. Worth noting. [Gemini]

- [ ] **1-09: `#` prefix command behaves differently in PennMUSH.**
  Goes through `parse_force()` requiring `Mobile(player)` and
  control. [Claude]

- [ ] **1-16: Page recipient separator supports comma separation too,
  not just spaces.** (`speech.cpp:607-660`) [Claude]

- [ ] **1-18: @pemit target list supports comma separation, not just
  spaces.** (`speech.cpp:1315`) [Claude]

- [ ] **1-18: examine /owner switch is TinyMUSH-only, not just
  Level 2.** MUX has /brief, /debug, /full, /parent. [Claude]

- [ ] **1-19: DARK flag with CAN_HIDE power for WHO visibility is
  oversimplified.** Relationship between DARK, UNFINDABLE, Can_Dark,
  Can_Hide, and Hidden varies by implementation. [Claude]

- [ ] **1-29: CONTROL_OK requirement for TinyMUSH zone control not
  mentioned.** [Claude]

- [ ] **1-29: Zone event attributes (ZENTER, OZENTER, AZENTER) may be
  PennMUSH-specific.** [Claude]

- [ ] **1-32: IDLE power name varies.** MUX: `idle`.
  PennMUSH: `Idle`. [Claude]

---

## Volume 1: Functions (Ch 20-26)

- [ ] **1-20: `squish()` described without optional character argument.**
  Ch 26 correctly shows the optional arg. Both MUX and PennMUSH
  support it. [Claude]

- [ ] **1-26: `while()` marked Level 2 but only in TinyMUSH and
  RhostMUSH.** Not in MUX or PennMUSH. [Claude]

- [ ] **1-24/1-26: Duplicate listings of `isnum()`, `isint()`,
  `isdbref()`, `isobjid()`, `isword()`, `valid()`.** Content is
  consistent but redundant across both chapters. [Claude]

---

## Volume 2: Technical Accuracy

- [ ] **2-01: "Every player can build" is incorrect.** Building is
  gated behind permissions in all four implementations. [Codex]

- [ ] **2-06: STICKY flag description is incorrect.** Same dropto issue
  as 1-05. STICKY sends object HOME, not to dropto. [Claude]

- [ ] **2-07: CONFORMAT and EXITFORMAT presented as universal but are
  PennMUSH-specific.** [Claude]

- [ ] **2-10: `first()` example with 3 arguments is incorrect.**
  `first()` accepts at most 2 arguments (list, delimiter). [Claude]

- [ ] **2-12: `#@` position counter described as starting at 0;
  starts at 1.** Same issue as 1-19. [Claude]

- [ ] **2-12: `if()` function not universal.** PennMUSH and MUX have
  `if()`; TinyMUSH and RhostMUSH only have `ifelse()`. The chapter
  should present `ifelse()` as the more universal function and note
  that `if()` is available on PennMUSH and MUX. [Claude, Surveys]

- [ ] **2-12: `@if`/`@ifelse` command does not exist on TinyMUSH or
  RhostMUSH.** [Claude]

- [ ] **2-13: `repeat()` example output has wrong character count.**
  `repeat(=-, 20)` should produce 40 characters, not 44. [Claude]

- [ ] **2-14: Sort type `i` described as "integer" but means
  "case-insensitive."** Correct type for numeric sort is `n`.
  (`funlist.c:168`) [Claude]

- [ ] **2-15: $-command search order lists master room as "#0".**
  PennMUSH master room is configurable. [Claude]

- [ ] **2-16: ACONNECT example uses `mail(me)` which is a loadable
  module in TinyMUSH, not core.** [Claude]

---

## Volume 2: Coverage Gaps

- [ ] **No coverage of zones.** Mentioned briefly in Ch 15-16
  references but never introduced or explained. [Claude]

- [ ] **No coverage of @power command.** Ch 23 uses `@power Morgan =
  announce` but powers are never explained as a concept. [Claude]

- [ ] **No coverage of @force command.** Mentioned in security warnings
  (Ch 23) but never formally documented. [Claude]

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

- [ ] **1-19: `@function` permission model diverges more than
  documented.** Beyond the GOD/WIZARD/Global_Funcs variation already
  noted, RhostMUSH's entire permission model is different (powers +
  depowers + toggles), so "requires WIZARD" is itself an
  oversimplification of Rhost's layered permission checking. [Surveys]
