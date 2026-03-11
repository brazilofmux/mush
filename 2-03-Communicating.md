# Communicating

## Overview

Communication is the heart of a MUSH. The server provides several ways to
talk: speech for everyone in the room, poses for describing actions, pages
for private messages across the game, whispers for quiet conversations,
and emits for narrator-style text. This chapter covers them all.

## Room Speech

### say

```
say <message>
"<message>
```

The `say` command speaks to everyone in your current room. You see:

```
You say, "Hello!"
```

Everyone else in the room sees:

```
Sparrow says, "Hello!"
```

The `"` prefix is a shortcut. Most MUSH players use it exclusively:

```
> "What do you think?
You say, "What do you think?"
```

### pose

```
pose <message>
:<message>
```

The `pose` command displays an action. Everyone in the room, including you,
sees:

```
Sparrow leans against the wall.
```

A space is automatically inserted between your name and the message. Use
the `:` prefix shortcut:

```
> :smiles warmly.
Sparrow smiles warmly.
```

### semipose

```
;<message>
```

The semipose is like a pose but with **no space** between your name and the
message. This is useful for possessives:

```
> ;'s eyes light up.
Sparrow's eyes light up.
```

And for punctuation that should attach to the name:

```
> ;, looking surprised, takes a step back.
Sparrow, looking surprised, takes a step back.
```

### When to Use Say vs. Pose

Use `say` when your character is speaking dialogue. Use `pose` when your
character is performing an action, thinking, or when you want to mix
dialogue with action:

```
> :nods slowly. "I think you're right," she says.
Sparrow nods slowly. "I think you're right," she says.
```

This style -- posing actions with embedded dialogue in quotes -- is the
standard convention on roleplay-focused MUSHes.

## Private Communication

### page

```
page <player> = <message>
```

The `page` command sends a private message to another player, no matter
where they are in the game. You see:

```
You paged Morgan with 'Hey, are you busy?'
```

Morgan sees:

```
Sparrow pages: Hey, are you busy?
```

You can page multiple players at once:

```
> page Morgan Jax = Meeting in 5 minutes.
```

To page the same person again, some servers let you omit the name:

```
> page = Actually, make that 10 minutes.
```

Pages are the standard way to have private out-of-character conversations.

### whisper

```
whisper <player> = <message>
```

A whisper sends a private message to someone in the **same room**. Unlike
pages, other players in the room see that you whispered, but they do not
see the content:

```
Sparrow whispers something to Morgan.
```

Whispers are useful for in-character asides.

## Emits

### @emit

```
@emit <message>
```

The `@emit` command displays a message to your room with **no name prefix**.
The text appears exactly as you type it:

```
> @emit The ground shakes briefly.
The ground shakes briefly.
```

Emits are used for environmental descriptions, narration, and special
effects. Since they do not identify who sent them, some MUSHes restrict
their use or enable the NOSPOOF flag so players can see the source.

### @pemit

```
@pemit <player> = <message>
```

Sends a message to a specific player, similar to `page` but without the
formatting and attribution. Used primarily by code rather than by players
directly.

### @oemit

```
@oemit <object> = <message>
```

Sends a message to everyone in the room **except** the specified object.
This is useful for showing a message to others but not to yourself:

```
> @oemit me = Sparrow appears in a flash of light.
```

Everyone except you sees the message.

### @remit

```
@remit <room> = <message>
```

Sends a message to all players in a specific room. You must control the
room or have appropriate permissions. This is commonly used in code to send
messages to rooms the object is not in.

## Blocking Communication

### HAVEN Flag

If you need quiet time, you can set the HAVEN flag:

```
> @set me = HAVEN
```

This blocks incoming `@pemit` messages (but not pages, on most servers).
Clear it with:

```
> @set me = !HAVEN
```

### Page Locking

You can lock your character against pages from specific players:

```
> @lock/page me = !*ThatPerson
```

Or allow pages only from specific people:

```
> @lock/page me = *Friend1 | *Friend2
```

### AWAY and REJECT Messages

When you are away from the keyboard:

```
> @away me = I'm AFK, back in 30 minutes.
```

Players who page you will see your away message. To reject pages entirely:

```
> @reject me = Sorry, I'm not accepting pages right now.
```

## The think Command

```
think <expression>
```

The `think` command evaluates an expression and shows the result **only to
you**. No one else sees anything. It is the primary debugging tool:

```
> think 2 + 2
4
> think strlen(Hello)
5
```

You will use `think` extensively when learning MUSHcode.

## Nospoof

On some MUSHes, you may see messages prefixed with a source indicator:

```
[Sparrow(#42)] The lights flicker.
```

This happens when you have the NOSPOOF flag set. It shows the dbref and
name of the object that sent each message, preventing other players from
impersonating the server or other characters with emits.

To enable nospoof:

```
> @set me = NOSPOOF
```

## Communication Etiquette

Every MUSH community has its own norms, but some conventions are nearly
universal:

- **OOC markers.** When speaking out of character in a roleplay scene, use
  a marker like `<OOC>` or surround your comment with parentheses or
  double brackets: `(( heading out in 5 ))`.
- **Page for OOC.** On roleplay MUSHes, in-room speech is typically
  in-character. Use pages for out-of-character conversations.
- **Ask before paging strangers.** Some players prefer not to receive
  unsolicited pages. On most MUSHes this is just politeness, not a rule.
- **Consent and boundaries.** Respect other players' limits. If someone
  asks you not to page them, stop.

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `"message` | Say something to the room. |
| `:action` | Pose an action to the room. |
| `;action` | Semipose (no space after name). |
| `page player = msg` | Private message to a player. |
| `whisper player = msg` | Private message in the same room. |
| `@emit message` | Emit raw text to the room. |
| `@pemit player = msg` | Send text to a specific player. |
| `think expression` | Evaluate and show only to yourself. |
