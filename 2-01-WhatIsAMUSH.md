# What Is a MUSH?

## A World Made of Text

A MUSH is a multi-user, text-based virtual world. Imagine a place where
you type commands to move through rooms, talk to other people, pick up
objects, and build new places -- all described in words rather than graphics.
A MUSH is that place.

The acronym stands for **Multi-User Shared Hallucination**, a playful name
that captures the essence of the experience: many people, connected over
the Internet, sharing an imagined space that exists only because everyone
agrees it does.

When you connect to a MUSH, you see descriptions of rooms and the people
in them. You type commands to speak, move, and act. Other players see your
actions and respond with their own. The result is a collaborative,
real-time, text-based experience that has been captivating people since the
early 1990s.

## What Can You Do on a MUSH?

MUSHes serve many purposes:

**Socializing.** At their simplest, MUSHes are places to hang out and talk.
Many players treat them as text-based chat rooms with a sense of place --
you are not just talking, you are sitting in a virtual coffee shop or
standing on the bridge of a starship.

**Roleplaying.** Many MUSHes are dedicated to collaborative storytelling.
Players create characters and act out scenes together, often in richly
detailed settings based on books, movies, television shows, or original
worlds. The pose command lets you describe your character's actions in
third person, and the result reads like a collaboratively written novel.

**Building.** On most MUSHes, players can create rooms, objects, and exits
(subject to server permissions and quotas). You can build a house, a
dungeon, a space station, or an entire city. The building tools are simple
but flexible, and the results are limited only by your imagination and your
ability to describe them.

**Programming.** MUSHes include a built-in programming language called
MUSHcode (or softcode). With it, you can create interactive objects,
automated systems, games within games, and tools for other players. Many
MUSHes have elaborate coded systems for combat, magic, economies, and
more -- all written in MUSHcode by players.

**Administration.** Running a MUSH is a hobby in itself. Administrators
configure the server, manage players, maintain the database, and shape the
community. It is part system administration, part community management,
and part creative direction.

## A Brief History

The MUSH family of servers traces its lineage back to TinyMUD, created by
Jim Aspnes in 1989. TinyMUD introduced the idea of a multi-user environment
where every player could build and extend the world.

In 1990, Larry Foard created TinyMUSH, which added a programmable expression
evaluator -- the ability to embed code in objects that would run when
triggered. This was the key innovation that separated MUSHes from their
MUD ancestors: instead of relying on compiled C code for game mechanics,
MUSH administrators and players could create interactive systems using
in-game softcode.

From TinyMUSH grew several branches:

- **TinyMUSH** continued to evolve through versions 2.x and 3.x, with
  version 4.0 representing a modern, modular rewrite.
- **TinyMUX** (Multi-User Experience) branched from TinyMUSH 2.0 and
  developed its own identity, emphasizing stability and performance.
- **PennMUSH** branched early and developed independently, becoming the
  most widely deployed MUSH server with a rich feature set.
- **RhostMUSH** branched from TinyMUSH 2.x with a focus on compatibility,
  extensive configuration options, and security features.

Despite their different codebases, all four servers share the same core
concepts: rooms, exits, things, players, attributes, flags, locks, and
the expression evaluator. Code written for one server generally works on
the others with minor adjustments. This book covers the features common to
all of them.

## How Is a MUSH Different from a MUD?

The terms are often confused. MUD (Multi-User Dungeon) is the broader
category that includes all text-based multi-user virtual worlds. A MUSH is
a specific type of MUD, distinguished by:

- **Player building.** On a MUSH, players can typically create rooms,
  objects, and exits (subject to permissions). On many MUDs, only
  administrators can build.
- **Softcode.** MUSHes have a built-in interpreted language that runs inside
  the game. Most MUDs rely on compiled code (C, C++, or similar) for game
  mechanics.
- **Social focus.** MUSHes tend to emphasize social interaction and
  collaborative storytelling. Many MUDs emphasize combat, leveling, and
  loot.

These are tendencies, not hard rules. There are combat-focused MUSHes and
social MUDs. But the technical distinction -- player building and softcode
-- is what defines the MUSH family.

## MUSH Terminology at a Glance

You will encounter these terms throughout this book:

| Term | Meaning |
|------|---------|
| **Room** | A location in the virtual world. |
| **Exit** | A passage connecting two rooms. |
| **Thing** | An object that can be carried or placed in a room. |
| **Player** | A character controlled by a human. |
| **Dbref** | A database reference number (e.g., `#42`). Every object has one. |
| **Attribute** | A named property on an object (e.g., a description). |
| **Flag** | A boolean setting on an object (e.g., DARK, STICKY). |
| **Lock** | A condition that controls who can interact with an object. |
| **Softcode** | Programs written in MUSHcode, the in-game language. |
| **Hardcode** | The server itself, written in C. |
| **Wizard** | An administrator with full control over the game. |
| **Builder** | A player who creates rooms, exits, and objects. |
| **Coder** | A player who writes MUSHcode programs. |

Do not worry about memorizing these now. Each term will be explained fully
when it comes up.

## What You Need

To use a MUSH, you need:

1. **A MUSH client.** This is a program that connects to a MUSH server
   over the Internet. Popular clients include MUSHclient, Potato, BeipMU,
   and mudlet. You can also use a plain telnet client, though a dedicated
   MUSH client is much more comfortable.

2. **A MUSH to connect to.** You need the address (hostname or IP) and
   port number of a running MUSH server. MUSHes are listed on community
   directories, or you can run your own.

3. **Curiosity.** The rest, this book will teach you.

In the next chapter, you will connect to a MUSH for the first time.
