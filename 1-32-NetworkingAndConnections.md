# Networking and Connections

## Overview

A MUSH server communicates with players over TCP/IP network connections.
This chapter specifies the connection lifecycle, authentication, multiple
connections, idle management, and the interface between the network layer
and the game engine.

## Connection Lifecycle

### Listening

A conforming implementation shall listen for incoming TCP connections on one
or more configurable ports. The default port is implementation-defined
(common defaults include 2860, 4201, and 6250). The server shall bind to
all available network interfaces unless configured otherwise.

### Connection Acceptance

When a client connects, the server shall:

1. Accept the TCP connection.
2. Check the client's IP address against the site access list. If the site
   is forbidden, the server shall send a rejection message and close the
   connection.
3. Optionally resolve the client's hostname via DNS (asynchronously, to
   avoid blocking the game loop).
4. Display the connection screen (the contents of the configured connection
   file).
5. Enter the login state, awaiting authentication.

### Authentication

The client authenticates by issuing one of the following commands at the
login prompt:

```
connect <player-name> <password>
create <player-name> <password>
```

The `connect` command logs into an existing player account. The `create`
command creates a new player and logs in. The `create` command may be
disabled by server configuration.

If authentication fails, the server shall display an error message and allow
the client to retry. After a configurable number of failed attempts
(implementation-defined, typically 3-5), the server shall disconnect the
client.

### Post-Login

After successful authentication:

1. The Message of the Day (MOTD) is displayed.
2. The player's ACONNECT attribute is triggered as an action list.
3. The player's location is displayed (as though the player typed `look`).
4. Other players in the room see the player's arrival.
5. If the player has unread mail, a notification is displayed.

### Disconnection

A connection ends when:

- The player issues the `QUIT` command.
- The player issues the `LOGOUT` command (disconnects the character but
  may keep the socket open for a new login, implementation-defined).
- The idle timeout expires.
- An administrator uses `@boot` to disconnect the player.
- The server shuts down.
- The network connection is lost.

On disconnection:

1. The player's ADISCONNECT attribute is triggered.
2. Other players in the room see the player's departure.
3. If this was the player's last connection, the player is marked as
   not connected.

## Multiple Connections

A conforming implementation shall support multiple simultaneous network
connections to the same player account. Each connection is tracked
independently with its own:

- Socket descriptor.
- Connection timestamp.
- Idle timestamp.
- Input/output buffers.

All connections to the same player receive the same game output (room
descriptions, messages, etc.). Commands entered on any connection are
executed by the player.

When one connection disconnects, others remain active. The ADISCONNECT
attribute is triggered only when the **last** connection disconnects
(implementation-defined; some implementations trigger it on every
disconnection with the remaining connection count available as a parameter).

## Idle Timeout

The server shall enforce an idle timeout. If a connected player does not
issue any commands within the timeout period, the connection is
automatically closed. The default idle timeout is implementation-defined
(commonly 3600 seconds / 1 hour).

The timeout may be overridden per-player via the TIMEOUT attribute on the
player object. Players with the IDLE power (or equivalent) are exempt from
idle timeouts.

## Connection Attributes

The following attributes on player objects are triggered during connection
events:

| Attribute | Triggered |
|-----------|-----------|
| ACONNECT | When the player connects (after login). |
| ADISCONNECT | When the player disconnects. |

These attributes are evaluated as action lists. Within ACONNECT and
ADISCONNECT, the following substitutions are available
(implementation-defined):

| Parameter | Description |
|-----------|-------------|
| `%#` | The connecting/disconnecting player. |
| `%1` | The number of connections remaining (after the event). |

## Global Connection Attributes

The master room (object #0) may have ACONNECT and ADISCONNECT attributes
that are triggered for all player connections and disconnections. These
global attributes enable server-wide login/logout processing.

## Site Access Control

The server shall support IP-based access control to restrict connections
from specific addresses or networks. The access control list (ACL) is
maintained by the server administrator and supports:

- Allowing or forbidding specific IP addresses.
- Allowing or forbidding IP address ranges (subnets).
- Restricting specific sites to guest access only.
- Restricting specific sites from creating new characters.

The ACL is configured through the server configuration file or
administrative commands. The specific syntax is implementation-defined.

## Connection Information Functions

The following functions provide information about active connections:

| Function | Returns |
|----------|---------|
| `lwho()` | List of dbrefs of connected players. |
| `mwho()` | List of connected non-DARK players. |
| `nwho()` | Count of connected players. |
| `conn(<player>)` | Seconds since connection. |
| `idle(<player>)` | Seconds since last command. |
| `doing(<player>)` | Player's DOING string. |

## WHO Command

The `WHO` command displays a list of connected players with their names,
connection times, idle times, and DOING messages. Players with the DARK
flag (and appropriate powers) or the UNFINDABLE flag may be hidden from the
WHO list, depending on server configuration.

Wizards see an enhanced WHO list that includes player dbrefs, IP addresses,
and port numbers.

## SSL/TLS

Some implementations support encrypted connections via SSL/TLS. When
supported, the server listens on an additional port for secure connections.
The SSL/TLS implementation is entirely implementation-defined. Level 2.

## Implementation Notes

The network layer shall be non-blocking. A conforming implementation shall
not allow a single slow or unresponsive client to block the game loop or
delay processing for other connected players.

Input from clients shall be buffered and processed as complete lines
(terminated by newline characters). Output to clients shall be buffered
and flushed efficiently.

The maximum number of simultaneous connections is implementation-defined but
shall be configurable. Implementations should support at least 100
simultaneous connections.
