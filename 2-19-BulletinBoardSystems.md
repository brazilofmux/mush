# Bulletin Board Systems

## What Are Bulletin Boards?

Bulletin boards (often called BBS or bboards) are persistent message
boards where players post announcements, discussions, and information
for the community. Unlike channels (which are real-time) and mail (which
is private), bulletin boards are public archives that anyone can read at
their leisure.

Most MUSHes use a softcoded bulletin board system -- a set of commands
built in MUSHcode rather than compiled into the server. The two most
common systems are Myrddin's BBS and Anomaly Jobs, though many games
write their own.

## Reading Boards

List the available boards:

```
> +bblist
--- Bulletin Boards ---
 1  Announcements     3 posts   (Staff)
 2  General           8 posts
 3  RP Coordination   5 posts
 4  Help Wanted       2 posts
```

Read a board's table of contents:

```
> +bbread 2
--- General (8 posts) ---
 1  Morgan     03/05  Looking for RP partners
 2  River      03/06  Map of the city
 3  Ash        03/07  New player guide
 ...
```

Read a specific post:

```
> +bbread 2/3
--- General: Post 3 ---
Author: Ash
Date: 03/07/2026
Subject: New player guide

I put together a quick guide for new arrivals. Check out the
library room (type 'library' from the town square) for a copy.
Questions welcome!
```

## Posting to Boards

Write a new post:

```
> +bbpost 2/My First Post = Hello everyone! I just arrived and
  I'm excited to explore. If anyone wants to show me around,
  page me!
```

The format is `+bbpost <board>/<subject> = <body>`.

Some systems support multi-line posting:

```
> +bbwrite 2/Event Recap
> -
The tournament went great! Here are the results:
First place: Morgan
Second place: River
Third place: Ash
Thanks to everyone who participated.
> .
Post submitted.
```

## Replying to Posts

Most board systems support threaded replies:

```
> +bbreply 2/3 = Great guide, Ash! Maybe add a section about
  channels too?
```

Replies usually appear as follow-up entries under the original post or
as a new post with "Re:" in the subject.

## Editing and Removing Posts

Edit your own posts:

```
> +bbedit 2/1 = Looking for RP partners (updated with times)
```

Remove your own posts:

```
> +bbremove 2/1
Post removed.
```

Staff can usually remove any post for moderation purposes.

## Catching Up on New Posts

When you connect, you may see:

```
BBS: 2 new posts since your last visit.
```

Read only the new posts:

```
> +bbnew
--- New Posts ---
Board 2 (General): Post 8 by River - "Weekend plans"
Board 3 (RP Coordination): Post 6 by Morgan - "Quest signup"
```

Mark all posts as read without reading them:

```
> +bbcatchup
All boards marked as read.
```

Or catch up on a specific board:

```
> +bbcatchup 2
Board 2 marked as read.
```

## Common Board Types

Most MUSHes set up boards for specific purposes:

| Board | Purpose |
|-------|---------|
| Announcements | Staff news and policy changes. |
| General | Open discussion for the community. |
| RP Coordination | Scheduling and planning roleplay scenes. |
| Help Wanted | Requests for assistance or collaborators. |
| Bug Reports | Reporting problems to staff. |
| Suggestions | Ideas for game improvements. |
| Classifieds | In-character trade and services. |

## How BBSes Work (Under the Hood)

Since bulletin boards are softcoded, they are built from the same tools
covered in earlier chapters: \$-commands, attributes, and user-defined
functions. A typical BBS object stores posts as numbered attributes:

```
&POST_2_3 BBS Object = author|date|subject|body
```

The `+bbread` command parses the player's input, retrieves the right
attribute, splits it on the delimiter, and formats the output. If you
have completed the MUSHcode programming chapters, you have all the
skills needed to understand -- or even build -- a BBS system.

## Tips

- **Read the announcements board first.** It often contains rules, theme
  information, and recent changes that affect everyone.
- **Use boards instead of mass mail.** If your message is for the whole
  community, post it on a board rather than mailing everyone.
- **Keep posts focused.** One topic per post makes boards easier to
  browse.
- **Check back for replies.** Boards are asynchronous conversations.
  People may respond days after your post.
- **Respect board purposes.** Do not post off-topic content on
  specialized boards. Use the general board for miscellaneous chat.
