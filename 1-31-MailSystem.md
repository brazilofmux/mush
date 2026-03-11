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
| `/nosig` | Does not append the sender's mail signature. |

### Mail Signature

If the sender has a `@mailsignature` attribute set, its evaluated value
is appended to outgoing messages (unless `/nosig` is specified).

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
@malias/destroy <alias>
```

Aliases are referenced with a `+` prefix in recipient lists (e.g.,
`@mail +staff = Message`).

## Mail Quotas

```
@mailquota <player> = <limit>
```

Sets the maximum number of messages a player may have in their mailbox.
When the quota is reached, new incoming messages are rejected. Requires
wizard privileges.

## Mail Permissions

The `@lock/mail` lock on a player controls who may send mail to that player.
If the lock fails, the sender receives an error message and the mail is
not delivered.

The `@mailforwardlist` attribute specifies dbrefs to which incoming mail is
automatically forwarded.

## Mail Functions

### mail()

```
mail(<player>)
mail(<player>, <message-number>)
```

With one argument, returns the number of messages in \<player\>'s mailbox.
With two arguments, returns the text of the specified message. The caller
must be the specified player or a wizard.

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
