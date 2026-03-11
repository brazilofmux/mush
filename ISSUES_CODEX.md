# Codex Review Notes

This review compares Volume 1 and Volume 2 against the engine sources in `./src`
with emphasis on claims presented as common, mandatory, or implementation-neutral.

## Findings

### 1. The manuscript over-claims cross-engine consensus, but later standardizes behavior that the source trees do not share.

- Manuscript:
  - `1-01-ScopeAndPurpose.md:10-26` says the standard is derived from the common behavior of TinyMUSH 4, TinyMUX 2.13, RhostMUSH, and PennMUSH.
  - `1-01-ScopeAndPurpose.md:43-51` says code written to mandatory features "shall function on any conforming server."
  - `1-01-ScopeAndPurpose.md:101-103` treats channels and mail as specified systems.
- Source evidence:
  - `src/rhostmush/Server/readme/POWER_COMPARE.TXT:13-15` explicitly says "Rhost has no hardcoded comsystem."
  - `src/tinymush/src/modules/comsys/comsys.c:2100-2112` shows TinyMUSH's comsys is a module command table, not a universal core interface shared by all engines.
  - `src/pennmush/hdrs/flags.h:224-250` and `src/rhostmush/Server/src/flags.c:781-820` show materially different power catalogs and names.
- Why this matters:
  - The framing promises a shared mandatory core, but several later chapters read like Penn/Tiny-oriented normalization rather than a codification of actual four-engine agreement.

### 2. `#0` is described as a universal "master room" and default player start, but the source trees separate and/or configure those roles.

- Manuscript:
  - `1-02-ConformanceAndTerminology.md:110-115` defines the master room as object `#0` and says it is the starting location for newly created players.
  - `1-04-ObjectsAndDbrefs.md:154-156` says invalid homes fall back to the master room `#0`.
  - `1-04-ObjectsAndDbrefs.md:214-224` says `#0` serves both as starting location and as the global-command fallback room.
- Source evidence:
  - `src/mux2.13/docs/CONFIGURATION.md:49-55` distinguishes `player_starting_room` from `master_room`.
  - `src/mux2.13/docs/CONFIGURATION.md:91-105` gives separate example values for `master_room` and `player_starting_room`.
  - `src/rhostmush/Server/readme/wizhelp.html:23135-23143` documents `player_starting_room` as a config parameter.
- Why this matters:
  - The book currently hardcodes one deployment pattern as if it were a family-wide invariant. At minimum, this should be downgraded to implementation-defined behavior or recast as "common on some servers."

### 3. Volume 2 tells readers that every player can build, but the engines gate building behind builder access, command permissions, or configuration.

- Manuscript:
  - `2-01-WhatIsAMUSH.md:36-39` says "Every player on a MUSH can create rooms, objects, and exits."
  - `2-01-WhatIsAMUSH.md:88-99` repeats player-building as a defining technical distinction.
- Source evidence:
  - `src/mux2.13/src/command.cpp:734-750` and `src/mux2.13/src/command.cpp:795-800` mark `@create`, `@dig`, `@open`, and `@link` with `CA_GBL_BUILD`.
  - `src/tinymush/src/netmush/nametabs.c:634-645` and `src/tinymush/src/netmush/nametabs.c:687-690` do the same for TinyMUSH.
  - `src/pennmush/src/conf.c:1295` has `options.restrict_building`, and `src/pennmush/hdrs/mushdb.h:15-18` defines `Builder(x)` in terms of access to `@dig`.
- Why this matters:
  - As written, the beginner volume teaches a capability model that is not true on many real games and not true by default policy in the implementations you ship in `./src`.

### 4. The channels chapters present one command family as if it were broadly standard, but the implementations vary enough that these examples are misleading without engine labels.

- Manuscript:
  - `1-30-CommunicationSystem.md:12-14` says the core channel concepts are common to all major implementations.
  - `1-30-CommunicationSystem.md:32-39`, `43-60`, and `105-110` normalize `@channel/*`, `addcom`, and `@clock`.
  - `2-17-Channels.md:18-57` and `104-137` present `@channel/join`, `@channel/leave`, `@channel/emit`, `@channel/add`, `@channel/desc`, `@clock/*`, and `@channel/priv`.
