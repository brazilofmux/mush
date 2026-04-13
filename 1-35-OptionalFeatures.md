# Optional Features

## Overview

This chapter catalogs features that are neither required by Level 1 nor
Level 2 conformance but are widely implemented and useful. An implementation
may support any combination of these features. When an optional feature is
supported, it should conform to the specification given here.

## Unicode Support

Implementations vary in their support for Unicode text. A conforming
implementation that advertises Unicode support shall:

- Accept UTF-8-encoded input on player connections and from softcode
  string literals.
- Emit UTF-8-encoded output to clients that negotiate UTF-8 (via
  telnet CHARSET, MCCP, or IAC handshake).
- Preserve Unicode code points through string-manipulation functions
  without corrupting them.
- Count characters (not bytes) in positional functions (`strlen()`,
  `mid()`, `left()`, `right()`), where a character is one Unicode
  code point or grapheme cluster (implementation-defined).
- Compare strings using Unicode-aware collation (see `comp()`,
  `sort()` type codes in Chapters 20 and 22).

TinyMUX 2.14 implements this set. Other engines may be partial; ASCII
is a valid subset and implementations lacking full Unicode support
should document the subset they do support.

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

## WebSockets

TinyMUX 2.14 accepts WebSocket connections on the same port as
telnet, enabling browser-based clients to connect without proxying
software. At the softcode level, a WebSocket client is
indistinguishable from a telnet client (`%#`, `@pemit`, commands all
work identically); the difference is in the I/O channel, which
supports binary frames and structured out-of-band messages.

## GMCP (Generic Mud Communication Protocol)

GMCP is a telnet subnegotiation for out-of-band structured messages
between server and client. An implementation that supports GMCP
provides:

- A softcode function (e.g., `gmcp()`) that sends a named,
  JSON-formatted message to a specific connection.
- An incoming-message hook that fires an attribute when a
  GMCP-speaking client sends a message to the server.
- Package-name conventions (typically `Category.Subtype`, e.g.,
  `Char.Vitals`, `Room.Info`, `Comm.Channel.Text`).

TinyMUX 2.14 implements GMCP. PennMUSH has partial support via its
HTTP/websocket bridge. TinyMUSH and RhostMUSH do not.

## Scheduled Tasks

Implementations may provide a cron-style scheduling facility for
softcode execution at wall-clock times independent of the command
queue. TinyMUX 2.14's `@cron` / `@crontab` / `@crondel` is the
reference; PennMUSH ships a simpler `@daily`. Chained `@wait` loops
remain the portable fallback where neither is available.

## Extended String Functions

Some implementations provide C-style formatted output and local-scope
register helpers:

- `printf()` — format a string using C-style format specifiers.
- `letq()` — bind q-registers in a local scope (like `let` in
  Lisp-family languages), preventing register pollution.
- `mailsend()` — side-effect function to send mail from softcode
  without interactively composing it.

These are present in TinyMUX 2.14; other engines provide their own
subsets.

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

TinyMUX implements a reality level system that controls which
objects can perceive and interact with each other. Objects are
assigned transmit and receive reality levels (`txlevel` and
`rxlevel`); only objects whose reality levels match can see or
communicate with each other. The associated softcode surface
includes:

- `hasrxlevel(<object>, <level>)` — test receive-level membership.
- `hastxlevel(<object>, <level>)` — test transmit-level membership.
- `rxlevel(<object>)` / `txlevel(<object>)` — inspect the levels
  set on an object.
- `listrlevels()` — enumerate defined reality levels.

RhostMUSH supports a partial equivalent; PennMUSH and TinyMUSH do not
implement reality levels in the base server. Softcode that uses
these functions is TinyMUX-specific unless feature-detected.

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
