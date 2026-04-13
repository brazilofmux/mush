# Channels

## What Are Channels?

Channels are global communication lines that work across rooms. Unlike
`say` and `pose`, which are limited to the people in your current
location, a channel message reaches every connected player who has joined
that channel -- no matter where they are on the grid.

Most MUSHes have several channels: a public chat channel, a staff
channel, a newbie help channel, and often game-specific ones like an
out-of-character (OOC) channel or a trade channel.

## Joining and Leaving Channels

Commands diverge between PennMUSH and TinyMUX. Use whichever set your
server accepts — `help @channel` or `help addcom` will tell you.

On PennMUSH:

```
> @channel/on Public
You have joined channel Public.
> @channel/off Public
You have left channel Public.
```

On TinyMUX, membership is managed through aliases: creating an alias
joins you, removing the alias removes you. PennMUSH accepts the
alias commands too and usually treats them as the preferred form:

```
> addcom pub = Public
Channel alias 'pub' set to channel Public.
> delcom pub
Channel alias 'pub' removed.
```

The alias also lets you talk on the channel with a short prefix
instead of typing the full name every time.

## Talking on a Channel

With an alias set, prefix your message with the alias:

```
> pub Hello everyone!
<Public> Sparrow says, "Hello everyone!"
```

You can also pose on a channel:

```
> pub :waves.
<Public> Sparrow waves.
```

Without an alias, use `@cemit` (both engines):

```
> @cemit Public = Hello everyone!
```

`@cemit` broadcasts a plain message to the channel without speaker
attribution and typically requires that you be a member of the
channel (or have wizard privileges).

## Listing Channels

To see what channels are available:

```
> @channel/list
Name         Owner    Description
Public       #1       General chat for everyone
Staff        #1       Staff-only discussion
Newbie       #1       Help for new players
```

To see who is on a channel:

```
> @channel/who Public
Players on channel Public:
  Sparrow    Morgan    River
```

## Channel Etiquette

- **Stay on topic.** If a channel has a stated purpose, respect it.
- **Keep it friendly.** Channels reach many people at once. Heated
  arguments are better taken to pages.
- **Use the right channel.** Do not ask staff questions on the public
  channel when a help channel exists.
- **Mute when away.** If you are going idle for a long time, consider
  temporarily muting busy channels so you do not flood your scroll
  when you return.

## Muting and Silencing

If a channel is too busy, you can silence it without leaving. On
TinyMUX, toggle your alias off and on:

```
> pub off
Alias 'pub' is now quiet.
> pub on
Alias 'pub' is active again.
```

On PennMUSH, two distinct switches control two different things:

```
> @channel/gag Public         (suppress all channel messages)
> @channel/mute Public        (suppress connect/disconnect notices)
> @channel/ungag Public
> @channel/unmute Public
```

"Gag" is the one you want for "too busy, stop showing me messages."
"Mute" only silences the join/leave/connect/disconnect spam. When
silenced by any of these mechanisms, messages still go to the channel
but you do not see them; you remain a member and can re-enable at
any time.

## Creating Your Own Channel

If you have permission (usually builders or staff), you can create
channels. Syntax depends on engine:

```
> @channel/add Trading           (PennMUSH)
> @ccreate Trading               (TinyMUX)
```

Set a description with `@channel/describe Trading = ...` (PennMUSH)
or by assigning an appropriate attribute / using `@cset` on TinyMUX.
Consult the server's help for its exact administration verb.

### Channel Locks

Control who can join, speak, or see a channel. PennMUSH uses the
`@clock` command:

```
> @clock/join Trading = FLAG^APPROVED
> @clock/speak Trading = FLAG^APPROVED
```

TinyMUX has no `@clock`; access is set via `@cset/<option>` and
`@coflags`/`@cpflags`, plus the lock on the channel's underlying
object. Lock key expressions themselves follow the same patterns as
the object locks described in the Locks and Security chapter.

### Channel Settings

Common configuration options vary:

```
> @channel/privs Trading = notitles    (PennMUSH: suppress player titles)
> @channel/privs Trading = quiet       (PennMUSH: suppress join/leave notices)
> @cset quiet Trading                  (TinyMUX: equivalent quiet option)
```

Portable admin code should consult the target engine's help for the
exact command surface.

## Practical Example: Setting Up Communication

A typical new player setup looks like this:

```
> addcom pub = Public
> addcom ooc = OOC
> addcom help = Newbie
> pub Hey, just joined! Any tips for getting started?
<Public> Sparrow says, "Hey, just joined! Any tips for getting started?"
```

Now you have three channels available with short, easy aliases.

## Tips

- **Check available channels early.** One of the first things to do on a
  new MUSH is list channels and join the public ones.
- **Keep aliases short.** Single letters or short abbreviations save
  typing: `p` for Public, `o` for OOC.
- **Channels are OOC by default.** Most channels are out-of-character
  communication. In-character interaction usually happens through room
  commands.
