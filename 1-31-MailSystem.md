# The Mail System

## Overview

The mail system provides asynchronous private messaging between players. Mail
persists across sessions: messages remain in the recipient's mailbox until
explicitly deleted. The mail system enables communication that does not
require both parties to be connected simultaneously.

The mail system is Level 2. The core features described here are common
across all major implementations, though details of command syntax and
storage vary.

## Sending Mail

### @mail

```
@mail <player-list> = [<subject>/]<message>
@mail/send <player-list> = [<subject>/]<message>
```

Sends a mail message to one or more players. The \<player-list\> is a
space-separated list of player names or dbrefs. If a subject is included
(separated from the message by `/`), it appears in the message header.

Switches that modify send behavior:

| Switch | Description |
|--------|-------------|
| `/urgent` | Marks the message as urgent. |
| `/silent` | Suppresses the "You have new mail" notification. |
| `/nosig` | PennMUSH-specific: do not append the sender's mail signature on this message. |

The exact switch set is implementation-defined. TinyMUX, for example,
ships `/safe` and `/unsafe` to control purge protection but does not
implement `/nosig`. Portable softcode should probe for switch
availability.

### Mail Signature

If the sender has a mail-signature attribute set, its evaluated value
is appended to outgoing messages. The attribute name is
implementation-defined: PennMUSH uses `MAILSIGNATURE`; TinyMUX uses
`SIGNATURE` (attribute index `A_SIGNATURE`). TinyMUSH and RhostMUSH
use their own names. Portable softcode must select the correct
attribute name for the target engine.

## Reading Mail

### @mail

```
@mail
@mail <message-number>
@mail/read <message-list>
```

Without arguments, `@mail` displays a summary of messages in the current
folder. With a message number, it displays that specific message.

### Message List Syntax

Many mail commands accept a \<message-list\> that specifies which messages
to operate on. Message lists support:

| Format | Description |
|--------|-------------|
| `3` | A single message number. |
| `2-5` | A range of messages. |
| `-7` | Messages 1 through 7. |
| `3-` | Messages 3 through the last. |
| `*player` | Messages from the specified player. |
| `~3` | Messages from 3 days ago. |
| `read` | All read messages. |
| `unread` | All unread messages. |
| `urgent` | All urgent messages. |
| `tagged` | All tagged messages. |
| `cleared` | All messages marked for deletion. |
| `all` | All messages. |

### Message Status

Each message has a status indicated in the message list:

| Code | Status |
|------|--------|
| `N`  | New (unread). |
| `U`  | Urgent. |
| `C`  | Cleared (marked for deletion). |
| `F`  | Forwarded. |
| `+`  | Tagged. |

## Replying and Forwarding

### @mail/reply

```
@mail/reply <message-number> = <message>
```

Sends a reply to the sender of the specified message.

### @mail/forward

```
@mail/fwd <message-list> = <player-list>
```

Forwards the specified messages to one or more players.

### @mail/retract

```
@mail/retract <player> = <message-list>
```

Retracts (deletes) previously sent messages that the recipient has not yet
read.

## Message Management

### Tagging

```
@mail/tag <message-list>
@mail/untag <message-list>
```

Tags or untags messages for later reference. Tagged messages are preserved
across purges.

### Deletion

```
@mail/clear <message-list>
@mail/unclear <message-list>
@mail/purge
```

The `/clear` switch marks messages for deletion. The `/unclear` switch
reverses the marking. The `/purge` switch permanently deletes all cleared
messages. Purging typically occurs automatically when a player disconnects.

### Marking

```
@mail/unread <message-list>
```

Marks read messages as unread (new).

## Folders

Players have multiple mail folders (typically 16, numbered 0-15). Folder 0
is the inbox and the default folder.

```
@mail/folder
@mail/folder <number>
@mail/folder <number> = <name>
@mail/unfolder <number>
@mail/file <message-list> = <folder-number>
```

The `/folder` command without arguments lists all folders. With a number, it
switches to that folder. With a name assignment, it names a folder. The
`/unfolder` command removes a folder name. The `/file` command moves messages
to a different folder.

### Automatic Filing

The `@mailfilter` attribute, when set on a player, is evaluated for each
incoming message. The result determines which folder the message is filed
into.

## Mail Statistics

```
@mail/stats [<player>]
@mail/dstats [<player>]
@mail/fstats [<player>]
```

These commands display mail statistics. The `/stats` switch shows basic
counts. The `/dstats` switch includes read/unread breakdowns. The `/fstats`
switch includes per-folder details. Viewing another player's statistics
requires wizard privileges.

## Mail Aliases

Mail aliases allow sending to named groups of recipients:

```
@malias <alias> = <player-list>
@malias/add <alias> = <player>
@malias/remove <alias> = <player>
@malias/delete <alias>
```

