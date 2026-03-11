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

## Attributes

7. **Maximum attribute name length.** The maximum number of characters in
   an attribute name.

8. **Maximum attribute value length.** The maximum number of characters in
   an attribute value (commonly 4096 or 8192).

9. **Maximum number of attributes per object.** Whether a limit exists and
   its value.

10. **Attribute name character set.** Which characters are permitted in
    user-defined attribute names.

11. **Standard attribute numbering.** The internal numbers assigned to
    built-in attributes.

## Flags and Powers

12. **Flag characters.** The single-character abbreviations used for each
    flag in the `flags()` function output and `examine` display.

13. **Additional flags.** Any flags beyond the standard set defined in
    Chapter 7.

14. **Additional powers.** Any powers beyond the standard set defined in
    Chapter 8.

15. **Flag and power permission levels.** Which privilege level is required
    to set or clear each flag and power.

## Expression Evaluation

16. **Maximum expression nesting depth.** The maximum depth of nested
    `[]` evaluations.

17. **Maximum function invocation count.** The maximum number of function
    calls permitted in a single expression evaluation.

18. **Maximum recursion depth for `u()`.** The maximum nesting depth for
    user-defined function calls.

19. **Buffer size.** The maximum length of an evaluated expression result
    (commonly 4096 or 8192 characters).

20. **Register namespace.** The set of valid register names for `setq()`
    and `r()` (commonly 0-9, or 0-35, or named registers).

## Commands

21. **Queue size limit.** The maximum number of entries in the command queue
    per object.

22. **Queue execution rate.** The number of queue entries executed per
    server cycle.

23. **Semaphore count limit.** The maximum count for semaphore-based
    `@wait`.

24. **`@dolist` iteration limit.** The maximum number of iterations in a
    single `@dolist` command.

25. **`kill` command availability.** Whether the `kill` command is enabled.

## Functions

26. **Maximum function arguments.** The maximum number of arguments a
    function may accept.

27. **`encrypt()`/`decrypt()` algorithm.** The encryption algorithm used.

28. **`digest()` algorithms.** The set of hash algorithms supported.

29. **Floating-point display precision.** The number of decimal places
    shown in floating-point results.

30. **`rand()` quality.** The random number generator algorithm and
    seeding method.

31. **Side-effect function gating.** The mechanism used to control access
    to side-effect functions (global config, per-object flag, power, or
    per-function config).

## Locks

32. **Lock nesting limit.** The maximum depth for indirect lock (`@`)
    evaluation.

33. **Evaluation lock limits.** CPU time and recursion limits for
    evaluation locks (`/` syntax).

## Networking

34. **Default port.** The TCP port on which the server listens.

35. **Maximum connections.** The maximum number of simultaneous network
    connections.

36. **Idle timeout default.** The default idle timeout in seconds.

37. **Login retry limit.** The number of failed login attempts before
    disconnection.

38. **Connection timeout.** The time allowed to complete login after
    connecting.

39. **SSL/TLS support.** Whether and how encrypted connections are
    supported.

## Database

40. **Storage backend.** The database storage format and backend
    (flat file, GDBM, LMDB, etc.).

41. **Dump interval default.** The default automatic dump interval.

42. **Forking dump support.** Whether forking dumps are supported and
    the default setting.

43. **Crash dump format.** The format used for emergency crash dumps.

## Other

44. **Help file format.** The format and location of help text files.

45. **Log file format.** The format and location of server log files.

46. **Configuration file format.** The syntax of the server configuration
    file.

47. **Startup command-line options.** The set of command-line flags
    accepted by the server.

## Documentation Requirement

A conforming implementation shall provide documentation listing its choices
for each implementation-defined behavior. This documentation may take the
form of a configuration guide, a help file topic, or an appendix to the
implementation's manual.

Changes to implementation-defined behaviors between versions should be
documented in release notes.
