# Describing Your Creations

## The Art of Description

Descriptions are what players see when they look at your rooms, objects,
and characters. Good descriptions bring the virtual world to life. They are
the "graphics" of a MUSH -- your words paint the picture.

## Setting Descriptions

The `@desc` command sets an object's description:

```
> @desc here = A narrow alley between two tall buildings.
  Puddles of rainwater reflect the grey sky. A fire escape
  ladder hangs from the wall to your left.
```

You can describe any object you own:

```
> @desc me = A tall woman with short dark hair and wire-rimmed
  glasses. She carries a battered leather satchel.
> @desc Magic Sword = A slender blade of blue steel. Faint
  runes glow along the fuller.
```

## Message Attributes

Descriptions are just one type of message attribute. MUSH objects support
a rich set of messages that are displayed in different situations.

### Success and Failure Messages

When a player successfully uses an object (passes its lock), the success
messages are shown. When they fail, the failure messages appear:

```
> @succ door = You push the door open and step through.
> @osucc door = pushes the door open and steps through.
> @fail door = The door is locked. You hear a click as the
  handle refuses to turn.
> @ofail door = tries the door, but it is locked.
```

**@succ** is shown to the player who succeeds. **@osucc** is shown to
everyone else in the room (prefixed with the player's name). **@fail** and
**@ofail** work the same way for failures.

### Drop Messages

When a player drops an object:

```
> @drop chest = You set the chest down carefully.
> @odrop chest = carefully sets down a wooden chest.
```

### Enter and Leave Messages

For enterable objects and rooms:

```
> @enter carriage = You climb into the carriage.
> @oenter carriage = climbs into the carriage.
> @leave carriage = You step out of the carriage.
> @oleave carriage = steps out of the carriage.
```

### Action Attributes

Every message type has an **action** variant (prefixed with `A`) that
executes MUSHcode when triggered:

```
> @asucc door = @pemit %# = A cold draft blows through as the
  door opens.
> @afail door = @pemit %# = You hear laughter from the other side.
```

Action attributes are your first taste of programming -- the server runs
the commands in the attribute when the event occurs. We will explore this
fully in Part III.

## The Message Pipeline

When a player interacts with an object (tries to pick it up, pass through
an exit, etc.), the server runs what is called the **did_it pipeline:**

1. Evaluate the object's lock against the player.
2. If the lock **passes:** show SUCC to the player, show OSUCC to others,
   execute ASUCC.
3. If the lock **fails:** show FAIL to the player, show OFAIL to others,
   execute AFAIL.

This pipeline applies to the default lock. Other lock types (enter, leave,
use, etc.) have their own message sets.

## Writing Good Descriptions

### Room Descriptions

A good room description answers: Where am I? What do I see? What can I
interact with?

**Too short:**

```
A room.
```

**Too long:** A full page of text that players will skim past.

**Just right:**

```
A cluttered workshop lit by a single oil lamp. Shelves along the
walls hold jars of colored powders and bundles of dried herbs. A
heavy wooden workbench dominates the center of the room, its
surface scarred with burns and knife marks. A narrow staircase
leads up.
```

This description sets the mood, gives sensory details, and hints at things
the player can examine more closely.

### Object Descriptions

Objects should be described as they would appear when examined closely:

```
> @desc workbench = A massive oak workbench, easily eight feet
  long. The surface is covered in scratches, burns, and stains
  from years of use. A leather tool roll sits at one end, and a
  magnifying glass on a swivel arm is clamped to the edge.
```

### Character Descriptions

Player descriptions should convey appearance, not actions or thoughts:

**Good:** "A heavyset man with calloused hands and a permanent
five-o'clock shadow. He wears a stained canvas apron over work
clothes."

**Avoid:** "He is the strongest person in the room and everyone
respects him." (This tells other players how to react, which is
presumptuous.)

### Tips for Better Descriptions

- **Use sensory details.** Not just what you see, but what you hear, smell,
  and feel. "The air smells of woodsmoke and pine."
- **Mention lighting.** It sets mood instantly. "Candlelight flickers
  against the stone walls."
- **Keep it to 3-5 sentences** for most rooms and objects. Detailed is
  good; exhaustive is not.
- **Write in present tense.** "The fountain bubbles quietly," not "The
  fountain bubbled quietly."
- **Avoid references to the reader.** "You see a fountain" is less
  immersive than "A stone fountain stands at the center of the plaza."

## Dynamic Descriptions

Descriptions can include MUSHcode that changes based on conditions:

```
> @desc here = A garden path.
  [if(gt(rand(2),0),Butterflies flit among the flowers.,
  A gentle breeze stirs the leaves.)]
```

Each time someone looks, they might see a different detail. Dynamic
descriptions are covered fully in Part III.

## The @idesc Attribute

The `@idesc` (interior description) is shown when someone looks at a room
from **inside** an enterable object in that room, or when looking at the
interior of an enterable object:

```
> @idesc carriage = The carriage interior is upholstered in
  red velvet. Small windows on each side show the passing scenery.
```

## Custom Formatting

Advanced builders can use the CONFORMAT and EXITFORMAT attributes on rooms
to customize how contents and exits are displayed:

```
> &EXITFORMAT here = Exits: [iter(lexits(me),name(##),%b,|)]
```

This replaces the default "Obvious exits:" line with a custom format. These
techniques are covered in the programming chapters.

## Quick Reference

| Command | Sets Attribute |
|---------|---------------|
| `@desc` | Description (what you see when you look). |
| `@succ` | Success message (shown to the actor). |
| `@osucc` | Others' success message. |
| `@asucc` | Success action (MUSHcode to execute). |
| `@fail` | Failure message (shown to the actor). |
| `@ofail` | Others' failure message. |
| `@afail` | Failure action (MUSHcode to execute). |
| `@drop` | Drop message. |
| `@odrop` | Others' drop message. |
| `@adrop` | Drop action. |
| `@enter` | Enter message. |
| `@oenter` | Others' enter message. |
| `@leave` | Leave message. |
| `@oleave` | Others' leave message. |
| `@idesc` | Interior description. |
| `@sex` | Gender (for pronoun substitution). |
