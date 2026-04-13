# The Mail System

## Overview

The built-in mail system lets players send messages to each other even
when the recipient is offline. It works like a simple email system inside
the MUSH: you compose a message, address it to one or more players, and
send it. They read it the next time they connect.

## Reading Mail

When you connect, you may see a message like:

```
MAIL: You have 3 new messages.
```

To read your mail:

```
> @mail
--- Mail Box (3 messages) ---
 1  New   From: Morgan    Subject: Welcome!
 2  New   From: River     Subject: Meeting tonight
 3  Read  From: Morgan    Subject: Re: Question
```

To read a specific message:

```
> @mail 1
From: Morgan
Date: Mon Mar 09 14:22:31 2026
Subject: Welcome!

Hey Sparrow! Welcome to the MUSH. Let me know if you have questions.
```

## Sending Mail

To send a message:

```
> @mail Morgan = Welcome back!/It's good to see you again.
```

The format is `@mail <recipients> = <subject>/<body>`. The slash
separates the subject line from the message body.

For longer messages, TinyMUX supports a multi-line composition mode
(PennMUSH uses a different editor interface; check its `help @mail`):

```
> @mail/send Morgan = Weekend event
> - I wanted to let you know about the event this weekend.
> - It starts Saturday at 8pm.
> - Hope to see you there!
> --
Message sent.
```

Each `-<text>` line appends to the body, and `--` (two dashes on a
line by themselves) finishes and sends the message. A lone `.` does
**not** send the message in TinyMUX — it is just treated as a normal
command.

### Multiple Recipients

Send to several players at once by separating names with spaces:

```
> @mail Morgan River = Reminder/Meeting at 8pm tonight.
```

## Replying and Forwarding

Reply to a message by number:

```
> @mail/reply 1 = Thanks for the welcome!
```

This automatically addresses the reply to the original sender and
prefixes the subject with "Re:".

Forward a message to someone else:

```
> @mail/fwd 2 = Sparrow
```

Both TinyMUX and PennMUSH use the abbreviated switch `/fwd`.
`/forward` is not recognized.

## Managing Your Mailbox

### Deleting Messages

```
> @mail/delete 1
Message 1 deleted.
```

Delete a range:

```
> @mail/delete 1-3
Messages 1-3 deleted.
```

### Clearing Deleted Messages

On some servers, deleted messages are only marked for deletion. To
permanently remove them:

```
> @mail/purge
```

### Folders

Organize messages into folders:

```
> @mail/folder Important
Folder "Important" created.
> @mail/file 2 = Important
Message 2 filed to Important.
> @mail/folder Important
--- Important (1 message) ---
 2  Read  From: River     Subject: Meeting tonight
```

## Mail Aliases

Create shortcuts for groups of recipients you mail frequently:

```
> @malias staff = Morgan River Ash
> @mail *staff = Update/New policy starting Monday.      (TinyMUX)
> @mail +staff = Update/New policy starting Monday.      (PennMUSH)
```

This sends the message to all three players. Note the prefix: when
referencing a mailing-list alias in a recipient list, TinyMUX expects
a leading `*` and PennMUSH expects a leading `+`. Using the wrong
prefix (or omitting it entirely) makes the server look for a player
literally named "staff" and fail with "no such player."

## Practical Example: Coordinating an Event

```
> @mail Morgan River Ash = Saturday Event/
  Hey everyone! I'm hosting an RP event this Saturday at 8pm.
  Meet at the Town Square. Bring your characters ready for
  adventure. Reply if you can make it!
```

Then check responses:

```
> @mail
--- Mail Box (5 messages) ---
 4  New   From: Morgan    Subject: Re: Saturday Event
 5  New   From: River     Subject: Re: Saturday Event
```

## Tips

- **Check your mail regularly.** People send important information
  through mail since it works even when you are offline.
- **Keep your mailbox tidy.** Delete old messages and use folders for
  things you want to keep. Some servers have mailbox quotas.
- **Use descriptive subjects.** "Hi" tells the recipient nothing. "RP
  event Saturday 8pm" tells them everything.
- **Do not spam.** Mass mailing every player on the game is poor
  etiquette. Use channels or bulletin boards for announcements.
