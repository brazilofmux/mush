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

The exact syntax varies by server, but the most common commands are:

```
> @channel/join Public
You have joined channel Public.
> @channel/leave Public
You have left channel Public.
```

Some servers use `addcom` and `delcom` instead:

```
> addcom pub = Public
Channel alias 'pub' set to channel Public.
> delcom pub
Channel alias 'pub' removed.
```

The alias lets you talk on the channel with a short prefix instead of
typing the full name every time.

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

Without an alias, use the full command:

```
> @channel/emit Public = Hello everyone!
```

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

## Muting and Gagging

If a channel is too busy, you can mute it without leaving:

```
> @channel/mute Public
You have muted channel Public.
> @channel/unmute Public
You have unmuted channel Public.
```

When muted, messages still go to the channel but you do not see them.
You remain a member and can unmute at any time.

## Creating Your Own Channel

If you have permission (usually builders or staff), you can create
channels:

```
> @channel/add Trading
Channel Trading created.
> @channel/desc Trading = Buy, sell, and trade items.
```

### Channel Locks

Control who can join, speak, or see a channel:

```
> @clock/join Trading = FLAG^APPROVED
> @clock/speak Trading = FLAG^APPROVED
```

This restricts the Trading channel to approved players only. Lock syntax
follows the same patterns described in the Locks and Security chapter.

### Channel Settings

Common configuration options:

```
> @channel/priv Trading = no_titles
> @channel/priv Trading = quiet
```

`no_titles` suppresses player titles in channel output. `quiet` hides
join and leave messages.

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
