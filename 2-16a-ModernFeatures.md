# Modern Features

## Overview

The earliest MUSH servers shipped a small, self-contained feature set
— attributes, locks, channels, mail — that has been stable for
decades. The modern reference implementations, particularly TinyMUX
2.14 and PennMUSH, have quietly added capabilities that bring MUSH
into the same world as contemporary web and game technology: JSON
manipulation, SQL database integration, WebSocket connections, and
the Generic Mud Communication Protocol (GMCP) for rich client
integration.

These features are **not** universally available. TinyMUX 2.14 has
the most complete modern feature set and is the reference for this
chapter; PennMUSH has SQL, partial JSON, and WebSocket support;
TinyMUSH and RhostMUSH vary. Check your server's help before relying
on any of them.

## JSON

Modern MU* servers increasingly need to exchange data with web
services, dashboards, or tooling that speaks JSON. TinyMUX 2.14
provides a set of softcode functions for producing, inspecting, and
mutating JSON values.

### Producing JSON

```
> think json(string, Hello)
"Hello"
> think json(number, 42)
42
> think json(boolean, 1)
true
> think json(array, 1 2 3)
[1,2,3]
> think json(object, name "Morgan" age 30)
{"name":"Morgan","age":30}
```

### Validating JSON

```
> think isjson({"name":"Bob"})
1
> think isjson(not json)
0
> think isjson(42, number)
1
```

`isjson()` returns 1 if its argument is a well-formed JSON value. The
optional second argument restricts the match to a specific type.

### Querying JSON

```
> think json_query({"name":"Bob","age":30}, get, $.name)
"Bob"
> think json_query({"name":"Bob","age":30}, keys)
name age
> think json_query([10,20,30], size)
3
> think json_query({"a":1}, exists, $.a)
1
```

`json_query()` uses JSONPath syntax (`$` for the root, `.name` for
object fields, `[n]` for array indices) to pull values out of a JSON
document.

### Mutating JSON

```
> think json_mod({"a":1}, set, $.b, 2)
{"a":1,"b":2}
> think json_mod({"a":1}, remove, $.a)
{}
> think json_mod([1,2,3], replace, $[1], 99)
[1,99,3]
```

`json_mod()` returns a new JSON value with the requested edit applied.

### Practical Example: Emitting a GMCP Message

```
> &FN_ROOM_INFO me = json(object, id %0 name %1 exits %2)
> gmcp(*Sparrow, Room.Info, u(FN_ROOM_INFO, 42, Town Square, {n e s}))
```

This packages a room description as a GMCP `Room.Info` message and
sends it to a modern client, which can then render a map sidebar or a
navigation widget.

## SQL Integration

TinyMUX and PennMUSH can connect to an external SQL database and
execute queries directly from softcode.

### Single-Result Queries

```
> think sql(SELECT name FROM characters WHERE id=42)
Morgan
> think sql(SELECT name\, hp FROM characters WHERE id=42, |, ~)
Morgan~80
```

The single-argument form returns a row-delimited list of results.
The optional second and third arguments set the row and column
delimiters. Note that commas within the query must be escaped with
`\` so the MUSHcode parser does not treat them as argument
separators.

### Cursor-Based Queries (TinyMUX, optional)

TinyMUX optionally exposes a cursor API for streaming large result
sets. The functions are compiled in only when TinyMUX is built with
the `STUB_SLAVE` distributed-architecture option, which is **not**
enabled in the standard build. On a stock TinyMUX server these
functions are absent — `sql()` is the portable baseline. Where the
cursor API is available it looks like this:

```
> think rsopen(SELECT name\, hp FROM characters WHERE faction='Red')
0
> think rsrecnext(0)
Morgan 80
> think rsrecnext(0)
River 95
> think rsclose(0)
```

`rsopen()` returns a cursor ID, `rsrecnext()` advances to the next
row and returns it, and `rsclose()` releases the cursor. Before
relying on the cursor API, confirm with the server admin (or via
`@list functions` / `help rsopen`) that this build has it.

### Security Warning

SQL access is powerful and dangerous. Any softcode author with SQL
permission can read (and, if the database user has write access,
modify) everything in the connected database. Gate SQL access behind
a dedicated power (PennMUSH's `Sql_Ok`, TinyMUX's `sql` power), audit
which objects have that power, and never construct queries by string
concatenation from player input.

## WebSockets and GMCP

Traditional MUSH clients speak plain telnet. Modern clients may speak
WebSockets (for browser-based connections) or use GMCP (an out-of-band
telnet subnegotiation) to exchange structured data.

### WebSocket Connections

TinyMUX 2.14 accepts WebSocket connections on the same port as
telnet. A browser-based client connecting via WebSocket is
indistinguishable from a telnet client at the softcode level — the
same `%#` identifies the enactor, the same `@pemit` reaches them, the
same commands work.

What changes is the I/O: WebSocket clients can receive binary frames
and structured messages alongside normal game text, which is where
GMCP comes in.

### GMCP: Sending Structured Data

GMCP lets the server push named, JSON-formatted messages to the
client out-of-band. The client can display them however it wishes: a
health bar, a map, a sidebar, an inventory panel.

```
> gmcp(Sparrow, Char.Vitals, {"hp": 80, "maxhp": 100, "mp": 50})
> gmcp(Sparrow, Room.Info, {"id": 42, "name": "Town Square"})
```

Each call sends a single GMCP message. The first argument is the
recipient player; the second is the package name (conventionally
`Category.Subtype`); the third is the JSON payload.

### Receiving GMCP from the Client

Modern clients may also send GMCP messages back to the server, and a
softcoded handler can receive them. TinyMUX triggers a configurable
attribute when a GMCP message arrives, providing the package name and
payload as arguments. See the server's `help gmcp` for the exact
interface and configuration steps.

### Practical Example: Health Bar

A simple health-bar integration:

```
> &FN_UPDATE_VITALS me = gmcp(%0, Char.Vitals,
  json(object, hp v(%0/HP) maxhp v(%0/MAXHP)))
> &AHP_CHANGE me = $+hp *:
  &HP me = %0;
  u(FN_UPDATE_VITALS, %#)
```

Whenever a player's HP changes, the server pushes a Char.Vitals GMCP
message. A GMCP-aware client displays the updated health bar in real
time.

## Portability and Fallback

If your game must run on multiple engines, wrap modern features in a
feature-detection layer:

```
> &CAP_JSON me = [strmatch(lit([config(json)]), 1)]
> &SAFE_SEND me = [switch(v(CAP_JSON), 1,
    [gmcp(%0, %1, %2)],
    [pemit(%0, [json_fallback_text(%2)])])]
```

On engines without JSON or GMCP support, the same softcode falls back
to plain-text emission. This is more work than writing only for
TinyMUX, but it keeps your code deployable.

## Tips

- **Version-check.** These features evolve quickly. A script that
  works on TinyMUX 2.14 may fail on 2.13. Version-detect and branch.
- **Benchmark.** JSON parsing and SQL queries are more expensive than
  string handling. Avoid calling them in hot loops.
- **Document for your staff.** If your game uses GMCP for a health
  bar, write down which package name and payload shape you use —
  otherwise the next developer will have to reverse-engineer it.
- **Keep a telnet fallback.** Plain-text output is still the contract
  with users. GMCP should enrich the experience, not replace it.
