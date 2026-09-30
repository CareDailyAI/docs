# 05. Errors and retries

Every response has a `resultCode`. `0` is success. This file tells an agent what to do with
everything else, and how to be a polite client.

The full table with explanations is in [Result codes and gotchas](../platform_apis/result_codes.md).

---

## Decide by code

| Code | Kind | Do |
| :---: | --- | --- |
| `2` | Key expired or wrong cloud | Mint a new key on the right cloud, once. Retry once |
| `7` | Access denied | Check the key type (`11` for organization calls) and the scope. Do not retry |
| `8`, `9`, `14` | Bad request | Fix the request. `8` at login is an unencoded `%` in the password |
| `12` | Login refused | Stop. Check encoding, and that step two sends `passcode` without `PASSWORD`. Never loop |
| `16` | Account locked | Stop and tell a person |
| `17` | Passcode sent | Expected. Wait for the person to supply it |
| `19` | Temporarily locked | Wait `lockTimeout` milliseconds |
| `21` | Device offline | Report it. Retrying will not wake the device |
| `29` | No such API | Wrong path or method. `/reports/...` has no `/admin/json` prefix |
| `1`, `27`, `30` | Server side | Back off and retry, a few times at most |
| `44` | Too many calls | Back off, then continue slower |

---

## Back-off

```python
import time

TRANSIENT = {1, 27, 30, 44}

def with_backoff(call, attempts=4):
    delay = 1.0
    for i in range(attempts):
        j = call()
        code = j.get("resultCode", 0)
        if code == 0:
            return j
        if code == 19 and j.get("lockTimeout"):
            time.sleep(j["lockTimeout"] / 1000)
            continue
        if code not in TRANSIENT or i == attempts - 1:
            return j                      # let the caller report it
        time.sleep(delay)
        delay *= 2
    return j
```

Never wrap a **login** in this. Repeated failed logins lock the account, and each step-one call of
an administrator login throws away the previous passcode.

---

## Etiquette

- **Prefer push to polling.** Subscribe over [WebSockets](06_live_events.md) rather than reading
  the same state every few seconds.
- **Ask for what you need.** Filter with `paramName`, `locationId`, `organizationId` and `rowCount`
  rather than pulling everything and filtering locally.
- **Run sweeps sequentially.** When an organization-wide task needs many calls, make them one at a
  time with a short pause, and stop at the first unexpected error.
- **HTTP 404 on `/reports/data/{token}` means "not ready".** Poll a few times, a few seconds apart.

> **TODO(verify):** the platform's published rate limits, if any. Until they are documented, treat
> `resultCode 44` as the signal and slow down when you see it.

---

## Success that is not success

- A device command's `0` means queued.
- A data stream message's `0` means accepted for delivery.
- A bot-owned state you wrote directly will be rewritten.
- A filter the endpoint does not support is ignored, and you get everything.

When it matters, read it back.

## Related

- [04 Safe writes](04_safe_writes.md)
- [Result codes and gotchas](../platform_apis/result_codes.md)
