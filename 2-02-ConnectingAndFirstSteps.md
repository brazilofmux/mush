# Connecting and First Steps

## Choosing a Client

Before you can enter a MUSH, you need a program to connect with. A MUSH
client handles the network connection and provides a comfortable interface
for reading and typing.

**Dedicated MUSH clients** offer the best experience:

- **MUSHclient** (Windows) -- A mature, feature-rich client with scripting
  support.
- **BeipMU** (Windows) -- A modern client with a clean interface.
- **Potato** (Windows, Mac, Linux) -- A cross-platform client with good
  ANSI color support.
- **mudlet** (Windows, Mac, Linux) -- A powerful client with Lua scripting,
  popular in the broader MUD community.

**Telnet** works in a pinch. On Linux or Mac, open a terminal and type
`telnet hostname port`. On Windows, you may need to enable the Telnet
feature or use PuTTY in raw mode.

**Web clients** are available on some MUSHes, letting you connect through
your browser with no software installation.

For this book, any client that can make a TCP connection to a hostname and
port will work.

## Connecting

Your MUSH's address consists of a **hostname** (or IP address) and a **port
number**. For example:

```
mush.example.com 4201
```

In your client, create a new connection using this address and port. Once
connected, you will see the MUSH's connection screen -- a welcome message
that typically includes the game's name, a brief description, and
instructions for logging in.

## Logging In

At the connection screen, you have two options:

**Connect to an existing character:**

```
connect <name> <password>
```

**Create a new character:**

```
create <name> <password>
```

For example:

```
> create Sparrow mypassword
```

This creates a new character named Sparrow with the password "mypassword"
and logs you in. Choose a name that fits the MUSH's theme and a password
that is not easily guessed. Some MUSHes require character approval before
you can play; others let you start immediately.

After logging in, you will see the Message of the Day (MOTD) and then the
description of the room where your character is standing.

## Your First Look Around

After login, the server automatically shows you your surroundings. You will
see something like:

```
Arrival Hall
A grand hall with marble floors and tall windows. Sunlight streams
through stained glass, casting colored patterns on the stone walls.
A bulletin board hangs near the entrance.
Obvious exits:
North  East  Out
Players:
Morgan  Jax
```

This display has several parts:

- **Room name:** "Arrival Hall" at the top.
- **Description:** The paragraph describing the room.
- **Exits:** The directions you can move.
- **Contents:** Other players and objects in the room.

You can look at the room again at any time by typing:

```
> look
```

To look at a specific object or player:

```
> look Morgan
> look bulletin board
```

## Basic Commands

Here are the essential commands to get you started:

### Speaking

```
> say Hello, everyone!
You say, "Hello, everyone!"
```

Other players in the room see:

```
Sparrow says, "Hello, everyone!"
```

The shortcut `"` works the same way:

```
> "Hello!
You say, "Hello!"
```

### Posing

```
> pose waves hello.
Sparrow waves hello.
```

Or use the `:` shortcut:

```
> :waves hello.
Sparrow waves hello.
```

Poses describe your character's actions in the third person. They are the
primary tool for roleplaying.

### Moving

Type the name of an exit to move through it:

```
> north
```

You will see the description of the new room. Other players in the old room
see you leave; players in the new room see you arrive.

### Checking Inventory

```
> inventory
You are carrying:
  Magic Sword
  A worn map
You have 100 Pennies.
```

### Getting Help

```
> help
```

This displays the MUSH's built-in help system. Most commands have a
help entry:

```
> help say
> help look
> help @describe
```

The help system is your most valuable reference. Use it often.

### Help on Real Servers

Different MUSH engines ship different sets of help commands.
Learning the ones your server provides is a 30-second investment
that pays off forever:

- **`help`** — always available. The main reference.
- **`wizhelp`** (TinyMUX, TinyMUSH, RhostMUSH) — wizard-only topics,
  useful if you have staff privileges.
- **`plushelp`** (TinyMUX, TinyMUSH) — help for the `+`-prefixed
  softcoded commands local to a particular game. If your MUSH has
  game-specific commands like `+roll`, `+bbs`, or `+where`, this is
  where they are documented.
- **`staffhelp`** (TinyMUX) — staff procedures, separate from
  `wizhelp`.
- **`+help`** (TinyMUSH and many softcode packages) — supplementary
  help added by the game's administrators.
- **`help <topic> /search <keyword>`** (RhostMUSH) — wildcard search
  across all help topics.

PennMUSH takes a different approach: administrators configure which
help commands exist (via `help_command` settings), so a PennMUSH
server might expose `help`, `news`, `events`, and `lore` as four
separate indexes. Type `help help` to see which indexes your server
provides.

**If you are new to a server**, start with `help newbie` or `news
newbie`. Most MUSHes maintain a dedicated introduction for new
arrivals covering local conventions, the IC/OOC distinction, and how
to contact staff.

## Customizing Your Character

### Setting Your Description

Other players will look at you. Give them something to see:

```
> @desc me = A tall figure in a long coat, with sharp eyes and
  an easy smile.
```

Now when someone types `look Sparrow`, they see your description.

### Setting Your Gender

```
> @sex me = female
```

This affects pronoun substitution in automated messages (e.g., "She has
arrived" instead of "They have arrived").

### Changing Your Password

```
> @password oldpassword = newpassword
```

## Understanding the Interface

### The Prompt

Most MUSH clients show a text area where you type commands and a scrolling
area where the server's output appears. There is no graphical prompt from
the server itself -- you just type and press Enter.

### Output Formatting

MUSH output is plain text, sometimes enhanced with ANSI color codes. Most
clients display colors automatically. If you see strange codes like
`[1;31m`, your client may need its ANSI color option enabled.

### Line Length

MUSH output is typically formatted for 78-80 character terminal widths.
If text looks oddly wrapped, adjust your client's window width.

## Common Mistakes

**Forgetting the command prefix.** Commands like `@describe`, `@set`, and
`@dig` start with `@`. If you type `describe me = ...`, the server will
not understand.

**Spaces matter.** `say Hello` and `sayHello` are different.
`@desc me = A cat` and `@desc me=A cat` may also behave differently
depending on the server.

**Case does not matter for commands.** `SAY`, `Say`, and `say` all work.
Object names are also case-insensitive in most contexts.

## What Next?

You can now connect, look around, talk, and move. In the next chapter, you
will learn the full range of communication commands -- how to speak, pose,
whisper, page, and emit.
