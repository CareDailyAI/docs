# Guides

Worked stories that cross several APIs. Each one follows a real task from start to finish and
links to the reference pages for the detail.

| Guide | You will learn |
| --- | --- |
| [The life of an alert](life_of_an_alert.md) | How a fall moves from a sensor to a bot, to the family's phones, to a partner cloud, and back when someone resolves it |
| [Watch a home live](watch_a_home_live.md) | The baseline, subscribe, react pattern behind installation tools and live dashboards |
| [Troubleshooting a home](troubleshooting.md) | The order of checks when someone says "it is not working" |

```mermaid
flowchart LR
    S["📡 Sensors"] --> P["☁️ Platform"] --> B["🤖 Bots"]
    B --> P
    P --> A["📱 Apps"]
    P --> X["🏢 Partner clouds"]
    A -->|"data stream messages"| P
    style P fill:#eef2ff,stroke:#3f3bf2,stroke-width:2px
    style B fill:#f0fdf4,stroke:#1b873f
```

For the exact request order behind each app screen, see the
[Message Sequence Charts](../message_sequence_charts/README.md).

## Related

- [Concepts](../concepts/README.md)
- [Agent Kit](../agent_kit/README.md), the same knowledge written for AI agents
