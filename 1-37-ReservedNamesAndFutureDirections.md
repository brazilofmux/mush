# Reserved Names and Future Directions

## Overview

This chapter reserves names and identifiers for future use by this standard
and identifies areas where the standard may be extended in future revisions.
Implementations should avoid using reserved names for implementation-specific
features to prevent conflicts with future versions of the standard.

## Reserved Command Names

The following command names are reserved for future standardization:

- `@channel` and all `@channel/*` switches.
- `@mail` and all `@mail/*` switches.
- `@sql` for database integration.
- `@json` for JSON operations.
- `@http` for HTTP client operations.
- `@event` for event-driven programming.
- `@module` for module management.
- `@config` for runtime configuration.
- `@log` for logging operations.

Implementations may use these names for their own features but should be
prepared to adjust if a future version of this standard defines them.

## Reserved Function Names

The following function name prefixes are reserved:

- `json*()` for JSON manipulation functions.
- `sql*()` for SQL query functions.
- `http*()` for HTTP client functions.
- `event*()` for event system functions.
- `mod*()` for module system functions (excluding `mod()` for modulo).

## Reserved Attribute Names

The following attribute name prefixes are reserved for future
standardization:

- `CHANNEL_*` for channel system attributes.
- `MAIL_*` for mail system attributes.
- `EVENT_*` for event system attributes.
- `MODULE_*` for module system attributes.

User-defined attributes should avoid these prefixes.

## Reserved Flag Names

No specific flag names are reserved at this time. Implementations are
encouraged to use descriptive names and to submit proposals for
standardization of widely-used custom flags.

## Future Directions

The following areas are under consideration for future revisions of this
standard:

### Unicode Support

Current MUSH implementations vary in their support for Unicode text.
Future revisions may specify requirements for UTF-8 input and output,
Unicode-aware string functions, and internationalized object names.

### Structured Data Types

MUSHcode currently represents all data as strings. Future revisions may
define structured data types (lists, dictionaries, JSON objects) with
dedicated manipulation functions and type-safe operations.

### Event-Driven Programming

Current MUSHcode programming relies on $-commands, ^-listeners, and
attribute triggers. Future revisions may define a formal event system
with event registration, event propagation, and event handlers.

### Standardized Configuration

Server configuration is currently entirely implementation-defined. Future
revisions may standardize a core set of configuration parameters and their
names, enabling portable server configuration.

### HTTP and Web Integration

As MUSHes increasingly integrate with web applications, future revisions
may standardize HTTP client functions, webhook support, and REST API
interfaces.

### Improved Security Model

Future revisions may address:

- Sandboxed execution environments for untrusted code.
- Capability-based security as an alternative to the flag/power model.
- Rate limiting and resource quotas for expression evaluation.
- Audit logging of privileged operations.

### Test Suite

A future revision should include a standardized test suite that
implementations can use to verify conformance. The test suite would consist
of MUSHcode programs that exercise each requirement and verify correct
behavior.

### Deprecation

Future revisions may deprecate features that are no longer recommended:

- The `kill` command, which is disabled on most modern MUSHes.
- The `GOING` flag and delayed destruction, in favor of immediate
  destruction.
- Single-character flag abbreviations in favor of named flags.

Deprecated features would remain in the standard for backward compatibility
but would be marked as candidates for removal in subsequent revisions.

## Versioning

This is version 1.0 of The MUSH Standard. Future revisions shall be
numbered sequentially (1.1, 2.0, etc.) with the following conventions:

- **Minor revisions** (1.1, 1.2) add optional features, clarify ambiguous
  requirements, and fix errata. They do not remove or modify existing
  requirements.
- **Major revisions** (2.0, 3.0) may add new requirements, remove
  deprecated features, and restructure the standard.

Implementations should specify which version of the standard they conform
to.

## Submission of Proposals

Proposals for additions to this standard may be submitted by implementation
teams, MUSH community members, and other interested parties. Proposals
should include:

1. A description of the feature and its purpose.
2. A specification in the style of this standard.
3. Evidence of implementation in at least one reference implementation.
4. Analysis of compatibility with existing MUSHcode.

The standard will be maintained and revised through community consensus
among the reference implementation teams.
