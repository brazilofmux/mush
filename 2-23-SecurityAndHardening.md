# Security and Hardening

## Overview

A MUSH is a network service that accepts connections from the internet
and lets users run code on your server. Security matters. This chapter
covers the practical steps to protect your game, your players, and your
system.

## Network Security

### Firewall Configuration

Only expose the port your MUSH listens on (default 4201). Block
everything else:

```
# Allow MUSH port
iptables -A INPUT -p tcp --dport 4201 -j ACCEPT

# Allow SSH for administration
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Drop everything else
iptables -A INPUT -j DROP
```

If your server also runs a web interface or API, open only the ports
you actually use.

### Run as an Unprivileged User

Never run the MUSH as root. Create a dedicated user:

```
$ useradd -m -s /bin/bash mush
$ su - mush
$ ./startmush
```

If the MUSH process is compromised, the attacker has only the
privileges of the `mush` user -- not root.

### Connection Limits

Configure limits to prevent denial-of-service:

```
max_players 200
max_logins 5
connect_fail_limit 10
```

`max_logins` limits simultaneous unauthenticated connections.
`connect_fail_limit` disconnects after too many failed login attempts.

## In-Game Security

### Privilege Discipline

The most common security failures come from giving too many people
Wizard or Royalty privileges. Follow the principle of least privilege:

- **God (#1):** One person. Used only for tasks that require it.
- **Wizards:** A small, trusted group. Know the codebase well.
- **Royalty:** Staff who need administrative access but not full control.
- **Powers:** Grant specific capabilities rather than blanket privilege.

```
> @power Morgan = announce
> @power Morgan = boot
```

This gives Morgan the ability to make announcements and boot players
without granting full Wizard access.

### Protecting Sensitive Objects

Set critical objects (the master room, zone masters, global command
objects) to be owned by God or a secure Wizard character:

```
> @chown Global Commands = #1
> @set Global Commands = SAFE
```

The `SAFE` flag prevents accidental `@destroy`.

### The Master Room

Room #0 (the master room) is special: commands on objects in this room
are available to everyone everywhere. Guard it carefully:

- Only Wizards should be able to build in Room #0.
- Review every object placed there. A malicious \$-command in Room #0
  affects every player.
- Audit Room #0 periodically for unexpected objects.

### Locking Down @function

The `@function` command creates global functions available to all code.
Like Room #0, anything added here affects the entire game:

```
> @function/restrict mycustomfunc = WIZARD
```

Only allow trusted staff to create global functions.

## Code Security

### Sanitize Player Input

Every command that accepts player input should sanitize it with
`secure()` or `escape()`:

```
> &CMD_ECHO me = $echo *:@pemit %# = [secure(%0)]
```

Without sanitization, a player can type:

```
> echo [pemit(*,You got hacked)]
```

And execute arbitrary code through your object.

### Avoid @force on Player Input

Never use `@force` with unsanitized input:

```
BAD:  @force %# = %0
GOOD: @switch %0 = go, {@force %# = go}, ...
```

Accepting arbitrary commands through `@force` is a code injection
vulnerability.

### Limit Side-Effect Functions

Side-effect functions like `create()`, `set()`, and `tel()` should
only be used in controlled contexts. If player input can influence
their arguments, sanitize first.

### Review Global Code

Periodically review code in Room #0, zone master objects, and parent
objects. Look for:

- Commands that accept but do not sanitize input.
- Uses of `@force` or `trigger()` that could be exploited.
- Attributes readable by players that should be private.

## Password Security

### Strong Passwords for Staff

All Wizard and Royalty characters should have strong passwords. A
compromised staff password is a compromised game.

### Password Storage

MUSH servers store passwords hashed. The hash algorithm varies by
server. Modern versions use SHA-256 or bcrypt. Older databases may
use weaker hashing -- upgrade if possible.

### @newpassword

If a staff account may be compromised, reset the password immediately:

```
> @newpassword Morgan = newsecurepassword
```

Then notify the player to change it.

## Backup Security

### Protect Database Files

The database flat file contains everything -- including hashed passwords
and private attributes. Restrict file permissions:

```
$ chmod 600 data/netmush.db
$ chmod 700 data/
```

### Secure Backup Storage

Store backups in a location with restricted access. If backups are
transmitted off-site, encrypt them:

```
$ gpg -c data/backups/netmush-20260311.db
```

## Auditing

### Log Review

Check logs regularly for:

- Failed login attempts (potential password guessing).
- Unexpected Wizard commands.
- Players creating large numbers of objects rapidly.
- Connection patterns suggesting automated attacks.

### @stats and @search

Use administrative commands to spot anomalies:

```
> @stats/all
> @search type=THING flag=WIZARD
> @search owner=#42
```

### Periodic Security Review

Schedule a regular review (monthly or quarterly):

1. Audit privilege levels. Remove unneeded Wizard/Royalty flags.
2. Review objects in Room #0.
3. Check global functions.
4. Verify backups are current and restorable.
5. Update the server software if patches are available.

## Tips

- **Keep the server software updated.** Security patches fix real
  vulnerabilities.
- **Fewer Wizards is better.** Each Wizard account is an attack surface.
- **Lock first, unlock later.** Default to restrictive permissions and
  loosen them only when needed.
- **Document your security practices.** New staff need to know the
  standards.
- **Plan for incidents.** Know what you will do if the game is
  compromised: how to shut down, how to investigate, how to restore.
