# Getting Around

## Moving Through Exits

The most common way to move in a MUSH is to type the name of an exit:

```
> north
Town Square
A bustling square with a fountain at its center. Market stalls
line the edges, and the town hall rises to the east.
Obvious exits:
South  East  West  Town Hall
Players:
Jax  Morgan  Quinn
```

When you move, three things happen:

1. Players in the room you left see a departure message (e.g., "Sparrow
   has left.").
2. You see the description of the new room.
3. Players in the room you entered see an arrival message (e.g., "Sparrow
   has arrived.").

### Exit Aliases

Exits often have short aliases. An exit named `North;north;n` can be
used with any of those names:

```
> north
> n
```

Both do the same thing. Builders typically set up single-letter aliases
for the cardinal directions: `n`, `s`, `e`, `w`, `ne`, `nw`, `se`, `sw`,
`u` (up), and `d` (down).

### The go Command

You can also use `go` explicitly, though this is rarely necessary:

```
> go north
```

## Looking Around

### look

```
look
look <object>
look <player>
```

Typing `look` by itself re-displays the current room. You can also look
at specific objects or players to see their descriptions:

```
> look fountain
A stone fountain carved with figures of dolphins. Clear water
spills from their mouths into a wide basin.
```

```
> look Morgan
A stocky dwarf with a braided beard and soot-stained hands.
A heavy hammer hangs from his belt.
```

### What You See in a Room

A room display includes:

- **The room name** -- typically shown in bold or a highlight color.
- **The description** -- the text set with `@desc` on the room.
- **Obvious exits** -- a list of exits you can use.
- **Contents** -- players and objects visible in the room.

Objects with the DARK flag are hidden from the contents list. Exits with
the DARK flag are hidden from the exits list.

## Special Movement

### home

```
home
```

The `home` command teleports you to your home location. Every player has
a home set when they are created. You can change your home with:

```
> @link me = <room>
```

### enter and leave

Some objects can be entered. If an object has the ENTER_OK flag, you can
step inside it:

```
> enter carriage
The Carriage
A velvet-lined interior with facing seats and small windows.
```

To get back out:

```
> leave
Town Square
...
```

Builders use enterable objects to create vehicles, containers, and nested
spaces.

### @teleport

If you have permission, you can teleport directly to a room:

```
> @teleport #100
```

Teleportation is usually restricted. Some rooms have the JUMP_OK flag,
which allows anyone to teleport there. Otherwise, you need special powers
or wizard privileges.

## Inventory

### inventory

```
inventory
```

Shows what you are carrying:

```
You are carrying:
  Magic Sword
  A worn map
  Iron Key
You have 100 Pennies.
```

### get and drop

To pick up an object from the room:

```
> get Magic Sword
Picked up.
```

To put it down:

```
> drop Magic Sword
Dropped.
```

Not all objects can be picked up. The object's lock determines whether you
are allowed to take it.

### give

To hand an object to another player in the same room:

```
> give Morgan = Magic Sword
```

You can also give currency:

```
> give Morgan = 50
```

This transfers 50 Pennies (or whatever the game's currency is called) from
your balance to theirs.

## Finding Things

### WHERE and WHO

The `WHO` command shows who is currently connected:

```
> WHO
Player Name     On For   Idle   Doing
Morgan          2h 15m   3m     Building the forge
Jax             45m      0m
Quinn           3h 02m   1h     AFK
3 players connected.
```

The "Doing" column shows each player's self-set status message. You can set
yours with:

```
> @doing Exploring the forest
```

### @find

To find objects you own:

```
> @find sword
Magic Sword(#203)
Rusty Sword(#417)
```

This lists all objects you own whose names contain "sword."

### @search

For more powerful searches:

```
> @search type=room
> @search flags=D
```

The `@search` command is covered in detail in later chapters.

## The Score Command

```
> score
You have 100 Pennies.
```

Shows your current currency balance. Currency is used to create objects and
may be used by game-specific systems.

## Movement Messages

When you move through an exit, the server can display customized messages.
For example, a builder might set:

- **SUCC:** You push through the heavy curtain.
- **OSUCC:** Sparrow pushes through the heavy curtain.
- **ODROP:** Sparrow emerges from behind the curtain.

These messages make movement more immersive. As a player, you simply enjoy
them. As a builder (which you will learn in Part II), you will set them
yourself.

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `north` (or any exit) | Move through an exit. |
| `look` | View the current room. |
| `look <thing>` | View an object or player. |
| `home` | Go to your home location. |
| `enter <object>` | Enter a container/vehicle. |
| `leave` | Exit a container/vehicle. |
| `inventory` | See what you are carrying. |
| `get <object>` | Pick up an object. |
| `drop <object>` | Put down an object. |
| `give <player> = <object>` | Hand an object to someone. |
| `WHO` | See who is connected. |
| `@doing <message>` | Set your WHO status. |
| `score` | Check your currency balance. |
