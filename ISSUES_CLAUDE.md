# Issues

Issues identified by cross-referencing the book against source code in
`./src/` (TinyMUSH 4.0, TinyMUX 2.13, RhostMUSH, PennMUSH).

## Infrastructure

- [ ] **mdfix batch processing bug.** When processing multiple files in
  a single invocation, mdfix sometimes overwrites a file with the
  content of the preceding file. Affected 2-18, 2-21, 2-25 in this
  session. Workaround: process files one at a time. Root cause needs
  investigation in `mdfix.rl`.

---

## Volume 1: High-Impact Factual Errors

- [ ] **1-05 (Object Types): Dropto behavior description is wrong.**
  The book says STICKY on an object sends it to the dropto. Source
  shows STICKY sends dropped objects HOME, not to the dropto. Also,
  room sweep behavior (sending objects to dropto when all players
  leave) requires the room itself to have STICKY -- omitted from the
  book. (MUX `move.cpp:255-308`)

- [ ] **1-06 (Attributes): `get()` inheritance claim is wrong.** The
  book says `get()` retrieves without inheritance. All four
  implementations walk the parent chain: MUX `functions.cpp:2066`
  calls `atr_pget_LEN`; PennMUSH `attrib.c:1184` calls
  `atr_get_with_parent()`.

- [ ] **1-09 (Command Parsing): $-command search order is internally
  inconsistent.** The numbered list says Player > Inventory > Room >
  Objects-in-room. MUX source (`command.cpp:2645-2673`) shows
  Player > Objects-in-room > Room > Inventory. The implementation
  note at the bottom of the same section correctly describes the MUX
  order, contradicting the list above it.

- [ ] **1-09, 1-11: `@force` described as immediate execution.** Both
  TinyMUSH and TinyMUX queue `@force` by default; only `@force/now`
  is immediate. (MUX `wiz.cpp:328-339`)

- [ ] **1-15 (Movement): Movement message sequence is wrong.** The
  LEAVE/OLEAVE/ALEAVE messages fire BEFORE `move_object`, not after.
  The book has steps 3-7 in the wrong order. Actual sequence:
  SUCC/OSUCC/ASUCC on exit, then LEAVE/OLEAVE/ALEAVE + OXENTER,
  then move, then DROP/ODROP/ADROP, then MOVE/OMOVE/AMOVE on player,
  then ENTER/OENTER/AENTER + OXLEAVE. (MUX `move.cpp:358-367`)

- [ ] **1-15: MOVE/OMOVE/AMOVE attributes omitted entirely.** After
  DROP/ODROP/ADROP, the player's own MOVE, OMOVE, AMOVE fire. The
  book does not mention this step at all.

- [ ] **1-15: Teleport message sequence is reversed.** OXTPORT fires
  BEFORE the move; TPORT/OTPORT/ATPORT fires AFTER. The book has it
  backwards. (MUX `move.cpp:432-441`)

- [ ] **1-16 (Communication): HAVEN blocking @pemit is incorrect.**
  HAVEN blocks pages, not @pemit. No implementation checks HAVEN in
  the pemit path. PEMIT_ALL power is PennMUSH-only.

- [ ] **1-16: Nospoof format is reversed.** Book shows
  `[#42(Bob)] ...` but actual format is `[Bob(#42)]` -- name first,
  then dbref. (MUX `game.cpp:723-727`)

- [ ] **1-18 (Object Manipulation): @verb syntax is significantly
  oversimplified.** The actual arguments are attribute names for the
  did_it pipeline, not direct text messages. Argument count and
  meaning are wrong. (TinyMUSH `predicates.c:3068-3194`)

- [ ] **1-29 (Zones): Zone lock mechanism varies drastically but only
  one model is described.** PennMUSH uses `@lock/zone`; TinyMUX uses
  the enter lock on the ZMO; TinyMUSH uses the control lock + requires
  CONTROL_OK on the controlled object. These are fundamentally
  different.

---

## Volume 1: Medium-Impact Issues

### Flags and Powers (Ch 7-8)

- [ ] **1-07: Several flags incorrectly listed with no display
  character.** OPAQUE='O', LIGHT='l', AUDIBLE='a', ROYALTY='Z',
  PARENT_OK='Y', OPEN_OK='z' in MUX. (MUX `flags.cpp:340-381`)

