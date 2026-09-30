# 02. Discovery

Before an agent reads or writes anything, it should know which cloud it is on, where the specs are,
and what exists on the home in front of it. Every call in this file is a read.

---

## Which cloud?

| Cloud | API base URL |
| --- | --- |
| Sandbox | `https://sboxall.peoplepowerco.com` |
| US production | `https://app.peoplepowerco.com` |
| EU production | `https://eu.caredaily.ai` |

These are the servers the [Application API reference](https://app.caredaily.ai/cloud/apidocs/cloud.html)
lists. Confirm with no key:

```bash
curl -s "$CAREDAILY_SERVER/cloud/json/settings"          # every cloud and its servers
curl -s "$CAREDAILY_SERVER/cloud/json/settingsServer/wsapi"   # this cloud's WebSocket server
curl -s "$CAREDAILY_SERVER/espapi/watch"                 # "OK" when up
```

**IDs, accounts and keys are per cloud.** An organization, location, user or device ID from
sandbox means nothing on production. Never reuse one across clouds.

---

## The specs

Fetch them live when you need an endpoint you have not used before. They change.

```bash
curl -s https://app.caredaily.ai/cloud/apidocs/yaml/cloud.yaml -o cloud.yaml
curl -s https://app.caredaily.ai/cloud/apidocs/yaml/admin.yaml -o admin.yaml
curl -s https://app.caredaily.ai/cloud/apidocs/yaml/bots.yaml  -o bots.yaml
```

| Spec | Paths | Covers |
| --- | --- | --- |
| `cloud.yaml` | `/cloud/json/...`, `/cloud/appstore/stream`, `/cloud/appstore/summary` | Users, locations, devices, parameters, states, narratives, notifications, data stream messages |
| `admin.yaml` | `/admin/json/...`, `/reports/...` | Organizations, organization users, locations and devices, admins, the object store, reports |
| `bots.yaml` | `/cloud/appstore/...`, `/cloud/developer/...`, `/analytic/...` | Bot instances, and the developer API for building bots |

The WebSocket protocol and event streaming formats are not in the specs. They are in this
repository: [WebSockets](../platform_apis/websockets.md) and
[Event Streaming](../platform_apis/event_streaming.md).

---

## What does this key reach?

```bash
source ~/.caredaily/key.env
H=(-H "API_KEY: $CAREDAILY_API_KEY" -H "Accept: application/json")

curl -s "$CAREDAILY_SERVER/cloud/json/user" "${H[@]}"                        # me, and my locations
curl -s "$CAREDAILY_SERVER/admin/json/organizations?organizationId=<id>" "${H[@]}"   # an org I administer
```

The organization row's ID field is `id`, and `parentId` walks up the hierarchy.

---

## What exists on this home?

| Question | Call |
| --- | --- |
| Who is here? | `GET /cloud/json/location/{locationId}/users` |
| What devices? | `GET /cloud/json/devices?locationId={locationId}` |
| Which rooms? | `GET /cloud/json/location/{locationId}/spaces` |
| Which bots run here? | `GET /cloud/appstore/appInstance?locationId={locationId}` |
| Which data stream addresses do those bots accept? | `GET /cloud/appstore/summary?locationId={locationId}` |
| Which service plans? | `GET /cloud/json/userServicePlans?locationId={locationId}` |

`/cloud/appstore/summary` returns `dataStreams[]`. Check an address is there before you send to it.

---

## A control query, always

Before you conclude that something does not exist, run the same query against a home or an
organization where you know it does. An empty answer from a filter that the endpoint silently
ignores looks exactly like "nothing found", and so does a key on the wrong cloud.

## Related

- [03 Reading data](03_reading_data.md)
- [Concepts](../concepts/README.md)
