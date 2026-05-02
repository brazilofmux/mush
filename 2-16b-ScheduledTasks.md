# Scheduled Tasks

## Overview

Some work in a MUSH is not triggered by a player action. A weather
system tick, a daily economy reset, a periodic cleanup of temporary
attributes, a weekly announcement post — these all need to run on a
wall-clock schedule, not in response to anything a user typed.

MUSH has historically handled this with chained `@wait` loops: a
command queues itself again after its interval. This works, but it is
fragile — a typo or a crash breaks the chain, and reading the
currently-scheduled work is awkward. Modern servers provide a proper
cron facility.

## @cron (TinyMUX)

TinyMUX ships a built-in `@cron` system with standard Unix cron
syntax. Scheduled entries fire independently of the command queue
and do not depend on chained `@wait`s.

### Scheduling an Entry

```
> @cron #500/AWEATHER = 0 * * * *
Cron entry added.
```

The general form is `@cron <object>/<attribute> = <timestring>`. The
timestring is a standard five-field cron spec:

```
<minute> <hour> <day-of-month> <month> <day-of-week>
```

- **Minute:** 0–59
- **Hour:** 0–23 (24-hour clock)
- **Day of month:** 1–31
- **Month:** 1–12, or `jan`–`dec`
- **Day of week:** 0–7 (both 0 and 7 are Sunday), or `sun`–`sat`

Each field accepts:

- `*` — any value
- `N` — a single value (e.g. `30`)
- `N-M` — a range (e.g. `1-5` for Mon–Fri if used in day-of-week)
- `N,M,O` — a list (e.g. `1,15,30`)
- `*/K` — every K units (e.g. `*/15` for every 15 minutes)
- `N-M/K` — stepped range (e.g. `0-30/5`)

### Common Patterns

```
> @cron #500/AWEATHER  = 0 * * * *           (hourly)
> @cron #500/ATICK     = */15 * * * *        (every 15 minutes)
> @cron #500/ADAILY    = 0 6 * * *           (06:00 every day)
> @cron #501/AMONTHLY  = 10 3 1 * *          (03:10 on the 1st)
> @cron #501/AWORKDAY  = 0 9 * * mon-fri     (09:00 weekdays)
> @cron #501/ABIWEEK   = 0 0 1,15 * *        (midnight on the 1st and 15th)
```

### Listing Scheduled Entries

```
> @crontab
Obj       Attr         Schedule         Next fire
#500      AWEATHER     0 * * * *        2026-04-12 15:00:00
#500      ATICK        */15 * * * *     2026-04-12 14:15:00
#501      ADAILY       0 6 * * *        2026-04-13 06:00:00
```

Without arguments, `@crontab` shows entries for objects you own.
With an object argument, it shows entries for that object (you must
control it). Wizards with the `See_All` power can see all entries.

### Removing Entries

```
> @crondel #500/AWEATHER      (remove one attribute's schedule)
> @crondel #500               (remove all schedules on #500)
```

### Permanence Across Restarts

Cron entries are **not** automatically preserved across a server
restart. Put the `@cron` commands in a `STARTUP` attribute on a
stable object so they are re-registered at boot:

```
> &STARTUP #500 =
    @cron me/AWEATHER = 0 * * * *;
    @cron me/ATICK    = */15 * * * *;
    @cron me/ADAILY   = 0 6 * * *
```

The server fires the `STARTUP` attribute on every object that has one
when the game boots (subject to the `run_startup` configuration
option). There is no `@startup` command — the attribute is invoked
automatically. Set it once and the next restart will replay it and
recreate the schedule.

## Alternatives on Other Engines

- **PennMUSH**: ships `@daily` (a once-per-day trigger at a
  configurable hour), no general cron. For finer granularity,
  softcoded `@wait` loops remain the norm.
- **TinyMUSH, RhostMUSH**: no built-in cron. Use chained `@wait` or
  an `@startup` that installs the first `@wait`.

Portable softcode that must run cross-engine typically defines a
wrapper: check for `@cron` availability, use it if present, fall back
to `@wait` chaining otherwise.

## Practical Example: Weather System

A weather tick that updates global state every 15 minutes, announces
major changes, and runs a daily reset at midnight:

```
> &ATICK #500 = @@  every 15 minutes
    &TICKS me=[add(v(TICKS),1)];
    u(FN_ADVANCE_WEATHER)

> &ADAILY #500 = @@  midnight reset
    &DAY me=[add(v(DAY),1)];
    &TICKS me=0;
    @cemit Public=[ansi(hy, Good morning, travelers!)]

> &STARTUP #500 =
    @cron me/ATICK  = */15 * * * *;
    @cron me/ADAILY = 0 0 * * *
```

After the next restart, the weather cron is live, running
unattended. You can examine `@crontab` to confirm the schedule is
registered and see when the next tick will fire.

## Tips

- **Use `@@` comments** in scheduled attributes. When a cron entry
  misbehaves a year from now, you want the attribute to tell you what
  it was supposed to do.
- **Keep the attribute short.** A cron attribute should dispatch to a
  named function (`u(FN_*)`) rather than contain the whole body
  inline. This keeps the scheduled text scannable and makes the real
  logic easier to edit.
- **Log the firing.** While debugging a new cron, append a line to a
  scratch attribute every time it runs (`&TICK_LOG me=...`). Once
  stable, remove the logging.
- **Beware the server's local time.** Cron uses the host's local
  clock. A game that spans time zones may see "daily at 06:00" fire
  at surprising wall-clock times for distant players. Document the
  server's time zone on the MOTD.
- **Do not schedule expensive work every minute.** A heavy database
  scan every `* * * * *` can swamp the server. Start with longer
  intervals and tighten only when you have measured the cost.
