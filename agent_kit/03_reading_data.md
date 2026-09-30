# 03. Reading data

Recipes for the reads an agent does most, with the parsing traps attached. Everything here is a
`GET`. Organization-wide reads need an administrator key.

---

## Setup

Shell state rarely persists between an agent's commands, so start each one with:

```bash
source ~/.caredaily/key.env
cdget() { curl -s -G "$CAREDAILY_SERVER$1" "${@:2}" -H "API_KEY: $CAREDAILY_API_KEY" -H "Accept: application/json"; }
```

Example: `cdget /cloud/json/devices --data-urlencode "locationId=123456" | python -m json.tool`

Or in Python:

```python
import json, os, urllib.parse, urllib.request
SERVER, KEY = os.environ["CAREDAILY_SERVER"].rstrip("/"), os.environ["CAREDAILY_API_KEY"]

def get(path, **params):
    url = f"{SERVER}{path}?{urllib.parse.urlencode(params, doseq=True)}"
    req = urllib.request.Request(url, headers={"API_KEY": KEY, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.load(r)
    if j.get("resultCode", 0) != 0:
        raise RuntimeError(f"{path}: resultCode {j.get('resultCode')} {j.get('resultCodeMessage', '')}")
    return j
```

---

## Find a person

```bash
cdget /admin/json/users --data-urlencode "organizationId=<org>" --data-urlencode "searchBy=pat@example.com"
```

- **No match returns no `users` field at all**, only `{"resultCode": 0}`.
- **Try variants before you say "no account":** `pat+*@example.com` and `pat*`. Plus-addressed
  sign-ups hide from an exact search.
- **More than one match?** Show the list and let a person choose. Never pick silently.

Then read the account and its homes:

```bash
cdget /cloud/json/user --data-urlencode "userId=<id>"
```

`locations[]` lists each home, with `locationUser` holding this person's access, role and category
there. `/admin/json/locations` has **no** `userId` filter; do not use it to go from a person to a
home.

## Read a home

```bash
cdget /cloud/json/location/<loc>/users                         # the Trusted Circle
cdget /cloud/json/devices --data-urlencode "locationId=<loc>"  # devices, with current parameters
cdget /cloud/json/devices/<deviceId>/parameters --data-urlencode "locationId=<loc>"
```

- Parameters are at **`devices[0].parameters[]`**, each `{name, value, lastUpdateTime}`.
- **Values are strings.** Compare with `"1"`.
- **Online or offline:** use `lastDataReceivedDateMs`, not `connected`.

## Read history

| What | Call |
| --- | --- |
| A parameter over time | `/cloud/json/devices/{deviceId}/parametersByDate/{startDate}?locationId=&paramName=&sortOrder=desc` |
| The timeline the app shows | `/cloud/json/locations/{loc}/narratives?rowCount=50` (page with `nextMarker` → `pageMarker`) |
| Mode changes | `/cloud/json/location/{loc}/events` |
| What was sent to a person | `/cloud/json/notifications?userId=&startDate=` (`startDate` is required) |

Dates can be ISO 8601 or epoch milliseconds. Prefer the `...Ms` fields in responses for arithmetic.

## Read bot output

```bash
cdget /cloud/json/locations/<loc>/state --data-urlencode "name=dashboard_header"
cdget /cloud/json/locations/<loc>/state --data-urlencode "name=now" --data-urlencode "name=insights"
```

One `name` returns `value`; several return `states[]`. The formats are in
[Synthetic APIs](../synthetic_apis/README.md). An empty state can mean the bot has not written it
yet; check that a bot runs on the home before you call it broken (see [02](02_discovery.md)).

## Organization-wide views

```bash
cdget /admin/json/devices --data-urlencode "organizationId=<org>" --data-urlencode "deviceType=<type>"
cdget /admin/json/locations --data-urlencode "organizationId=<org>" --data-urlencode "searchBy=<name*>"
cdget /admin/json/organizations/<org>/narratives --data-urlencode "rowCount=50"
```

Always pass `organizationId`.

---

## Personal data

Users, contacts, notifications and report rows are personal data. Read them for the one person or
home the task is about, show what the task needs, and keep no copy. Never sweep an organization's
users to build a list.

## Related

- [Working with the REST API](../platform_apis/conventions.md)
- [Troubleshooting a home](../guides/troubleshooting.md)
