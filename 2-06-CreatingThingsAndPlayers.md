# Creating Things and Players

## Creating Things

Things are the objects of the MUSH world: swords, keys, signs, furniture,
machines, pets, and anything else that is not a room, exit, or player. The
`@create` command makes a new thing in your inventory:

```
> @create Magic Sword
Magic Sword created as object #300.
```

The new object appears in your inventory immediately. You can give it a
description, set attributes on it, and carry it around.

### Setting a Recycling Value

You can specify a cost when creating an object:

```
> @create Treasure Chest = 50
```

The cost is deducted from your currency balance and becomes the object's
recycling value -- the amount you get back when you destroy it. If you do
not specify a cost, a default value is used.

## Working with Things

### Examining Your Object

```
> examine Magic Sword
Magic Sword(#300T)
Type: THING  Flags:
Owner: Sparrow(#42)  Zone: *NOTHING*
Home: Sparrow(#42)
Location: Sparrow(#42)
```

The `T` after the dbref tells you it is a Thing. The output shows the
owner, home, and current location.

### Setting a Home

Every thing has a home location. If the object is dropped in a room with a
dropto, or if the room resets, the object returns home. Set it with:

```
> @link Magic Sword = #250
```

Now the sword's home is room #250.

### Dropping and Picking Up

```
> drop Magic Sword
Dropped.
> get Magic Sword
Picked up.
```

When you drop a thing, it moves to your current room. When you pick it up,
it moves to your inventory.

## Object Flags

Flags modify how objects behave. Some common flags for things:

**STICKY** -- When dropped in a room with a dropto, the object goes to the
dropto instead of staying in the room. Also useful for making objects return
home:

```
> @set Magic Sword = STICKY
```

**DARK** -- Hides the object from room contents lists. Players can still
interact with it if they know its name:

```
> @set Magic Sword = DARK
```

**ENTER_OK** -- Allows players to enter the object (for vehicles and
containers):

```
> @set Carriage = ENTER_OK
```

**VISUAL** -- Allows anyone to examine the object's attributes:

```
> @set Sign = VISUAL
```

**SAFE** -- Protects the object from accidental destruction:

```
> @set Magic Sword = SAFE
```

## Cloning Objects

If you want a copy of an existing object, use `@clone`:

```
> @clone Magic Sword
Clone of Magic Sword created as object #301.
```

The clone gets copies of all the original's attributes. You can rename it
afterward:

```
> @name #301 = Enchanted Blade
```

## Creating Player Characters

Normal players cannot create other player characters. This is a wizard-only
operation:

```
> @pcreate NewPlayer = password123
```

This creates a new player who can log in with `connect NewPlayer password123`.

### Guest Characters

Many MUSHes provide guest characters that visitors can use without creating
an account. Guest configuration is handled at the server level, not through
in-game commands.

## Naming Rules

Object names must follow the server's naming rules:

- **Things** can have almost any name. Leading and trailing spaces are
  stripped, and some special characters may be forbidden.
- **Exits** use semicolons to separate the primary name from aliases:
  `North;north;n`.
- **Players** must have unique names. The name cannot start with a number
  or contain certain special characters. The exact rules vary by server.
- **Rooms** follow the same rules as things.

To rename an object:

```
> @name Magic Sword = Flamebrand
```

To rename yourself (requires your password):

```
> @name me = NewName mypassword
```

## Object Ownership and Quotas

Every object you create is owned by you and counts against your **quota** --
the number of objects you are allowed to have. Check your quota with:

```
> @quota
Objects: 15  Quota: 50  Remaining: 35
```

If you are out of quota, you cannot create new objects. Destroying objects
frees up quota. Wizards can adjust quotas with `@quota/set`.

## Transferring Ownership

Normally, only wizards can change object ownership. The `@chown` command
transfers an object to another player:

```
> @chown Magic Sword = Morgan
```

The CHOWN_OK flag allows the object's owner to give it away without wizard
help. Set it before the transfer:

```
> @set Magic Sword = CHOWN_OK
```

Then the recipient can `@chown` it to themselves.

## The Object Lifecycle

Objects go through a simple lifecycle:

1. **Creation** -- `@create`, `@dig`, `@open`, or `@clone`.
2. **Configuration** -- Set descriptions, attributes, flags, and locks.
3. **Use** -- Players interact with the object.
4. **Destruction** -- `@destroy` removes the object.

Some servers use delayed destruction: the object gets a GOING flag and is
actually removed on the next database cleanup. You can cancel destruction
with `@undestroy` during this grace period.

## Tips

- **Name things clearly.** A player looking at a room should understand
  what each object is from its name alone.
- **Set descriptions on everything.** An object without a description looks
  unfinished.
- **Use the SAFE flag** on important objects to prevent accidental deletion.
- **Watch your quota.** Clean up test objects you no longer need.