- Source evidence:
  - `src/rhostmush/Server/readme/POWER_COMPARE.TXT:13-15` says Rhost has no hardcoded comsystem.
  - `src/tinymush/src/modules/comsys/comsys.c:2100-2112` exposes a different concrete interface: `@ccreate`, `@cdestroy`, `@cemit`, `@cwho`, `@clist`, `addcom`, etc.
  - `src/mux2.13/src/command.cpp:781-782` exposes `addcom`/`comtitle`, not the exact tutorial syntax shown in Volume 2.
- Why this matters:
  - This is teachable material, but it needs explicit engine scoping. Right now a reader can reasonably infer that `@channel/join` and `@channel/mute` are normal cross-MUSH commands, when the implementations range from hardcoded command families to module-based or softcode-driven comsys designs.

### 5. The "standard powers" catalog is not actually standardized across the included engines.

- Manuscript:
  - `1-08-Powers.md:23-24` requires a power system with "at least two 32-bit words."
  - `1-08-Powers.md:48-104` declares a mandatory Level 2 power catalog, including `CAN_BUILD`, `CREATE_PLAYER`, `CAN_WALL`, `NO_QUOTA`, and `IS_GUEST`.
  - `1-08-Powers.md:158-163` states that a wizard implicitly has all powers.
- Source evidence:
  - `src/pennmush/hdrs/flags.h:224-250` matches many Penn-style names: `CAN_BUILD`, `CREATE_PLAYER`, `CAN_WALL`, `NO_QUOTA`, `LINK_ANYWHERE`, `OPEN_ANYWHERE`.
  - `src/rhostmush/Server/src/flags.c:781-820` uses a different catalog and naming scheme: `FREE_WALL`, `FREE_QUOTA`, `PCREATE`, `TEL_ANYTHING`, `SEARCH_ANY`, etc.
  - `src/rhostmush/Server/readme/POWER_COMPARE.TXT:1-8` explicitly maps non-Rhost names to different Rhost equivalents.
- Why this matters:
  - The chapter is currently much closer to one engine family's vocabulary than to a neutral four-engine standard. It should either become an engine matrix or clearly mark the catalog as a proposed abstraction layer rather than observed consensus.

### 6. Volume 2's mail chapter is missing; `2-18-TheMailSystem.md` is a duplicate of the channels chapter.

- Manuscript:
  - `2-17-Channels.md:1-161` and `2-18-TheMailSystem.md:1-161` are the same channels text.
- Source evidence:
  - `src/tinymush/src/modules/mail/mail.c:1-15` is a real mail subsystem.
  - `src/rhostmush/Server/src/mail.c:1-1` and surrounding mail code confirm Rhost also ships hardcoded mail.
  - `src/mux2.13/docs/CONFIGURATION.md:50` documents `mail_expiration`, confirming mail is part of the shipped implementation set.
- Why this matters:
  - This is not just an editorial blemish. It leaves the reader without the promised user-facing mail chapter while the source trees clearly support mail functionality.

## Opportunities

### 1. Add a per-engine behavior matrix.

For chapters that currently use normative language, add a compact matrix for PennMUSH, TinyMUSH, TinyMUX, and RhostMUSH. The biggest wins are Chapters 4, 8, 30, and the Volume 2 tutorial chapters on channels and mail.

### 2. Separate "common model" from "example command syntax."

The chapters mix abstract semantics with concrete command names. A better structure would be:

- common concept
- Penn/Tiny/MUX examples
- Rhost notes where it diverges

That would preserve the teaching value without overstating interoperability.

### 3. Mark implementation-defined areas earlier and more aggressively.

The manuscript already has the category, but it is underused. The `master_room`, builder access model, and power catalog should be introduced as implementation-defined or optional up front, not after declarative normative prose.

### 4. Add a source-backed appendix for disputed claims.

Given the "standard" framing, a short appendix listing which chapters were checked against which source paths would materially improve trust and make future revisions cheaper.

### 5. Use the survey documents as supporting comparative context, not as primary authority.

The files under `surveys/` reinforce the same pattern seen in the code review:

- Penn and TinyMUSH surveys describe channel/mail support in terms of specific subsystems or modules, not a single universal interface.
- The Rhost survey and reverse-survey documents repeatedly frame Rhost as feature-rich but architecturally divergent, especially around comsys, powers, and subsystem exposure.

That makes the surveys useful as revision-planning context, but they do not reduce the need to mark claims as engine-specific in the book itself.
