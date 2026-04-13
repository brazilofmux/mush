# Running a MUSH Server

## Overview

This chapter is for people who want to run their own MUSH -- whether for
a private group of friends or a public game open to the internet. It
covers choosing a server, compiling it, basic configuration, and the
day-to-day tasks of keeping the game running.

## Choosing a Server

Four major MUSH server implementations are available. All are free and
open source:

| Server | Strengths |
|--------|-----------|
| PennMUSH | Most popular. Excellent documentation, active development. |
| TinyMUX | Fast, stable. Strong codebase for large games. |
| RhostMUSH | Feature-rich. Many built-in hardcode extensions. |
| TinyMUSH | The original lineage. Mature and well-understood. |

All four support the core MUSH feature set described in this book. The
differences are in extensions, configuration options, and internal
architecture. For a first game, PennMUSH or TinyMUX are the most
common recommendations.

## Compiling and Installing

Most MUSH servers are written in C and compile on Linux, macOS, and BSD.
The general process:

```
$ tar xzf pennmush-X.Y.Z.tar.gz
$ cd pennmush-X.Y.Z
$ ./configure
$ make
$ make install
```

Some servers use a configuration script before building:

```
$ cd game
$ ./setup.sh
```

Follow the `INSTALL` or `README` file included with your server for
exact instructions. You will need a C compiler (gcc or clang) and
standard development libraries.

## Configuration Files

Every server has a configuration file that controls its behavior. The
default name depends on the engine: TinyMUX ships `netmux.conf`,
PennMUSH ships `mush.cnf` (from the `mushcnf.dst` distribution
template), TinyMUSH uses `netmush.conf`, and RhostMUSH uses
`netrhost.conf`. Key settings include:

```
# Network settings
port 4201
ip_address 0.0.0.0

# Game identity
mud_name MyMUSH
mud_url http://example.com

# Database file
input_database data/netmush.db
output_database data/netmush.db.new

# Limits
max_players 100
idle_timeout 3600
```

Read through the configuration file carefully. Most settings have
sensible defaults, but you should at least set the game name, port, and
any network-specific options.

## Starting and Stopping

Start the server:

```
$ ./Startmush          # TinyMUSH / PennMUSH-style wrapper
$ ./Startmux           # TinyMUX wrapper
```

Or manually, invoking the server binary directly (binary and config
names are engine-specific):

```
$ ./netmush -c mush.cnf &          # PennMUSH
$ ./netmux -c netmux.conf &        # TinyMUX
$ ./netmush -c netmush.conf &      # TinyMUSH
```

The first time you start, the server creates a minimal database with
Room #0 and Player #1 (God). Connect as God with the password set in
your configuration.

Stop the server cleanly from inside the game:

```
> @shutdown
```

Or from the command line, send a signal:

```
$ kill -TERM <pid>
```

Always shut down cleanly when possible. A clean shutdown saves the
database properly.

## The Startup Script

Most servers include a `startmush` script that handles:

- Starting the server process.
- Restarting automatically if the server crashes.
- Rotating log files.
- Writing the process ID (PID) to a file for management.

Customize the startup script for your environment. Consider adding it to
your system's init scripts or a cron job to start on boot.

## Logging

The server writes logs to a file (usually `game/log` or `game/logs/`).
Logs record:

- Player connections and disconnections.
- Commands flagged for logging.
- Errors and warnings.
- Database save operations.
- Wizard actions.

Review logs regularly. They are your primary tool for understanding what
is happening on the game when you are not watching.

## Regular Maintenance Tasks

### Database Saves

The server periodically saves a snapshot of the database to disk. The
default interval varies by server (typically every 30-60 minutes). You
can trigger a manual save:

```
> @dump
```

### Backups

Back up your database regularly. At minimum, copy the database file
after each clean shutdown. A better approach:

```
$ cp data/netmush.db data/backups/netmush-$(date +%Y%m%d).db
```

Automate this with a cron job. Keep at least a week of backups.

### Monitoring

Check on the game periodically:

```
> @stats
```

This shows object counts, memory usage, and queue depth. Watch for:

- Runaway queue entries (use `@ps` to check, `@halt` to stop).
- Database growth that seems abnormal.
- Players reporting lag or connection issues.

## Going Public

When your game is ready for players:

1. **Open your firewall** on the game port (default 4201).
2. **Register a domain name** or use a static IP so players can find you.
3. **List your game** on MUSH directories and community sites.
4. **Write a connect screen** that welcomes new players and explains
   how to create a character.
5. **Set up staff.** Appoint trusted players as Wizards or Royalty to
   help manage the game.

## Tips

- **Start small.** Build the core areas and test with friends before
  opening to the public.
- **Keep the configuration file commented.** Future-you will thank
  present-you for documenting why each setting was changed.
- **Test after every config change.** Restart the server and verify
  the change took effect.
- **Have a recovery plan.** Know how to restore from a backup before
  you need to do it under pressure.
