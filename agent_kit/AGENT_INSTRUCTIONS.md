# Care Daily platform work

Copy this file into the root of the project your agent works in (as `CLAUDE.md`, `AGENTS.md` or
equivalent), or append it to the instruction file you already have. Fix the path below to where you
cloned the documentation.

---

## Reference kit

The Care Daily Agent Kit is at `~/caredaily-docs/agent_kit/`. **Read `README.md` and
`04_safe_writes.md` before any platform work**, then the numbered file that covers the task.

The live OpenAPI specs are the source of truth. Check an endpoint there before you use it for the
first time:

- `https://app.caredaily.ai/cloud/apidocs/yaml/cloud.yaml` (Application API)
- `https://app.caredaily.ai/cloud/apidocs/yaml/admin.yaml` (Admin API and reports)
- `https://app.caredaily.ai/cloud/apidocs/yaml/bots.yaml` (Bots, bot instances, developer API)

## Credentials

The username, password and server are in `$CAREDAILY_USER`, `$CAREDAILY_PASSWORD` and
`$CAREDAILY_SERVER`. The minted key lives in `~/.caredaily/key.env` as `CAREDAILY_API_KEY`.

**Never print, echo, log or write a password, passcode or API key anywhere.** That covers the
terminal, files in a repository, commits, messages, and partial values such as the first few
characters. Reference `$CAREDAILY_API_KEY` in commands; report a key only by its type and expiry.

## Standing rules

1. **Sandbox first.** Learn and test on the sandbox cloud. Production is read-only unless a person
   has named the specific change in this conversation.
2. **Say which cloud, organization and location you are about to write to**, before every write.
   Sandbox and production look identical from a terminal.
3. **Stay inside your own organizations.** Pass `organizationId` explicitly on every
   organization-scoped call. If a result names a person or a home outside them, stop and do not
   show it.
4. **Never delete** an organization, location, device, user, space or organization object. Ask a
   person.
5. **Change bot output by messaging the bot**, never by writing its state directly.
6. **One home per data stream message.** Always pass `locationId`.
7. **Read back every write that matters.** `resultCode 0` on a device command means queued.
8. **Never touch a bot you do not own.** Do not publish over, pause, reconfigure or delete it.
9. **An empty result proves nothing on its own.** Run a query you know returns rows, as a control,
   before you tell anyone something does not exist.
10. **Say when you are guessing.** Mark anything you took from a spec but have not run against a
    live server.
11. **Back off on errors.** Never retry a login in a loop, and slow down on `resultCode 44`.
12. **Personal data stays minimal.** One person at a time, for the task in front of you. No bulk
    copies into another system without a person's decision.
13. **When stuck, stop and ask** a person, with the cloud, IDs, calls and result codes, and no
    credentials.
