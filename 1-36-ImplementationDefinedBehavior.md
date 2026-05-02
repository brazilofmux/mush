# Implementation-Defined Behavior

## Overview

This chapter collects all behaviors that this standard leaves to the
discretion of the implementation. A conforming implementation shall
document its choice for each implementation-defined behavior listed here.

## Object Model

1. **Maximum database size.** The maximum number of objects the database
   can hold.

2. **Dbref recycling policy.** Whether and how dbrefs of destroyed objects
   are reused for newly created objects.

3. **Destruction delay.** Whether `@destroy` takes effect immediately or
   is delayed by one database cycle (with the GOING flag).

4. **Object #0 type.** Whether the master room (#0) is a room or may be
   another type.

5. **Currency name.** The name used for the in-game currency (commonly
   "Pennies").

6. **Object creation cost.** The currency cost to create objects of each
   type.

7. **Master room dbref.** The dbref of the master room, configurable
   independently of `#0` (commonly via `master_room`).

8. **Player starting room dbref.** The dbref new players are placed in
   on creation (commonly via `player_starting_room` or `player_start`).

9. **Default home dbref.** The fallback home location used when an
   object's home is invalid (commonly via `default_home`).

10. **Order of objects in the contents list.** Whether contents are
    ordered by creation, insertion, alphabetically, or otherwise.

11. **`type()` return for destroyed/invalid objects.** The string
    returned for `GARBAGE` or non-existent dbrefs (e.g. `GARBAGE`,
    `#-1 ILLEGAL TYPE`, or `#-1 NOT FOUND`).

## Attributes

12. **Maximum attribute name length.** The maximum number of characters in
    an attribute name.

13. **Maximum attribute value length.** The maximum number of characters in
    an attribute value (commonly 4096 or 8192).

14. **Maximum number of attributes per object.** Whether a limit exists and
    its value.

15. **Attribute name character set.** Which characters are permitted in
    user-defined attribute names.

16. **Standard attribute numbering.** The internal numbers assigned to
    built-in attributes.

17. **Stored password format.** The hash algorithm and storage format
    used for the player password attribute.

## Flags and Powers

18. **Flag characters.** The single-character abbreviations used for each
    flag in the `flags()` function output and `examine` display.

19. **Additional flags.** Any flags beyond the standard set defined in
    Chapter 7.

20. **Additional powers.** Any powers beyond the standard set defined in
    Chapter 8.

21. **Flag and power permission levels.** Which privilege level is required
    to set or clear each flag and power.

22. **Flag storage representation.** The storage layout for flag bits
    (fixed-width bitfields, dynamic flag tables, etc.).

## Expression Evaluation

23. **Maximum expression nesting depth.** The maximum depth of nested
    `[]` evaluations.

24. **Maximum function invocation count.** The maximum number of function
    calls permitted in a single expression evaluation.

25. **Maximum recursion depth for `u()`.** The maximum nesting depth for
    user-defined function calls.

26. **Buffer size.** The maximum length of an evaluated expression result
    (commonly 4096 or 8192 characters).

27. **Register namespace.** The set of valid register names for `setq()`
    and `r()` (commonly 0-9, or 0-35, or named registers).

28. **Space-compression default.** Whether the evaluator collapses
    runs of whitespace by default and which configuration controls it.

29. **`%?` function-metrics format.** Whether `%?` returns a single
    invocation count, a two-value `invocations recursions` pair, or
    is unsupported.

30. **ANSI / color-depth support.** Whether the server supports basic
    ANSI, 256-color, or 24-bit color codes.

## Commands

31. **Queue size limit.** The maximum number of entries in the command queue
    per object.

32. **Queue execution rate.** The number of queue entries executed per
    server cycle.

33. **Semaphore count limit.** The maximum count for semaphore-based
    `@wait`.

34. **`@dolist` iteration limit.** The maximum number of iterations in a
    single `@dolist` command.

35. **`kill` command availability.** Whether the `kill` command is enabled.

36. **Built-in vs `$`-command priority.** Whether built-in commands are
    matched before exits and `$`-commands, and the configurability of
    that order.

37. **`$`-command search order.** The order in which player, inventory,
    location, and remote objects are searched for matching
    `$`-commands.

38. **Attribute search order within an object.** The order in which an
    object's `$`-command attributes are tested when more than one
    matches.

39. **No-match message text.** The exact text shown when an input
    string fails to match any command, exit, or built-in.

40. **`home` and other built-in command position.** Where pseudo-builtins
    such as `home` fall in the matching order.

41. **Multi-exit-match resolution.** When multiple exits match at the
    same priority level, whether the server picks randomly, takes the
    first, or reports ambiguity.

