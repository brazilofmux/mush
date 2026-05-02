# Attributes and Properties

## What Are Attributes?

Attributes are named values stored on objects. You have already used one:
DESC is the attribute that holds an object's description. But objects can
have dozens or even hundreds of attributes, each holding a piece of data
or a snippet of code.

Think of attributes as the object's "memory." They store everything the
object needs to know: its description, its messages, its code, and any
custom data you assign.

## Setting Attributes

There are two ways to set an attribute value:

### The & Command

```
> &COLOR_FAVORITE me = blue
```

This sets the attribute COLOR_FAVORITE on yourself to the value "blue."
The `&` prefix is the most common way to set user-defined attributes,
and the form most code uses.

### The @set Command (Colon Form)

```
> @set me = COLOR_FAVORITE:blue
```

`@set <object> = <attr>:<value>` does the same thing. Note the
**colon** between the attribute name and the value — that is what
distinguishes value-setting from flag-setting.

> **Watch out:** `@set <obj>/<attr> = <value>` does **not** write
> the attribute's value. The `<obj>/<attr>` form sets an attribute
> *flag* (such as `no_inherit` or `wizard`) whose name is `<value>`,
> and will fail with "You can't set that!" if `<value>` is not a
> recognized flag name. Use `&` or the colon form above to write
> values; reserve `@set <obj>/<attr> = <flag>` for changing
> attribute flags. (See Chapter 11 for more on this gotcha.)

### Clearing Attributes

Set an attribute to nothing to clear it:

```
> &COLOR_FAVORITE me =
```

## Viewing Attributes

### examine

The `examine` command shows all of an object's attributes:

```
> examine me
Sparrow(#42PBc)
Type: PLAYER  Flags: CONNECTED
...
DESC: A tall woman with short dark hair.
COLOR_FAVORITE: blue
```

To see a specific attribute:

```
> examine me/COLOR_FAVORITE
COLOR_FAVORITE [#42]: blue
```

### @decompile

The `@decompile` command shows commands that would recreate an object's
settings:

```
> @decompile me
@desc me = A tall woman with short dark hair.
&COLOR_FAVORITE me = blue
```

This is useful for backing up your objects or copying settings.

## Built-in vs. User-Defined Attributes

**Built-in attributes** are predefined by the server. You have already used
several: DESC, SUCC, FAIL, OSUCC, OFAIL, DROP, ODROP. These have special
meaning -- the server looks at them automatically during specific events.

**User-defined attributes** are anything you create with the `&` command.
The server does not interpret them unless you write code that does. They
are your custom data storage.

Attribute names are case-insensitive: `COLOR_FAVORITE`, `color_favorite`,
and `Color_Favorite` all refer to the same attribute. By convention,
attribute names are written in uppercase.

## Common Built-in Attributes

| Attribute | Purpose |
|-----------|---------|
| DESC | Description shown by `look`. |
| SUCC | Success message for the default lock. |
| OSUCC | Others' success message. |
| ASUCC | Success action list (MUSHcode). |
| FAIL | Failure message for the default lock. |
| OFAIL | Others' failure message. |
| AFAIL | Failure action list (MUSHcode). |
| DROP | Drop message. |
| ODROP | Others' drop message. |
| ADROP | Drop action list. |
| LISTEN | Pattern that triggers ^-listeners. |
| ACONNECT | Actions run when a player connects. |
| ADISCONNECT | Actions run when a player disconnects. |
| AWAY | Displayed to players who page you while away. |
| IDLE | Displayed to players who page you while idle. |
| REJECT | Displayed when your page lock rejects a page. |
| DOING | Your status in the WHO list. |

## Attribute Flags

Attributes themselves can have flags that control their behavior:

**VISUAL** -- Anyone can see this attribute (not just the owner):

```
> @set me/FAVORITE_QUOTE = VISUAL
```

**WIZARD** -- Only wizards can change this attribute.

**LOCKED** -- Only the attribute's owner can change it (useful when the
object has been @chowned).

**NO_COMMAND** -- The attribute is not checked for \$-commands.

**NO_INHERIT** -- The attribute is not inherited by children.

To set an attribute flag:

```
> @set me/MYATTR = VISUAL
```

To clear it:

```
> @set me/MYATTR = !VISUAL
```

## The @wipe Command

To remove all user-defined attributes from an object:

```
> @wipe #300
```

To remove only attributes matching a pattern:

```
> @wipe #300/CMD_*
```

This removes all attributes starting with `CMD_`. Be careful -- there is
no undo.

## The @edit Command

To change part of an attribute without retyping the whole thing:

```
> @edit me/DESC = dark hair, red hair
```

This replaces "dark hair" with "red hair" in your description. Useful for
making small corrections to long attribute values.

## Reading Attributes in Code

You will learn this fully in Part III, but here is a preview. To read an
attribute's value in an expression:

```
> think v(COLOR_FAVORITE)
blue
```

The `v()` function reads an attribute on the current object. To read from
another object:

```
> think get(#42/COLOR_FAVORITE)
blue
```

## Inheritance

When an object has a **parent** (set with `@parent`), it inherits
attributes from the parent. If you read an attribute that does not exist
on the object, the server checks the parent, then the parent's parent,
and so on up the chain.

```
> @create Weapon Template
> @desc Weapon Template = A generic weapon.
> @create Magic Sword
> @parent Magic Sword = Weapon Template
> look Magic Sword
A generic weapon.
```

The Magic Sword does not have its own DESC, so it inherits the template's.
If you set a DESC on the sword, it overrides the parent:

```
> @desc Magic Sword = A blade of shimmering blue steel.
> look Magic Sword
A blade of shimmering blue steel.
```

Inheritance is a powerful tool for code organization. You can define
behavior once on a parent and have many children inherit it. This is
covered in depth in Part III.

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `&ATTR object = value` | Set a user-defined attribute. |
| `&ATTR object =` | Clear an attribute. |
| `examine object` | Show all attributes. |
| `examine object/ATTR` | Show one attribute. |
| `@decompile object` | Show commands to recreate attributes. |
| `@wipe object` | Remove all user-defined attributes. |
| `@wipe object/PATTERN` | Remove matching attributes. |
| `@edit object/ATTR = old, new` | Search and replace in an attribute. |
| `@parent object = parent` | Set inheritance parent. |
