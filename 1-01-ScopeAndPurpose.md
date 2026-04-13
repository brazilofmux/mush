# Scope and Purpose

## Scope

This standard specifies the behavior of a conforming MUSH (Multi-User Shared
Hallucination) server. It defines the object model, command language, expression
evaluation engine, built-in functions, flag system, permission model, and
networking behavior that a conforming implementation shall support.

This standard is derived from cross-implementation analysis of four
major MUSH engines:

- TinyMUSH (version 4.0)
- TinyMUX (version 2.14)
- RhostMUSH
- PennMUSH

These engines share a common core -- object model, attribute system,
expression evaluator, percent-code substitution, lock grammar, and
command-matching pipeline -- that has converged through three decades
of cross-pollination. Outside that core, divergence is substantial:
the four engines collectively ship hundreds of softcode functions
unique to a single engine, and entire subsystems (channels, mail,
powers, zones, help) have materially different architectures between
implementations.

Where all four engines agree on behavior, this standard prescribes
that behavior as mandatory. Where engines diverge, this standard
identifies one of three dispositions:

1. **Mandatory behavior** that all conforming implementations shall support.
2. **Optional features** that a conforming implementation may support, but
   shall document whether it does.
3. **Implementation-defined behavior** where this standard specifies the
   interface but permits implementations to choose among defined alternatives.

The standard also catalogs per-engine divergence directly, in the
form of cross-reference notes, compatibility matrices, and parallel
command listings. A softcode author who wants to write portable code
needs to know which form to use on which engine; pretending the
divergence does not exist would serve no one.

This standard does not specify:

- The internal architecture or data structures of a conforming implementation.
- The programming language in which a conforming implementation is written.
- The database storage format used by a conforming implementation.
- The administrative interface for server configuration beyond what is visible
  to connected users.
- Operating system or hardware requirements.
- Performance characteristics or resource limits, except where minimum
  thresholds are specified for conformance.

## Purpose

The purpose of this standard is threefold:

1. **For implementors.** A developer who implements the behaviors described in
   this standard will produce a server that is compatible with the existing
   MUSH ecosystem. Users, softcode, and administrative practices developed on
   one conforming server shall be transferable to another.

2. **For users and programmers.** A user or softcode author who writes to this
   standard can expect predictable behavior across conforming implementations.
   Code that relies only on mandatory features of this standard shall function
   on any conforming server.

3. **For the community.** By establishing a common specification, this standard
   enables independent implementations to interoperate at the application
   level and preserves the accumulated knowledge and practice of the MUSH
   community in a durable, implementation-independent form.

## History

The MUSH server family descends from TinyMUD, written by James Aspnes in 1989.
TinyMUSH, originally written by Larry Foard, introduced the programmable
attribute system and expression evaluator that distinguish MUSH servers from
other MUD families. Over three decades, the four major implementations have
evolved both independently and in dialogue with one another, borrowing features
and converging on common behaviors without the benefit of a formal specification.

This standard is the first attempt to codify that shared behavior.

## Document Organization

This standard is organized into nine parts:

- **Part I: Scope, Conformance, and Foundations** (Chapters 1--3) establishes
  the purpose of this standard, defines conformance levels and terminology, and
  describes the notational conventions used throughout.

- **Part II: The Object Model** (Chapters 4--8) defines the database of objects
  that constitutes a MUSH world: object types, database references, attributes,
  flags, and powers.

- **Part III: Command Processing** (Chapters 9--11) specifies how user input is
  parsed, how names are resolved to objects, and how commands are queued for
  execution.

- **Part IV: The Evaluation Engine** (Chapters 12--14) defines the expression
  evaluator, percent-code substitutions, and the function calling convention
  that together constitute the MUSHcode programming language.

- **Part V: Built-in Commands** (Chapters 15--19) specifies the commands that a
  conforming implementation shall provide, organized by function: movement,
  communication, building, object manipulation, and administration.

- **Part VI: Built-in Functions** (Chapters 20--26) specifies the functions
  available within the expression evaluator, organized by category: string,
  math, list, object, boolean, side-effect, and miscellaneous.

- **Part VII: Security and Permissions** (Chapters 27--29) defines the lock
  system, permission model, and zone mechanism that control access to objects
  and commands.

- **Part VIII: Systems** (Chapters 30--33) specifies the channel communication
  system, mail system, network connection handling, and database persistence
  requirements.

- **Part IX: Conformance and Extensions** (Chapters 34--37) defines
  conformance levels, catalogs optional features, specifies
  implementation-defined behavior, and reserves names for future use.

## Normative References

This standard references the following documents:

- **RFC 854** -- Telnet Protocol Specification
- **RFC 855** -- Telnet Option Specifications
- **RFC 2119** -- Key Words for Use in RFCs to Indicate Requirement Levels
- **RFC 5198** -- Unicode Format for Network Interchange
- **Unicode Standard, Version 15.0** -- Character encoding

## Definitions

Terms used with specific meaning in this standard are defined in Chapter 2,
"Conformance and Terminology."