42. **Help command surface.** Which help-style commands the server
    provides (`help`, `+help`, `wizhelp`, `staffhelp`, etc.) and which
    switches each accepts.

43. **Help file layout.** The on-disk format and topic-naming
    conventions used by the help system.

44. **`@search` match algorithm.** Whether `@search` uses prefix,
    substring, or wildcard matching, and the precedence of the
    classes it searches.

45. **WHO visibility for privileged players.** Which combination of
    `DARK`, `HIDDEN`, `CAN_HIDE`, etc. removes a player from WHO
    output for unprivileged viewers.

## Functions

46. **Maximum function arguments.** The maximum number of arguments a
    function may accept.

47. **`encrypt()`/`decrypt()` algorithm.** The encryption algorithm used.

48. **`encrypt()` argument set.** The optional null-transform arg and
    other engine-specific options for `encrypt()`/`decrypt()`.

49. **`digest()` algorithms.** The set of hash algorithms supported.

50. **`crypt()` categories.** The set of password-style hash categories
    accepted by `crypt()`.

51. **Floating-point display precision.** The number of decimal places
    shown in floating-point results.

52. **`rand()` quality.** The random number generator algorithm and
    seeding method.

53. **Side-effect function gating.** The mechanism used to control access
    to side-effect functions (global config, per-object flag, power, or
    per-function config).

54. **`sort()` default collation and accepted type codes.** The default
    sort type plus the engine-specific extensions (e.g. TinyMUX `u`
    Unicode-aware collation).

55. **`comp()` accepted type codes.** The set of comparison type codes
    accepted by `comp()`.

56. **Time-string format.** The format produced by time/date functions
    when no format argument is supplied.

## Locks

57. **Lock nesting limit.** The maximum depth for indirect lock (`@`)
    evaluation.

58. **Evaluation lock limits.** CPU time and recursion limits for
    evaluation locks (`/` syntax).

59. **Lock internal representation.** Whether lock expressions are
    stored as parse trees, bytecode, or another internal form.

## Networking

60. **Default port.** The TCP port on which the server listens.

61. **Maximum connections.** The maximum number of simultaneous network
    connections.

62. **Idle timeout default.** The default idle timeout in seconds.

63. **Idle-sweep frequency.** How often the server scans connections
    for idle disconnect (per-cycle, per-tick, or other cadence).

64. **Login retry limit.** The number of failed login attempts before
    disconnection.

65. **Connection timeout.** The time allowed to complete login after
    connecting.

66. **Post-disconnect socket reuse.** Whether the socket is held open
    for a fresh login after a disconnect.

67. **SSL/TLS support.** Whether and how encrypted connections are
    supported.

68. **SSL/TLS port indicators.** Configuration syntax used to mark a
    port as TLS (e.g. `+ssl` suffix, separate listener directive).

## Database

69. **Storage backend.** The database storage format and backend
    (flat file, GDBM, LMDB, SQLite, etc.).

70. **Dump interval default.** The default automatic dump interval.

71. **Forking dump support.** Whether forking dumps are supported and
    the default setting.

72. **Crash dump format.** The format used for emergency crash dumps.

## Zones, Channels, Mail

73. **Automatic zone assignment.** Whether newly-created objects
    inherit the creator's zone automatically.

74. **`@chzone` flag-stripping behavior.** Which privileged flags and
    powers are stripped when an object's zone changes.

75. **Channel privilege flags and characters.** Which per-user channel
    flags exist and how they display.

76. **Channel formatting customization.** Mechanisms (per-channel
    headers, prefixes, color overrides) for shaping channel output.

77. **Mail switch sets.** The set of switches accepted by the mail
    command(s) and their spellings.

78. **Mail signature attribute name.** The attribute consulted for an
    auto-appended signature (e.g. `MAILSIGNATURE` vs `SIGNATURE`).

79. **Mail delete switch spelling.** The exact switch name used to
    delete mail aliases or messages.

80. **Mail lock name.** The lock that gates `@mail` delivery
    (`@lock/maillock`, `@lock/Mail`, etc.).

81. **Mail storage format.** The on-disk representation used for
    persisted mail.

## Other

82. **Help file format.** The format and location of help text files.

83. **Log file format.** The format and location of server log files.

84. **Configuration file format.** The syntax of the server configuration
    file.

85. **Startup command-line options.** The set of command-line flags
    accepted by the server.

## Documentation Requirement

A conforming implementation shall provide documentation listing its choices
for each implementation-defined behavior. This documentation may take the
form of a configuration guide, a help file topic, or an appendix to the
implementation's manual.

Changes to implementation-defined behaviors between versions should be
documented in release notes.
