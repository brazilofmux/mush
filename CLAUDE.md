# MUSH Book Series Project

## Project Overview

A multi-volume book series about MUSH (Multi-User Shared Hallucination) servers.
Target output: EPUB and PDF for Amazon KDP.

### Volume 1: The MUSH Standard
A formal language and server specification, analogous to ANS Forth or ANS C.
Defines the object model, command language, evaluation engine, functions, flags,
permissions, and networking behavior.

### Volume 2: The MUSH User's Manual
A comprehensive user's guide covering connecting, building, MUSHcode programming,
communication systems, and server administration.

## Reference Implementations

- **TinyMUSH 4**: `/tmp/tinymush` — Modern, CMake, modular, LMDB
- **TinyMUX**: `~/tinymux` — Mature, stable, modular
- **RhostMUSH**: `/tmp/rhostmush` — Feature-rich, security-hardened, Lua
- **PennMUSH**: `/tmp/pennmush` — Most comprehensive, SQL, i18n, de facto reference

### Key Reference Files
- `/tmp/tinymush/docs/Code/COMMANDS_AND_REGISTRIES_REFERENCE.md` — Registry structures
- `/tmp/rhostmush/Server/readme/README.PennMUSH` — 76KB compatibility guide
- `/tmp/rhostmush/Server/readme/FLAG_COMPARE.TXT` — Flag comparison matrix
- `/tmp/rhostmush/Server/readme/POWER_COMPARE.TXT` — Power comparison matrix

## Build System

### File Naming Convention
`[VOLUME]-[CHAPTER]-[Title].md` (e.g., `1-04-ObjectsAndDbrefs.md`)
Volume introductions: `[VOLUME]-00-00-Volume[N]Introduction.md`

### Tools
- `book_assembler.py` — Assembles chapters into per-volume manuscripts
- `volume_config.yaml` — Volume/chapter configuration
- `mdfix` — Ragel-based markdown auto-fixer (compile: `make`)
- `linter.py` — AST-based markdown validator (uses markdown-it-py)
- `copy_artifacts.sh` — Copy outputs to Samba share

### Build Pipeline
1. Write/edit chapter .md files
2. Run `mdfix -i -v *.md` to auto-fix formatting
3. Run `python3 book_assembler.py` to assemble volumes
4. Run `cd book_output && ./convert_all_volumes.sh` for EPUB/PDF

### PDF Profile
Using "trade" profile: 6x9" trade paperback, 10pt, 0.75" binding margin.

## Writing Style

### For The MUSH Standard (Volume 1)
- Use formal standards language: "shall", "should", "may", "must not"
- Follow ISO/ANSI conventions for conformance levels
- Mark implementation-defined behavior explicitly
- Include BNF or similar notation for syntax definitions
- Cross-reference between sections

### For The MUSH User's Manual (Volume 2)
- Friendly, tutorial-oriented prose
- Abundant code examples with expected output
- Progressive complexity (basics first, advanced later)
- Practical, task-oriented organization

## Code Blocks
Use ``` for MUSHcode examples. The language is not recognized by most
syntax highlighters, so use plain fenced blocks or `mushcode` as the
language identifier.
