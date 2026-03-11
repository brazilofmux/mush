# Action Lists and Queuing

## Overview

MUSH servers do not execute all commands immediately. Some commands are
**queued** for later execution, either after a time delay or when a
synchronization condition is met. This chapter specifies the action list
format, the command queue, and the mechanisms for delayed and synchronized
execution.

## Action Lists

An **action list** is a string containing one or more commands separated by
semicolons. Action lists are stored in attributes and executed in response
to events.

### Format

```
<command1> ; <command2> ; <command3>
```

Each command in the list is a complete MUSH command (built-in command,
$-command trigger, or expression). Commands are executed in left-to-right
order.

### Evaluation

When an action list is executed, each command in the list is fully evaluated
(percent substitutions expanded, functions called) before execution. The
evaluation context includes:

- **%#** -- The dbref of the enactor (the player or object that triggered the
  action).
- **%!** -- The dbref of the executor (the object on which the action list
  resides).
- **%@** -- The dbref of the caller (the object that directly invoked the
  current function or trigger).
- **%0** through **%9** -- Positional parameters, if the action was triggered
  by a $-command pattern or `@trigger` with arguments.
- **%q0** through **%q9** and **%qa** through **%qz** -- Registers, which
  persist across commands within the same action list.

### Braces in Action Lists

Braces (`{}`) in action lists suppress evaluation of their contents until the
command is actually executed. This is critical for commands like `@switch` and
`@if` that select which branch to evaluate:

```
@switch %0=
  yes, {say I said yes!},
  no, {say I said no!},
  {say I don't understand.}
```

Without braces, all three `say` commands would be evaluated (but not executed)
during parsing, potentially causing unwanted side effects from function calls.

## The Command Queue

All commands that are not executed immediately are placed in the **command
queue**. The queue is a server-wide data structure that holds pending commands
along with their execution context.

### Queue Entries

Each entry in the command queue contains:

| Field         | Description |
|---------------|-------------|
| Executor      | The object that will execute the command (`%!`). |
| Enactor       | The object that caused the command to be queued (`%#`). |
| Caller        | The object that directly triggered the queue entry (`%@`). |
| Command text  | The command string to execute. |
| Arguments     | The values of `%0` through `%9`. |
| Registers     | The values of `%q0` through `%qz` at the time of queuing. |
| Wait time     | The earliest time at which the command may execute (for delayed commands). |
| Semaphore     | The object and attribute used for synchronization (for semaphore waits). |

### Queue Processing

The server processes the command queue in a loop. On each cycle:

1. All entries whose wait time has passed are eligible for execution.
2. Eligible entries are executed in the order they were queued (FIFO).
3. Each entry is fully executed (all commands in its action list) before the
   next entry begins.

The server shall process the queue at least once per second. The exact
frequency is implementation-defined.

### Queue Limits

To prevent denial-of-service from runaway softcode, the server shall enforce
limits on the command queue:

- **Per-object limit:** Each object has a maximum number of queue entries.
  The default limit is implementation-defined but should be at least 100. The
  QUEUEMAX attribute on an object overrides the default. Objects with the
  HUGE_QUEUE power have a substantially higher limit.

- **Global limit:** The server may impose a global maximum on the total number
  of queue entries across all objects.

When an object's queue limit is reached, additional queue entries for that
object shall be discarded with an error message to the object's owner.

## Immediate Execution

Commands typed interactively by a connected player are executed immediately
(synchronously) within the current input processing cycle. They do not pass
through the queue.

The following commands and mechanisms also execute immediately:

- `@force`: The forced command executes immediately in the current context.
- Function calls within expressions: Functions are evaluated inline.
- `@trigger` with the `/now` switch (Level 2): Immediate trigger execution.

## Delayed Execution: @wait

The `@wait` command places a command in the queue for execution after a
specified delay.

### Syntax

```
@wait <seconds> = <command-list>
```

The \<seconds\> argument specifies the minimum number of seconds to wait
before executing the command list. A value of 0 or a negative value causes
the command to be queued for execution on the next queue cycle (effectively
immediately, but asynchronously).

### Evaluation Timing

The command list is **not evaluated at the time @wait is called**. It is
stored as literal text and evaluated when it is executed from the queue. This
means that substitutions like `%#` and `%0` reflect the values at the time
of execution from the queue (which are captured when the entry is created),
not values that might have changed in the interim.

### Examples

```
> @wait 5 = say Five seconds have passed.
```

After 5 seconds, the server executes `say Five seconds have passed.`

```
> @wait 0 = say This runs on the next queue cycle.
```

The command runs asynchronously on the next queue processing cycle.

## Semaphores: Synchronized Execution

