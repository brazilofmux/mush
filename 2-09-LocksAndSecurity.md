# Locks and Security

## What Are Locks?

A lock is a condition attached to an object that determines who can interact
with it. When you try to pick up an item, walk through an exit, or enter
a container, the server checks the relevant lock. If you pass, the action
succeeds. If you fail, you are denied and see a failure message.

Locks are the primary tool for controlling access in a MUSH. With them, you
can create doors that only open for certain players, objects that only
specific characters can pick up, and rooms that restrict who may speak.

## The Default Lock

Every object has a default lock. For exits, it controls who can pass
through. For things, it controls who can pick them up. By default, the lock
is open -- anyone can pass.

### Locking to a Specific Player

```
> @lock door = *Morgan
```

Now only Morgan can pass through the door. The `*` prefix indicates a
player name.

### Locking to an Object

```
> @lock door = Iron Key
```

Now only someone who **is** the Iron Key or **carries** the Iron Key can
pass. Since the Iron Key is a thing, this effectively means anyone carrying
the key.

### Locking to a Dbref

```
> @lock door = #300
```

Using a dbref is more reliable than a name, since names can be duplicated
or changed.

## Lock Operators

You can combine conditions using boolean operators:

### AND (&)

```
> @lock vault = Iron Key & Gold Key
```

You must carry **both** keys.

### OR (|)

```
> @lock door = Iron Key | Skeleton Key
```

**Either** key works.

### NOT (!)

```
> @lock park = !*TroublePlayer
```

Everyone **except** TroublePlayer can enter.

### Combining Operators

```
> @lock vault = (Iron Key | Master Key) & *Morgan
```

Morgan must carry one of the keys. Parentheses control the order of
evaluation, just like in math.

## Lock Types

The default lock is not the only lock an object can have. Different lock
types control different interactions:

### Enter Lock

```
> @lock/enter carriage = +Ticket
```

Controls who can `enter` the object. The `+` prefix means the player must
**carry** the specified object.

### Leave Lock

```
> @lock/leave cell = *Guard | *Warden
```

Controls who can `leave` the object.

### Use Lock

```
> @lock/use machine = SKILL:engineering*
```

Controls who can `use` the object. This example uses an **attribute lock**
(explained below).

### Page Lock

```
> @lock/page me = *Friend1 | *Friend2
```

Controls who can `page` you.

### Speech Lock

```
> @lock/speech courtroom = ROLE:judge*
```

Controls who can speak in a room. Set on the room itself.

### Teleport Lock

```
> @lock/teleport here = !*Prisoner
```

Controls who can teleport to this location.

### Give Lock

```
> @lock/give sword = =me
```

Controls who can give this object away. The `=` prefix means identity --
only the exact object matches.

### Mail Lock

```
> @lock/mail me = !*Spammer
```

Controls who can send you @mail.

## Advanced Lock Types

### Attribute Locks

```
> @lock door = FACTION:Rebels
```

An attribute lock checks whether the player (or something they carry) has
a specific attribute set to a matching value. In this example, the player
must have a FACTION attribute set to "Rebels."

You can use wildcards:

```
> @lock door = RANK:*Captain*
```

Attribute locks are the most common way to build game systems. A faction
system, a class system, or a skill system can all be implemented with
attribute locks.

### Evaluation Locks

```
> @lock door = CHECK/1
```

An evaluation lock runs MUSHcode. The server evaluates the CHECK attribute
on the locked object, and if the result equals "1", the lock passes.

```
> &CHECK door = gt(get(%#/STRENGTH), 15)
```

Now the door opens only for characters with a STRENGTH attribute greater
than 15. Evaluation locks are powerful but computationally expensive.

### Indirect Locks

```
> @lock door = @#500
```

An indirect lock checks whether the player passes another object's lock.
In this example, the door checks the default lock on object #500.

This enables lock sharing: multiple objects can point to the same lock,
and changing the lock on #500 changes access for all of them.

### Identity Locks

```
> @lock throne = =*King
```

The `=` prefix means only the exact player matches -- carrying something
named "King" does not count.

### Carry Locks

```
> @lock door = +Badge
```

The `+` prefix means only carrying the object counts -- being the object
does not count.

### Owner Locks

```
> @lock building = $*Builder
```

The `$` prefix means any object owned by the specified player passes.

## Unlocking

To remove a lock:

```
> @unlock door
> @unlock/enter carriage
```

An unlocked object is accessible to everyone.

## Lock Failure Messages

Always set failure messages when you lock something:

```
> @lock door = Iron Key
> @fail door = The door is locked. You need a key.
> @ofail door = tries the door, but it is locked.
```

Without failure messages, the player gets no feedback when denied -- they
just see nothing happen, which is confusing.

## Common Lock Patterns

**A locked room with a key:**

```
> @lock east = Iron Key
> @succ east = You unlock the door and step through.
> @fail east = The door is locked solid.
> @ofail east = tries the locked door.
```

**A faction-restricted area:**

```
> @lock gate = FACTION:Alliance
> @fail gate = The guards block your path. Alliance only.
```

**A wizard-only room:**

```
> @lock entrance = FLAG^WIZARD
```

The `FLAG^` syntax checks whether the player has a specific flag set.

**A room where only certain people can speak:**

```
> @lock/speech courtroom = ROLE:judge* | ROLE:lawyer*
```

## Tips

- **Always test your locks.** Have another player (or a test character) try
  to pass.
- **Use dbrefs in locks** rather than names to avoid problems with name
  changes or duplicates.
- **Set failure messages** on every lock so players understand why they
  cannot pass.
- **Keep evaluation locks simple.** Complex evaluation locks slow down the
  server. Use attribute locks when possible.
- **Be careful with NOT locks.** `!*BadGuy` blocks one player, but you
  might want a whitelist (`=*Good1 | =*Good2`) instead.