The delete switch spelling is implementation-defined:
PennMUSH accepts `/destroy`; TinyMUX uses `/delete`.

Aliases are referenced with an engine-specific prefix in recipient
lists. TinyMUX uses `*` (`@mail *staff = Message`); PennMUSH
uses `+` (`@mail +staff = Message`). Using the wrong prefix causes
the engine to resolve the name as a literal player, which typically
fails with "no such player." Portable code should avoid embedding the
prefix character in literals and should dispatch on engine.

## Mail Quotas

Per-player mail quotas are an optional, PennMUSH-specific feature.
PennMUSH reads a `MAILQUOTA` attribute set directly on the player
object; when the quota is reached, new incoming messages are rejected.
There is no dedicated `@mailquota` wizard command — quotas are managed
by setting the attribute:

```
&MAILQUOTA <player> = <limit>
```

TinyMUX, TinyMUSH, and RhostMUSH do not implement per-player mail
quotas. A portable softcode quota enforcement would have to be built
on top of the `@lock/mail` mechanism or equivalent.

## Mail Permissions

A lock on the player object controls who may send mail to that player.
The lock's name is implementation-defined: TinyMUX uses
`@lock/maillock` (attribute `A_LMAIL`), PennMUSH uses `@lock/Mail`
(capital M). If the lock fails, the sender receives an error message
and the mail is not delivered.

Automatic forwarding of incoming mail is a PennMUSH-specific feature.
PennMUSH reads the `MAILFORWARDLIST` attribute on the recipient and,
if present and combined with a passing `MailForward` lock, forwards
the incoming message to the listed dbrefs. TinyMUX, TinyMUSH, and
RhostMUSH provide no equivalent auto-forwarding facility in the core
mail subsystem.

## Mail Functions

The softcode function surface for mail diverges substantially between
engines. There is no single agreed-upon mail-function API. The
table below catalogs representative functions across the four
reference engines; a cell showing "—" means that engine does not
provide a directly equivalent function.

| Operation | TinyMUX | PennMUSH | RhostMUSH | TinyMUSH |
|-----------|---------|----------|-----------|----------|
| Read message count / text | `mail(<p>)` / `mail(<p>,<n>)` | `mail([<p>,]<n>)` | `mailread(<n>)` | module-provided |
| Message sender | `mailfrom(<n>)` | `mailstats(<p>)` row | `mailstatus(<n>)` | module |
| Message timestamp | `mailtime(<n>)` | (in `mail()` output) | `mailstatus(<n>)` | module |
| Message subject | `mailsubject(<n>)` | (in `mail()` output) | — | module |
| Message size | `mailsize(<n>)` | — | — | module |
| Message status flags | `mailstatus(<n>)` | — | `mailstatus(<n>)` | module |
| Review recent/all | `mailreview(<p>)` | `maillist(<p>)` | — | module |
| Send from softcode | — | `mailsend()` (side-effect) | `mailsend(<p>,<subj>,<body>)` | module |
| Mailing-list alias | `malias()` | — | `mailalias(<alias>)` | module |
| Quota query | — | `mailstats(<p>)` | `mailquota(<p>)` | module |
| Bulk stats | — | `mailstats(<p>)` | — | module |
| Quick test | — | — | `mailquick(<p>)` | module |

TinyMUSH implements mail as a loadable module; installations that do
not load the mail module have no softcode mail API at all.

The descriptions below cover the TinyMUX forms, which were the
reference used by earlier drafts of this chapter.

### mail()

```
mail(<player>)
mail(<player>, <message-number>)
```

With one argument, returns the number of messages in \<player\>'s
mailbox. With two arguments, returns the text of the specified
message. The caller must be the specified player or a wizard.

### mailfrom()

```
mailfrom(<message-number>)
```

Returns the dbref of the sender of the specified message.

### mailtime()

```
mailtime(<message-number>)
```

Returns the timestamp of when the specified message was sent.

### mailsubject()

```
mailsubject(<message-number>)
```

Returns the subject line of the specified message.

### mailstatus()

```
mailstatus(<message-number>)
```

Returns the status flags of the specified message.

### Portability Note

Portable softcode that consults the mail system must feature-detect
(e.g., by probing the existence of a specific function name) and
branch on the engine, or be restricted to a single target engine.

## Implementation Notes

Mail storage is implementation-defined. Common approaches include:

- Linked list structures saved as part of the database dump.
- Separate database files (GDBM, NDBM, or similar).
- Flat text files loaded at startup.

Mail is stored separately from the object database and may have its own
dump cycle and recovery mechanisms.

Conforming Level 2 implementations that provide a mail system shall support
at minimum: sending mail, reading mail, clearing and purging messages, and
listing mail. Folders, aliases, and quota management are optional features.
