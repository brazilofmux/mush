# Optional Features

## Overview

This chapter catalogs features that are neither required by Level 1 nor
Level 2 conformance but are widely implemented and useful. An implementation
may support any combination of these features. When an optional feature is
supported, it should conform to the specification given here.

## SQL Integration

Some implementations provide functions for querying external SQL databases
from within MUSHcode. When supported, the interface typically includes:

- A function (e.g., `sql()`) that executes a SQL query and returns results.
- Configuration parameters for database connection (host, port, database
  name, credentials).
- Support for common database engines (MySQL, PostgreSQL, SQLite).

SQL integration is powerful but carries security risks. Implementations
should restrict SQL access to wizards or objects with a specific power.

## JSON Support

Some implementations provide functions for creating, parsing, and
manipulating JSON data structures. When supported, the interface typically
includes:

- `json_query()` for extracting values from JSON strings.
- `json()` for constructing JSON objects and arrays.
- JSON-aware iteration and mapping functions.

JSON support enables integration with external web services and APIs.

## Regular Expression Variants

While basic regular expression support (`regmatch()`, `regedit()`) is
Level 2, some implementations offer extended regex capabilities:

- `regrab()` and `regraball()` for regex-based list extraction.
- `regrep()` and `regrepi()` for regex-based attribute searching.
- `reswitch()` for regex-based switch/case evaluation.
- Named capture groups in regular expressions.

## Vector Operations

Some implementations provide functions for vector arithmetic, useful for
spatial computation in games with coordinate systems:

- `vadd()`, `vsub()` for vector addition and subtraction.
- `vmul()`, `vdot()` for scalar multiplication and dot product.
- `vmag()` for vector magnitude.
- `vunit()` for unit vector computation.

## Stack Operations

TinyMUSH provides a per-object stack data structure (via a loadable
module) with the following softcode interface:

- `push()`, `pop()`, `peek()` for stack manipulation.
- `lstack()` for listing stack contents.
- `empty()` for testing stack emptiness.

TinyMUX, PennMUSH, and RhostMUSH do not implement this API. Softcode
that relies on these functions is not portable across implementations.

## Extended ANSI and Color

Beyond basic 8-color ANSI support, some implementations offer:

- 256-color support using extended ANSI escape sequences.
- 24-bit (true color) RGB support.
- Named color aliases.
- Background color specification.

## Pueblo/HTML Support

Some implementations support Pueblo or HTML-enhanced output for clients
that support rich text display:

- Clickable links.
- Inline images.
- Custom fonts and formatting.

This feature has become less common as web-based MUSH clients have declined.

## Module and Plugin Systems

Some implementations support loadable modules or plugins that extend
server functionality:

- Dynamically loaded shared libraries.
- Module-defined functions and commands.
- Module hooks for connection, command, and evaluation events.

## Reality Levels

RhostMUSH implements a reality level system that controls which objects
can perceive and interact with each other. Objects are assigned transmit
and receive reality levels; only objects with matching levels can
communicate.

## Cluster System

RhostMUSH provides a cluster system for batch operations on groups of
related objects, enabling efficient management of large object sets.

## Account System

Some implementations support account-based authentication where a single
account may own multiple player characters:

- Login via account name rather than character name.
- Character selection after authentication.
- Shared account-level settings across characters.

## IPv6

Some implementations support IPv6 networking in addition to IPv4. When
supported, the server can listen on IPv6 addresses and perform IPv6-based
site access control.

## Implementation Notes

Optional features should be documented in the implementation's help system.
When an optional feature is present, it should be discoverable through
the `@list` command or equivalent.

Implementations are encouraged to provide configuration options to enable
or disable optional features, allowing server administrators to control the
available feature set.
