# Player Management

## Overview

Running a MUSH means managing a community. This chapter covers the
administrative commands and practices for creating, monitoring, and
disciplining player accounts.

## Creating Players

Players can create their own characters from the login screen using
`create <name> <password>`. As an administrator, you can also create
characters directly:

```
> @pcreate Morgan = temporarypassword
Player Morgan created as #42.
```

This is useful for reserving names, creating staff characters, or
setting up accounts for people who cannot connect to the login screen.

### Registration

Many games require new players to register before they can play. Enable
registration in the configuration:

```
register_create on
```

When enabled, new players must email or otherwise contact staff to get
an account. This reduces abuse but adds overhead.

## Player Privileges

MUSH servers have a hierarchy of privilege levels:

| Level | Description |
|-------|-------------|
| Player | Standard user. Can build and code within quotas. |
| Builder | Extended building privileges. May have higher quotas. |
| Staff | Trusted helpers. Varies by game. |
| Royalty | Full administrative access except for a few God-only commands. |
| Wizard | Nearly unlimited access. Can modify any object. |
| God | Player #1. Unrestricted. Cannot be modified by others. |

Grant privileges with the `@set` or `@power` commands:

```
> @set Morgan = ROYALTY
> @power Morgan = announce
```

**Be conservative with privileges.** Every Wizard-level character is a
potential security risk. Most staff functions can be handled with
Royalty or targeted powers.

## Monitoring Players

### Who Is Online

```
> WHO
Player     Idle  Doing
Morgan     0s    Building the market
River      5m    AFK
Sparrow    0s
```

The administrative version shows more detail:

```
> @doing/header
> SESSION
```

`SESSION` (or `@doing/header` depending on the server) shows IP
addresses, connection times, and other diagnostic information.

### Watching for Problems

Set up listen patterns or automated logging for:

- Abusive language on public channels.
- Rapid-fire commands that might indicate a bot or script.
- Players attempting to access objects they do not own.

```
> @log player = connects
```

## Discipline

### Warnings and Communication

Most issues are best handled by talking to the player first. Page them
or send mail explaining the concern. Keep records of conversations.

### @boot: Disconnecting a Player

```
> @boot Morgan
Morgan has been booted.
```

This disconnects the player immediately. Use it for disruptive behavior
that needs an immediate response.

### @newpassword: Resetting Passwords

```
> @newpassword Morgan = temporarypassword
```

Useful when a player forgets their password or when you need to secure
a compromised account. Tell the player to change it after logging in
with `@password`.

### @toad: Disabling an Account

The nuclear option. `@toad` converts a player into a thing, effectively
destroying the character:

```
> @toad Morgan
Morgan has been turned into a slimy toad!
```

This is irreversible. The player's objects are either destroyed or
chowned to a designated recipient. Use only for the most severe cases
(harassment, cheating, persistent abuse after warnings).

### Softer Alternatives

Before reaching for `@toad`, consider:

- **Site locks.** Block the player's IP from connecting.
- **Channel bans.** Remove the player from communication channels.
- **Quota reduction.** Set their building quota to zero.
- **Flag removal.** Remove the BUILDER or APPROVED flag.

```
> @set Morgan = !APPROVED
> @quota Morgan = 0
```

## Quotas

Quotas limit how many objects a player can create:

```
> @quota Morgan
Morgan has 5 objects (quota: 50).
> @quota/set Morgan = 100
Morgan's quota set to 100.
```

Set reasonable quotas. New players might start with 10-20. Builders and
staff typically need more. Infinite quotas (`@quota/set Morgan = 999`)
are fine for trusted builders.

## Site Management

### Site Locks

Block connections from specific IP addresses or ranges:

```
> @sitelock 192.168.1.0/24
```

Use this against persistent abusers who create new characters after
being disciplined.

### Registration by Site

Some servers let you require registration from specific sites while
allowing open creation from others:

```
> @sitelock/register 10.0.0.0/8
```

This forces anyone connecting from the 10.x.x.x range to register
but lets everyone else create normally.

## Tips

- **Document your policies.** Write clear rules and post them where
  players can find them (connect screen, bulletin board, help files).
- **Be consistent.** Apply the same standards to everyone. Favoritism
  erodes trust.
- **Keep records.** Log disciplinary actions and the reasons for them.
  Memory fades and staff changes happen.
- **Delegate.** Appoint trusted staff so the burden does not fall on
  one person. Define clear roles for each staff member.
- **Assume good faith first.** Most problems are misunderstandings, not
  malice.
