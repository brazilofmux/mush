# Troubleshooting

## My Command Does Not Work

**Symptom:** You type a command and nothing happens, or you get
"Huh? (Type 'help' for help)".

**Causes and fixes:**

- **Typo in the command pattern.** Check the `$` pattern on the object.
  Use `examine` to see the exact attribute value.
- **Object not in scope.** \$-commands only work if the object is in your
  inventory, in the room, or on you. Check with `look` and `inventory`.
- **Command conflict.** Another object matches first. Rename your
  command to something more distinctive (use a `+` prefix).
- **Missing INHERIT flag.** If the command is on a parent object and the
  child needs to use it, make sure the parent has the INHERIT flag
  where required by your server.

## My Code Returns Nothing

**Symptom:** `think [expression]` produces a blank line.

**Causes and fixes:**

- **Function name misspelled.** MUSHcode silently returns empty for
  unknown functions. Check spelling carefully.
- **Missing arguments.** Some functions return empty when given wrong
  argument counts.
- **Attribute does not exist.** `v(NONEXISTENT)` returns empty. Use
  `default()` to catch this: `default(me/ATTR, fallback)`.
- **Permissions.** You may not have permission to read the attribute or
  object. Check with `examine`.

## Numbers Are Not Working

**Symptom:** `add(2, 3)` returns something unexpected, or math
operations produce errors.

**Causes and fixes:**

- **Extra spaces.** `add( 2, 3)` has a space before the 2. Some servers
  are strict about this. Remove spaces inside function arguments.
- **Non-numeric input.** If a variable holds text instead of a number,
  math functions fail. Test with `isnum()`.
- **Integer vs. floating point.** `div(7, 2)` returns `3` (integer
  division). Use `fdiv(7, 2)` for `3.5`.

## Permissions Errors

**Symptom:** "Permission denied" when trying to modify an object.

**Causes and fixes:**

- **You do not own the object.** Check ownership with `examine`. Only
  the owner (or a Wizard) can modify an object.
- **Object is SAFE.** The SAFE flag prevents destruction. Use
  `@set obj = !SAFE` first if you own it.
- **Attribute is locked.** Some attributes have flags that prevent
  modification. Check attribute flags with `examine`.
- **Zone restrictions.** The object may be in a zone you do not control.

## iter() Produces Extra Spaces

**Symptom:** Output from `iter()` has unwanted spaces between elements
or blank entries.

**Causes and fixes:**

- **Empty results.** `iter()` includes empty strings as elements. Use
  a conditional to skip them: `iter(list, ifelse(check, ##,))`.
- **Whitespace in the pattern.** Newlines and spaces in your `iter()`
  pattern become part of the output. Keep the pattern on one line or
  use `trim()` on the result.
- **Output delimiter.** By default, `iter()` joins results with spaces.
  Specify a different output delimiter as the fourth argument.

## @wait Actions Never Fire

**Symptom:** You use `@wait` but the delayed action never executes.

**Causes and fixes:**

- **Halted queue.** Someone ran `@halt` on the object. Queued actions
  were cleared.
- **Object destroyed.** If the object is destroyed before the wait
  expires, the action is lost.
- **Semaphore never notified.** If using `@wait obj`, the semaphore
  must be released with `@notify obj`. Without it, subsequent actions
  queue forever.

## ANSI Colors Not Showing

**Symptom:** `ansi(hr, text)` produces plain text with no color.

**Causes and fixes:**

- **Client does not support ANSI.** Make sure your client has ANSI
  color enabled in its settings.
- **ANSI flag not set.** Some servers require the ANSI flag on your
  character: `@set me = ANSI`.
- **Nested ansi() calls.** Inner `ansi()` may reset the outer color.
  Structure your calls so they do not overlap.

## Mail Not Arriving

**Symptom:** You send mail but the recipient says they never got it.

**Causes and fixes:**

- **Player name misspelled.** Check with `@mail/status <player>`.
- **Mailbox full.** The recipient may have hit their quota. They need
  to delete old messages.
- **Player does not exist.** Verify the player exists and is not a
  thing or room with a similar name.

## Database or Server Issues

### Server Will Not Start

- Check the log file for error messages. Common causes: corrupted
  database, configuration syntax error, port already in use.
- Try loading a backup database.
- Verify file permissions on the database and log directories.

### Lag or Slow Performance

- Check `@ps` for runaway queued commands. Use `@halt` on the
  offending object.
- Check `@stats` for unusual object counts.
- Look for infinite loops in code (recursive `u()` calls without a
  base case).
- Check system resources: CPU, memory, disk space.

### Lost Objects After Crash

- Restore from the most recent backup.
- If the crash happened between dumps, work since the last dump is
  lost. Decrease the `dump_interval` to reduce exposure.

## General Debugging Techniques

1. **Use think.** Test expressions with `think` before putting them on
   objects. This isolates the expression from command matching issues.

2. **Use TRACE.** Set the TRACE flag on an object to see every function
   evaluation: `@set obj = TRACE`. Remove it when done.

3. **Examine everything.** Use `examine` to see the actual attribute
   values, flags, and ownership of objects involved.

4. **Check @ps.** View the command queue to see what is pending.

5. **Simplify.** If a complex expression fails, break it into smaller
   pieces and test each one with `think`.

6. **Read the help.** Most servers have extensive built-in help: `help
   <topic>`.
