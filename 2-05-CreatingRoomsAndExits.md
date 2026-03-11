# Creating Rooms and Exits

## Your First Room

Building on a MUSH starts with creating rooms and connecting them with
exits. The `@dig` command does both at once:

```
> @dig The Garden = Out;out;o, In;in;i
The Garden created as room #200.
Exit "Out" created as exit #201.
Exit "In" created as exit #202.
Linked exit #201 to The Garden(#200).
Linked exit #202 to Town Square(#5).
```

This single command:

1. Created a new room called "The Garden."
2. Created an exit called "Out" from your current room to The Garden.
3. Created an exit called "In" from The Garden back to your current room.

The semicolons after exit names define **aliases** -- shorter names you
can type instead of the full name. "Out;out;o" means the exit can be
used by typing `Out`, `out`, or `o`.

## Understanding @dig

The full syntax is:

```
@dig [/teleport] <room-name> [= <exit-to>[;<aliases>] [, <exit-back>[;<aliases>]]]
```

You can use `@dig` in simpler ways:

**Create a room with no exits:**

```
> @dig Secret Hideout
Secret Hideout created as room #210.
```

The room exists but is disconnected. You will need to create exits
separately or teleport there.

**Create a room with only a one-way exit:**

```
> @dig The Attic = Up;up;u
```

Creates the room and an exit to it, but no way back. Players who go up
will need another way to return.

**Teleport to the new room immediately:**

```
> @dig/teleport Workshop = Door;door;d
```

The `/teleport` switch moves you to the new room after creating it.

## Creating Exits Separately

If you need to add an exit to an existing room, use `@open`:

```
> @open North;north;n = #200
Exit "North" created as exit #215.
Linked exit #215 to The Garden(#200).
```

The exit is created in your current room and linked to the destination.
You can also create an unlinked exit:

```
> @open Secret Door;secret
```

An unlinked exit leads nowhere until you link it with `@link`:

```
> @link Secret Door = #210
```

## Exit Naming Conventions

Exit names and aliases follow a convention that makes navigation intuitive:

```
North;north;n
South;south;s
East;east;e
West;west;w
Northeast;northeast;ne
Up;up;u
Down;down;d
Out;out;o
```

The first name is the display name (what appears in the exits list). The
aliases are what players type. Always include both the full word and its
abbreviation.

For named exits, use descriptive names:

```
Town Hall;town hall;th
Through the Curtain;curtain
Climb the Ladder;climb;ladder;u
```

## Linking Exits

An exit must be **linked** to a destination to be usable. When you create
an exit with `@open ... = #destination`, it is linked automatically. You can
change an exit's destination:

```
> @link East = #300
```

To remove a link (making the exit unusable):

```
> @unlink East
```

To link an exit to the special destination HOME, which sends the user to
their home location:

```
> @link Exit = home
```

## Room Properties

After creating a room, you will want to set its description (covered in
Chapter 7) and possibly some flags:

**JUMP_OK** -- Allows anyone to `@teleport` to this room:

```
> @set #200 = JUMP_OK
```

**LINK_OK** -- Allows anyone to `@link` exits to this room:

```
> @set #200 = LINK_OK
```

**DARK** -- Hides the contents list when players look at the room:

```
> @set #200 = DARK
```

**FLOATING** -- Suppresses "unlinked room" warnings during database checks:

```
> @set #200 = FLOATING
```

## Working with Dbrefs

Every object you create gets a database reference number, shown when the
object is created (e.g., `#200`). You can use dbrefs to refer to objects
regardless of name conflicts:

```
> @desc #200 = A peaceful garden with a bubbling brook.
> @set #200 = JUMP_OK
```

To find the dbrefs of objects you own:

```
> @find garden
The Garden(#200R)
```

The `R` after the dbref means it is a Room.

## Destroying Rooms and Exits

To remove something you created:

```
> @destroy #201
```

Objects with the SAFE flag must be destroyed with `/override`:

```
> @destroy/override #201
```

Be careful: destroying a room destroys everything inside it that you own.
Destroying an exit removes it from the room.

## A Building Walkthrough

Let's build a small area: a cottage with two rooms.

```
> @dig Cottage - Living Room = Cottage;cottage;c, Out;out;o
Cottage - Living Room created as room #250.
> @dig/teleport Cottage - Kitchen = Kitchen;kitchen;k
Cottage - Kitchen created as room #251.
> @open Living Room;living;l = #250
> @desc here = A cozy kitchen with copper pots hanging from a
  rack above the stove. The smell of bread fills the air.
> @desc #250 = A warm living room with a fireplace and
  overstuffed chairs. A braided rug covers the wooden floor.
```

Now you have a cottage with two rooms connected to each other and to the
main area. Players can enter from outside, move between the kitchen and
living room, and leave.

## Tips for Builders

- **Plan before you dig.** Sketch your area on paper first. It is easier
  to connect rooms correctly when you know the layout.
- **Be consistent with exits.** If North goes from A to B, then South
  should go from B to A.
- **Use the FLOATING flag** on rooms that are intentionally disconnected
  from the main grid.
- **Examine your work.** Use `examine` to check that exits are linked
  correctly and descriptions are set.
- **Set the SAFE flag** on objects you do not want accidentally destroyed:
  `@set here = SAFE`.
