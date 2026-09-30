# 06. Live events

Server push, with no polling. An agent that watches a home live can confirm a change the moment it
happens: a door opens, a setting applies, a bot updates the dashboard.

The protocol is in [WebSockets](../platform_apis/websockets.md), including a complete Python client.
This file is the agent's checklist.

---

## The sequence

1. **Baseline over REST.** Read the current values first:
   `GET /cloud/json/devices/{deviceId}/parameters?locationId=`.
2. **Ask for the server.** `GET /cloud/json/settingsServer/wsapi` returns `host`, `port`, `path`
   and `ssl`. Connect to `wss://host:port/path`. Ask each session; do not hardcode it.
3. **Authenticate.** `{"goal": 1, "id": "1", "key": "<API key>"}`. Build this message inside the
   program from `$CAREDAILY_API_KEY`, and never log it.
4. **Subscribe, one home.**

   | `type` | Data | Typical `operation` |
   | :---: | --- | :---: |
   | 1 | Location narratives | 7 |
   | 2 | Organization narratives | 7 |
   | 3 | Location state variables (add `name`) | 3 |
   | 6 | Device parameters | 1 |
   | 8 | SIM card attributes (needs `deviceId`) | 2 |

   `operation` is a bitmask: 1 create, 2 update, 4 delete.
5. **Receive** `goal` 6 messages and diff them against the baseline.
6. **Keep alive.** Send `?` every 15 to 30 seconds and expect `!`. Answer the server's `?` with
   `!`. Reconnect when a pong does not arrive.

---

## Running a watcher from an agent

Run the watcher as a long-lived background process that prints one line per event, and let each
line reach the conversation as it arrives. In Claude Code, the `Monitor` tool does this. The person
can then act ("open the back door"), and the agent sees the event land without polling.

Keep the output small: device ID, parameter name, new value, time. Never print the authentication
message.

## Tips

- **Shrink the watch list** as devices are identified.
- **Know the parameter.** Door sensors report `doorStatus` and many motion sensors `motionStatus`,
  each `"1"` or `"0"`. When a sensor stays silent, read its full parameter list and see what moved.
- Python with `websocket-client` or `websockets` is the easiest client to write. On Windows
  PowerShell 5.1, avoid cancelling a pending receive: it aborts the socket.

## Related

- [WebSockets](../platform_apis/websockets.md)
- [Watch a home live](../guides/watch_a_home_live.md)