- [ ] **1-07: IMMORTAL permission listed as "God" but source shows
  "Wizard".** Both TinyMUSH and MUX use `fh_wiz`. (MUX
  `flags.cpp:361`)

- [ ] **1-07: ZONE_MASTER, ZONE_CONTENTS, ZONE_PARENT flags do not
  exist with those names.** TinyMUSH has "ZONE"; PennMUSH has
  "SHARED" (aliased as "ZONE") for players only.

- [ ] **1-07: CONTROL_OK does not exist in TinyMUX.** TinyMUSH-only.

- [ ] **1-07: GUEST is a power in TinyMUX, not a flag.**
  (MUX `powers.h:41`)

- [ ] **1-07: INDESTRUCTIBLE listed as RhostMUSH-only but exists in
  TinyMUX too.** (MUX `flags.h:111`)

- [ ] **1-08: Power names don't match any implementation's user-facing
  names.** Book uses names like CAN_BUILD, PEMIT_ALL, TEL_ANYWHERE.
  MUX uses: builder, announce, tel_anywhere. PennMUSH uses: Builder,
  Announce, Tport_Anywhere. The book appears to use PennMUSH internal
  C macro names.

- [ ] **1-08: Several powers listed are PennMUSH-only but not marked.**
  PEMIT_ALL, CREATE_PLAYER, GLOBAL_FUNCS, HUGE_QUEUE, LOGIN_ANYTIME,
  OPEN_ANYWHERE.

### Commands (Ch 15-19)

- [ ] **1-15: Fallback home described as "#0" is inaccurate.** MUX
  falls back to `default_home`, then `start_home`, then `start_room`.
  (MUX `object.cpp:371-382`)

- [ ] **1-15: TOFAIL/OTOFAIL/ATOFAIL teleport failure attributes not
  mentioned.**

- [ ] **1-16: @femit does not exist in PennMUSH.** Should be marked
  Level 2 or noted.

- [ ] **1-16: LSPEECH lock requires Auditorium flag in MUX/TinyMUSH.**
  Without the flag, the lock is ignored.
  (MUX `speech.cpp:75-82`)

- [ ] **1-17: @name does not require password for player renaming.**
  None of the four implementations require it. May be legacy claim.

- [ ] **1-18: @undestroy is PennMUSH-only.** Other implementations
  clear the GOING flag with `@set`.

- [ ] **1-19: @shutdown/abort does not cancel pending shutdown.**
  TinyMUSH `/abort` means "dump core" (SHUTDN_COREDUMP). MUX has no
  switches. PennMUSH has /panic, /reboot, /paranoid but not /abort.

- [ ] **1-19: @dump/paranoid is PennMUSH-only.**

- [ ] **1-19: @allhalt is PennMUSH-only.** Other implementations use
  `@halt/all`.

- [ ] **1-19: @uptime does not exist in MUX or TinyMUSH.**

- [ ] **1-19: @if/@ifelse availability varies.** MUX has `@if`.
  PennMUSH has `@ifelse`. TinyMUSH and RhostMUSH have neither.

- [ ] **1-19: @dolist `#@` starts from 1, not 0.** `number` is
  incremented before use. (MUX `walkdb.cpp:82`)

- [ ] **1-19: @doing does not exist in PennMUSH.** PennMUSH uses
  `@poll` and the DOING logged-out command.

- [ ] **1-19: @function permission described as GLOBAL_FUNCS power.**
  MUX and TinyMUSH require GOD. RhostMUSH requires WIZARD. PennMUSH
  has the Global_Funcs power.

### Locks and Systems (Ch 27-33)

- [ ] **1-27: Lock attribute names diverge between implementations.**
  Book uses TinyMUSH/MUX naming (LENTER, LLEAVE). PennMUSH uses named
  locks ("Enter", "Leave"). PennMUSH has additional lock types not
  mentioned: Listen, From, Pay, Chzone, Dropto, Interact,
  MailForward, Take, InFilter, DropIn.

- [ ] **1-27: LTELOUT does not exist in PennMUSH.**

- [ ] **1-30: `@channel/add` syntax is PennMUSH-specific.** TinyMUX
  uses `@channel/create`.

