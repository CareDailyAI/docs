# For AI agents

If you are an AI agent reading this repository to learn how to work with the Care Daily platform,
start with [agent_kit/README.md](agent_kit/README.md), then read
[agent_kit/AGENT_INSTRUCTIONS.md](agent_kit/AGENT_INSTRUCTIONS.md) and follow its standing rules.

The short version:

- The live OpenAPI specs are the source of truth:
  `https://app.caredaily.ai/cloud/apidocs/yaml/cloud.yaml`, `admin.yaml` and `bots.yaml`.
- Sandbox first. Production writes only when a person has named the change.
- Never print, log or commit a password, passcode or API key.
- `resultCode 0` on a device command or a data stream message means accepted, not done. Read back.
- Change what a bot shows by sending it a data stream message, never by overwriting its state.
- Anything marked **TODO(verify)** in these docs is unconfirmed. Say so if you rely on it.