Semaphores provide a mechanism for synchronizing command execution. A
semaphore is implemented as an integer counter stored in an attribute
(by default, the SEMAPHORE attribute) on an object.

### @wait with Semaphores

```
@wait <object>[/<attribute>] = <command-list>
```

When a `@wait` command specifies an object (optionally with an attribute
name) instead of a time value, the command is placed on the semaphore queue
for that object/attribute combination. The command will not execute until the
semaphore is notified.

### @wait with Semaphore and Timeout

```
@wait <object>/<timeout> = <command-list>
```

When both an object and a timeout are specified, the command is placed on the
semaphore queue but will also execute if the timeout expires before the
semaphore is notified. This prevents commands from waiting indefinitely.

### @notify

The `@notify` command releases one or more commands waiting on a semaphore:

```
@notify <object>[/<attribute>]
@notify <object>[/<attribute>] = <count>
@notify/all <object>[/<attribute>]
```

- Without a count or `/all` switch, `@notify` releases the oldest waiting
  command on the semaphore and decrements the counter.
- With a count, `@notify` releases that many waiting commands.
- With `/all`, `@notify` releases all waiting commands and resets the counter
  to zero.

### @drain

The `@drain` command discards all commands waiting on a semaphore without
executing them and resets the counter:

```
@drain <object>[/<attribute>]
```

### Semaphore Counter Semantics

The semaphore counter tracks the balance between waits and notifies:

- When a command is added to the semaphore queue via `@wait`, the counter is
  incremented.
- When `@notify` is called and commands are waiting, the oldest command is
  released and the counter is decremented.
- When `@notify` is called and no commands are waiting, the counter is
  decremented below zero. A subsequent `@wait` on the same semaphore will
  execute immediately (consuming the pre-stored notification).

This allows `@notify` to be called before `@wait`, providing a
non-blocking synchronization primitive.

## @trigger

The `@trigger` command executes the contents of an attribute as an action
list:

```
@trigger <object>/<attribute> [= <arg0>, <arg1>, ..., <arg9>]
```

The specified attribute's value is evaluated and executed as a command list.
The optional arguments are passed as `%0` through `%9`.

The triggered action list executes with:

- **%!** set to the object containing the attribute.
- **%#** set to the enactor of the triggering command.
- **%@** set to the object that executed `@trigger`.
- **%0** through **%9** set to the provided arguments.

`@trigger` places the action list in the command queue by default. It does
not execute immediately within the calling command's context.

### @trigger vs. u()

The `@trigger` command and the `u()` function both execute attribute
contents, but they differ in execution model:

| Aspect         | @trigger              | u()                    |
|----------------|-----------------------|------------------------|
| Execution      | Queued (asynchronous) | Inline (synchronous)   |
| Returns value  | No                    | Yes                    |
| Queue entry    | Creates one           | No                     |
| Context        | New queue entry       | Same evaluation context |
| Side effects   | Delayed               | Immediate              |

## @halt

The `@halt` command removes all pending queue entries for an object:

```
@halt <object>
```

This immediately cancels all delayed and semaphore-waiting commands for the
specified object. The object's semaphore counters are reset to zero.

A player can `@halt` objects they own. Wizards can `@halt` any object.
Objects with the HALT_ANYTHING power can `@halt` any object and use
`@allhalt` to clear the entire queue.

### @allhalt

```
@allhalt
```

Clears all entries from the command queue for all objects. This is a wizard-
or HALT_ANYTHING-only command used in emergencies (e.g., runaway softcode
loops).

## Queue Inspection: @ps

The `@ps` command displays the contents of the command queue:

```
@ps
@ps <object>
```

Without an argument, `@ps` shows the player's own queue entries. With an
argument, it shows queue entries for the specified object (subject to
permission checks). The PS_ALL power permits viewing any object's queue.

The display shall include:

- The object that will execute each command.
- The wait time or semaphore reference.
- The command text (possibly truncated).
- The total number of queue entries.

## Execution Limits

To prevent infinite loops and runaway computation, a conforming implementation
shall enforce the following limits:

### Function Invocation Limit

Each command execution has a maximum number of function invocations. When this
limit is reached, further function calls return empty strings. The default
limit is implementation-defined but should be at least 2,500.

### Recursion Depth Limit

Nested function calls (functions calling functions via `u()`, `iter()`, etc.)
have a maximum nesting depth. The default is implementation-defined but shall
be at least 50.

### CPU Time Limit

A conforming implementation should impose a per-command CPU time limit. When
the limit is reached, the command is aborted. This prevents computationally
expensive expressions from blocking the server.

### Queue Size Limit

The total number of entries in the command queue has an upper bound. When the
queue is full, new `@wait` and `@trigger` commands fail.