- [ ] **1-33: Exits field in database table says "rooms only."** Exits
  can be attached to things and players too.

---

## Volume 1: Low-Impact Issues

- [ ] **1-04: `#-4` NOPERM described as TinyMUX-only but also exists
  in RhostMUSH.** (RhostMUSH `db.h:146`)

- [ ] **1-09: `#` prefix command behaves differently in PennMUSH.**
  Goes through `parse_force()` requiring `Mobile(player)` and control.

- [ ] **1-16: Page recipient separator supports comma separation too,
  not just spaces.** (MUX `speech.cpp:607-660`)

- [ ] **1-18: @pemit target list supports comma separation, not just
  spaces.** (MUX `speech.cpp:1315`)

- [ ] **1-18: examine /owner switch is TinyMUSH-only, not just Level
  2.** MUX has /brief, /debug, /full, /parent.

- [ ] **1-19: DARK flag with CAN_HIDE power for WHO visibility is
  oversimplified.** Relationship between DARK, UNFINDABLE, Can_Dark,
  Can_Hide, and Hidden varies by implementation.

- [ ] **1-29: CONTROL_OK requirement for TinyMUSH zone control not
  mentioned.**

- [ ] **1-29: Zone event attributes (ZENTER, OZENTER, AZENTER) may be
  PennMUSH-specific.** Should verify cross-implementation support.

- [ ] **1-32: IDLE power name varies.** MUX: `idle`. PennMUSH: `Idle`.

---

## Volume 1: Functions (Ch 20-26)

- [ ] **1-20: `squish()` described without optional character argument.**
  Ch 26 correctly shows `squish(<string> [, <character>])`. Ch 20
  shows only `squish(<string>)`. Both MUX and PennMUSH support the
  optional argument.

- [ ] **1-26: `while()` marked Level 2 but only in TinyMUSH and
  RhostMUSH.** Not in MUX or PennMUSH.

- [ ] **1-24/1-26: Duplicate listings of `isnum()`, `isint()`,
  `isdbref()`, `isobjid()`, `isword()`, `valid()`.** Described in
  both chapters. Content is consistent but redundant.

---

## Volume 2: Technical Accuracy

- [ ] **2-06: STICKY flag description is incorrect.** Same dropto issue
  as 1-05. Book says STICKY sends object to dropto; source shows it
  sends object HOME.

- [ ] **2-10: `first()` example with 3 arguments is incorrect.**
  `first(apple, banana, cherry)` -- `first()` accepts at most 2
  arguments (list, delimiter). Three comma-separated arguments would
  trigger a range check error.

- [ ] **2-12: `#@` position counter described as starting at 0;
  starts at 1.** Same issue as 1-19.

- [ ] **2-12: `if()` function is PennMUSH-centric.** TinyMUSH and
  RhostMUSH only have `ifelse()`. The chapter should present
  `ifelse()` as the more universal function.

- [ ] **2-12: `@if`/`@ifelse` command does not exist on TinyMUSH or
  RhostMUSH.** PennMUSH has `@ifelse` but not `@if` specifically.

- [ ] **2-13: `repeat()` example output has wrong character count.**
  `repeat(=-, 20)` should produce 40 characters (20 repetitions of
  "=-"), not the 44 shown.

- [ ] **2-14: Sort type `i` described as "integer" but means
  "case-insensitive."** TinyMUSH `funlist.c:168`: `'i'` maps to
  `NOCASE_LIST`. PennMUSH same. Correct type for numeric sort is `n`.

- [ ] **2-07: CONFORMAT and EXITFORMAT presented as universal but are
  PennMUSH-specific.**

- [ ] **2-15: $-command search order lists master room as "#0".**
  PennMUSH master room is configurable, not necessarily #0.

- [ ] **2-16: ACONNECT example uses `mail(me)` which is a loadable
  module in TinyMUSH, not core.**

---

## Volume 2: Coverage Gaps

- [ ] **No coverage of zones.** Zones are mentioned briefly in Ch 15-16
  references but never formally introduced or explained. Users
  encountering zone references have no context.

- [ ] **No coverage of @power command.** Ch 23 uses `@power Morgan =
  announce` but powers are never explained as a concept.

- [ ] **No coverage of @force command.** Mentioned in security warnings
  (Ch 23) but never formally documented.
