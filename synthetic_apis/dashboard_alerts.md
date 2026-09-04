# Synthetic API: Dashboard Alerts

This page catalogs every alert that a care-enabled location can publish through the `dashboard_header` state variable, so that external partners and app developers can recognize, render, and clear each one.

It is a companion to [Dashboard Header](dashboard_header.md), which documents the JSON schema, the `resolution` and `feedback` objects, and the `contact_ecc` flow. This page does not repeat that field reference. Every value below was checked against the bot microservices that produce the headers (see [References](#references)).

## Overview

### How alerts reach your application

`dashboard_header` is a location state variable holding a single JSON object: the highest-priority header currently active for the location. Many microservices each contribute a header; the dashboard header microservice keeps the whole stack and publishes only the winner. Between headers of equal priority, one tied to an active conversation wins, otherwise the one with the lowest internal "percent good" wins.

Subscribe to the state variable over [WebSockets](../platform_apis/websockets.md) or [poll it](https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Synthetic-APIs/operation/Get%20Location%20State). Each change replaces the previous value. When the winning alert is removed, the state variable falls back to the next header in the stack, typically a priority 0 or 1 status such as occupancy or "last seen".

### Example

```json
{
  "name": "radar_fall_2007",
  "priority": 6,
  "title": "Help needed!",
  "comment": "Fall detected.",
  "icon": "exclamation-circle",
  "icon_font": "far",
  "updated_ms": 1714200000000,
  "ttl_ms": 43200000,
  "external_partner": true,
  "alert_status": 1,
  "call": true,
  "ecc": true,
  "resolution": {
    "button": "UPDATE STATUS >",
    "title": "Update Status",
    "datastream_address": "conversation_resolved",
    "content": {
      "microservice_id": "61ab3699-6fce-41d3-9bf5-4e98ce054ddf",
      "conversation_id": "59f7de56-8d86-4060-a7ac-2be6996a1199"
    },
    "response_options": [
      {
        "text": "Resolve this alert.",
        "ack": "Okay, resolving the notification...",
        "icon": "thumbs-up",
        "icon_font": "far",
        "content": { "answer": 1 }
      }
    ]
  },
  "feedback": {
    "quantified": "Did People Power Family do a good job?",
    "verbatim": "What do you think caused the alert?",
    "datastream_address": "conversation_feedback",
    "content": {
      "microservice_id": "61ab3699-6fce-41d3-9bf5-4e98ce054ddf",
      "conversation_id": "59f7de56-8d86-4060-a7ac-2be6996a1199"
    }
  }
}
```

See [Dashboard Header](dashboard_header.md) for the meaning of every field, including `call`, `ecc`, `user_id`, and `alert_status`.

### Deciding what to render

Render a header as an alert when `priority` is 5 or 6 and its `name` matches one of the alerts in this page. Use `name` as the routing key, with prefix matching for the names that carry a suffix (`radar_fall_*`, `positional_fall_*`, `sedentary_*`).

The `external_partner` flag marks headers the bots intend for partner dashboards, but do not rely on it alone:

* Headers are replaced wholesale on each update. Several alerts set `external_partner` only on their first publish, so the flag disappears when the conversation escalates and the comment changes (radar falls and wearable falls behave this way).
* One partner-relevant alert, `sedentary_*`, never sets the flag.

Headers with `priority` 0 to 4 are system and status information (occupancy, last seen, installation progress, device battery, connectivity). Do not render them as alerts.

### Clearing

An alert disappears from `dashboard_header` when any of these happen:

* **Resolution from your application.** If a `resolution` object is present, send the merged `resolution.content` and the selected option's `content` to `resolution.datastream_address`. Conversation-driven alerts use `conversation_resolved`; one-shot alerts use `resolve_dashboard_header`. Always send to the address in the object. See [Dashboard Header](dashboard_header.md#resolution) for the message format.
* **Time to live.** When `ttl_ms` is present, the bot schedules deletion of that header `ttl_ms` milliseconds after it was published. The value is informational to the app.
* **Condition clears.** Activity resumes, the resident leaves the chair, the resident returns to bed, the pacing stops, or the conversation is resolved or times out over SMS or voice. The producing microservice deletes its own header.

Always display the latest `dashboard_header` value, and clear your alert view when the published header is no longer one of the alerts listed here.

## Critical Alerts (priority 6)

### Radar Fall Detection

| Field | Value |
|---|---|
| **Event name** | `radar_fall_{device_type}`, or `radar_fall` if the device type is unknown. Prefix-match on `radar_fall`. |
| **Device types** | `2000` Vayyar Care, `2003` Nobi, `2007` Pontosense, `2020` AeroSense Assure. |
| **Service toggle** | `care.radar` |
| **What it is** | A radar sensor detected a fall. |
| **Title** | "Help needed!". Becomes "Help needed and confirmed!" during the follow-up labeling conversation that confirms the fall. |
| **Comment** | "Fall detected." or the fall text supplied by the radar microservice, plus an escalation suffix (see below). |
| **Icon** | `exclamation-circle` |
| **Recommended header** | "Fall Detected" |
| **Recommended body** | "A fall has been detected. Please check on the resident." |
| **Clearing** | Conversation-driven (`conversation_resolved`). `ttl_ms` is 12 hours. Deleted by the bot when the conversation ends. |
| **Notes** | `external_partner: true` and `alert_status: 1` are set only on the first publish. Escalation updates omit both fields. When the fall is resolved, a `recent_fall_resolved` warning follows. |

### Wearable Fall Detection

| Field | Value |
|---|---|
| **Event name** | `positional_fall_{device_id}`. Prefix-match on `positional_fall`. |
| **Device types** | `2031` Intrex Multi Button, `2006` Comarch MPers Button, `4280` Becklar Belle X. |
| **Service toggle** | None. Active whenever a supported wearable is present. |
| **What it is** | A wearable button with fall detection reported a fall. The suffix is the device ID, so two wearables in one location produce distinct headers. |
| **Title** | "Help needed!". Becomes "Help needed and confirmed!" during the follow-up labeling conversation. |
| **Comment** | "Fall detected." or the text supplied by the device, plus an escalation suffix. |
| **Icon** | `exclamation-circle` |
| **Recommended header** | "Fall Detected" |
| **Recommended body** | "A fall was detected by the resident's wearable." |
| **Clearing** | Conversation-driven. `ttl_ms` is 12 hours. |
| **Notes** | `external_partner: true` and `alert_status: 1` are set only on the first publish. A manual press of the same wearable produces the `assist` header instead (see [Other headers](#other-headers-at-priority-5-or-6)). When the fall is resolved, a `recent_fall_resolved` warning follows. |

### Emergency SOS

| Field | Value |
|---|---|
| **Event name** | `pers` |
| **Service toggle** | None checked by the producer. The `care.button_call_for_help_medical` toggle configures the call-for-help conversation type used by this alert. |
| **What it is** | An Emergency SOS message relayed by SMS from a wearable such as an Apple Watch or Samsung Watch. Intrex wearable SOS events in proprietary deployments publish the same header. Presses of button devices do not produce `pers`; they produce `assist`. |
| **Title** | "Help needed!" |
| **Comment** | "Emergency SOS received from {name}: '{text}'. Is everything alright?", plus an escalation suffix. |
| **Icon** | `exclamation-circle` |
| **Recommended header** | "Emergency Help Requested" |
| **Recommended body** | "The resident has sent an emergency SOS." |
| **Clearing** | Conversation-driven. `ttl_ms` is 12 hours. |
| **Notes** | `external_partner: true` on every phase. |

### Request Assistance

| Field | Value |
|---|---|
| **Event name** | `request_assistance` |
| **Service toggle** | None. |
| **What it is** | Help was requested through the [Request Assistance](request_assistance.md) data stream address from an app or voice UI. |
| **Title** | "Help needed!" |
| **Comment** | The text from the request, plus an escalation suffix. |
| **Icon** | `exclamation-circle` |
| **Recommended header** | "Assistance Requested" |
| **Recommended body** | "The resident has requested assistance." |
| **Clearing** | Conversation-driven. `ttl_ms` is 12 hours. |
| **Notes** | `external_partner: true` on every phase. |

### No Morning Activity

| Field | Value |
|---|---|
| **Event name** | `morning_inactivity` |
| **Service toggle** | `care.morninginactivity` |
| **What it is** | No movement has been detected in the home during the expected wake-up window. |
| **Title** | "No Morning Activity" |
| **Comment** | "Sleeping in?\nHaven't seen anyone moving this morning.", plus an escalation suffix. |
| **Icon** | `bed` |
| **Recommended header** | "No Morning Activity" |
| **Recommended body** | "No activity has been detected this morning. The resident may still be in bed." |
| **Clearing** | Conversation-driven. No `ttl_ms`. Deleted when activity resumes or the conversation ends. |

### Unusually Quiet (General Inactivity, critical phase)

| Field | Value |
|---|---|
| **Event name** | `inactivity_warning` |
| **Service toggle** | `care.generalinactivity` |
| **What it is** | Activity stopped for an extended period after the "Stretch" warning phase. Same `name` as the warning; distinguish by `priority`. |
| **Title** | "Unusually Quiet" |
| **Comment** | "Activity was detected near the '{device}' and then nowhere else in the home. Please check in.", plus an escalation suffix. |
| **Icon** | `user-times` |
| **Recommended header** | "Unusually Quiet" |
| **Recommended body** | "No movement has been detected for an extended period. Please check on the resident." |
| **Clearing** | Conversation-driven. No `ttl_ms`. |

### Bed Exit

| Field | Value |
|---|---|
| **Event name** | `sleep_bedexit_alert` |
| **Service toggle** | `care.bedexit` (with `care.bedexit.hoursstart` and `care.bedexit.hoursend`) |
| **What it is** | The resident left the bed during the configured bed-exit hours. |
| **Title** | "Bed Exit Notification" |
| **Comment** | "Someone has recently exited the bed." |
| **Icon** | `bed-empty` |
| **Recommended header** | "Bed Exit" |
| **Recommended body** | "The resident has exited the bed." |
| **Clearing** | One-shot. `resolution` button "Dismiss", action sheet "Bed Exit Notification", single option "Dismiss" with `{"answer": 0}` sent to `resolve_dashboard_header`. `ttl_ms` is 10 minutes. |
| **Notes** | Does not escalate. |

### Out of Bed Too Long

| Field | Value |
|---|---|
| **Event name** | `sleep_out_of_bed_too_long` |
| **Service toggle** | `care.outofbedtoolong` (with `care.outofbedtoolong.time` and `care.outofbedtoolong.motion`) |
| **What it is** | The resident got up during sleep hours and has not returned to bed within the configured time. |
| **Title** | "Out of Bed Too Long" |
| **Comment** | "Someone has been out of bed for an unusually long time during sleep hours." |
| **Icon** | `bed` |
| **Recommended header** | "Out of Bed Too Long" |
| **Recommended body** | "The resident has been out of bed for an unusually long time during sleep hours." |
| **Clearing** | Conversation-driven. No `ttl_ms`. Deleted when the resident returns to bed or the conversation ends. |
| **Notes** | The conversation escalates, but the header comment is not rewritten per phase. |

### Bathroom Too Long

| Field | Value |
|---|---|
| **Event name** | `bath_too_long` |
| **Service toggle** | None per location. Enabled by the organization feature flag `care.activity.bathroom`. |
| **What it is** | Someone has been in the bathroom for an unusually long time. |
| **Title** | "Check the Bathroom" |
| **Comment** | "Possible fall? Someone has been in the bathroom for {minutes} minutes and hasn't left yet.", plus an escalation suffix. |
| **Icon** | `restroom` |
| **Recommended header** | "Check the Bathroom" |
| **Recommended body** | "Someone has been in the bathroom for an unusual amount of time." |
| **Clearing** | Conversation-driven. No `ttl_ms`. |

### Wandering (RTLS)

| Field | Value |
|---|---|
| **Event name** | `RTLS` |
| **Service toggle** | `care.wanderingrtls` (with `care.wanderingrtlsdistance`) |
| **What it is** | A real-time-location-tracked wearable moved beyond the configured distance from home. |
| **Title** | "Check the {device}" on the first publish when the device is known, otherwise "Far away from home". Later phases use "Far away from home". |
| **Comment** | The supporter message from the wandering microservice, plus an escalation suffix. |
| **Icon** | `shoe-prints` |
| **Recommended header** | "Wandering Alert" |
| **Recommended body** | "The resident appears to have wandered away from their expected area." |
| **Clearing** | Conversation-driven. No `ttl_ms`. |
| **Notes** | The final "Response from the Emergency Call Center" update omits `external_partner`. |

### Poor Sleep Quality

| Field | Value |
|---|---|
| **Event name** | `sleep_score` |
| **Service toggle** | None. Requires a bedroom activity sensor. |
| **What it is** | Last night's sleep score was very low. |
| **Title** | "Poor Sleep Quality" |
| **Comment** | "Poor sleep quality last night. Please check in." or "Poor sleep quality last night, and lots of bathroom visits. Please check in." |
| **Icon** | `snooze` |
| **Recommended header** | "Poor Sleep Quality" |
| **Recommended body** | "The resident had very poor sleep quality last night." |
| **Clearing** | One-shot. Default `resolution` button "UPDATE STATUS >", option "Resolve" with `{"answer": 0}` to `resolve_dashboard_header`. `ttl_ms` runs until 3 PM local time when published before 3 PM, until 5 PM when published between 3 PM and 5 PM, and the header is deleted immediately if published after 5 PM. |
| **Notes** | Same `name` at priority 5 means "Trouble Sleeping". |

## Warning Alerts (priority 5)

### Stretch (General Inactivity, warning phase)

| Field | Value |
|---|---|
| **Event name** | `inactivity_warning` |
| **Service toggle** | `care.generalinactivity` |
| **What it is** | No movement for a while. The first phase of general inactivity. |
| **Title** | "Stretch" |
| **Comment** | "Haven't detected any movement lately!\nTime to stand up and stretch." |
| **Icon** | `running` |
| **Recommended header** | "Time to Stretch" |
| **Recommended body** | "No movement has been detected lately." |
| **Clearing** | Conversation-driven. Escalates in place to priority 6 "Unusually Quiet" if inactivity continues. |

### Didn't Return Home

| Field | Value |
|---|---|
| **Event name** | `not_back_home` |
| **Service toggle** | `care.notbackhome` (with `care.notbackhometuning`) |
| **What it is** | The resident left home and has not returned within the expected time. |
| **Title** | "Perimeter: Didn't Return Home" |
| **Comment** | "I miss you." When supporters are contacted the comment is replaced with "Alerted family and friends." |
| **Icon** | `map-marker-question` |
| **Recommended header** | "Didn't Return Home" |
| **Recommended body** | "The resident left home and has not returned within the expected time." |
| **Clearing** | Conversation-driven. `ttl_ms` is 12 hours. |
| **Notes** | Stays at priority 5. The code path meant to raise it to priority 6 when the Emergency Call Center is contacted references an undefined constant and does not publish. |

### It's Bedtime

| Field | Value |
|---|---|
| **Event name** | `bedtime` |
| **Service toggle** | `care.latenight` |
| **What it is** | The resident appears to be up unusually late. |
| **Title** | "It's Bedtime" |
| **Comment** | "It appears you are up very late tonight.\nEverything okay?" When supporters are contacted, "\n\nAlerted family and friends." is appended. |
| **Icon** | `bed` |
| **Recommended header** | "Up Late" |
| **Recommended body** | "The resident appears to be up unusually late tonight." |
| **Clearing** | Conversation-driven. `ttl_ms` is 12 hours. |

### Out of Bedroom Activity

| Field | Value |
|---|---|
| **Event name** | `out_of_bedroom` |
| **Service toggle** | `care.outofbedroom` |
| **What it is** | Motion outside the bedroom or bathroom late at night. |
| **Title** | "Out of Bedroom Activity" |
| **Comment** | "Someone is outside of the bedroom or bathroom late at night." |
| **Icon** | `moon` |
| **Recommended header** | "Out of Bedroom" |
| **Recommended body** | "Activity detected outside the bedroom late at night." |
| **Clearing** | One-shot. `resolution` button "RESOLVE >", action sheet "Update Status", option "Resolved" with `{"answer": 0}` to `resolve_dashboard_header`. `ttl_ms` is 30 minutes. |

### Pacing Detected

| Field | Value |
|---|---|
| **Event name** | `pacing` |
| **Service toggle** | `care.pacing` (with `care.pacing.time`) |
| **What it is** | Sustained movement while the resident is alone, which may indicate agitation. |
| **Title** | "Pacing Detected" |
| **Comment** | "Sustained movement detected while the resident is alone." |
| **Icon** | `walking` |
| **Recommended header** | "Pacing Detected" |
| **Recommended body** | "Sustained repetitive movement detected while the resident is alone." |
| **Clearing** | Auto-clears when the pacing stops. No `resolution`, no `ttl_ms`. |

### Trouble Sleeping

| Field | Value |
|---|---|
| **Event name** | `sleep_score` |
| **Service toggle** | None. Requires a bedroom activity sensor. |
| **What it is** | Last night's sleep score was below normal but not severe. |
| **Title** | "Trouble Sleeping" |
| **Comment** | "Occupants appeared to have trouble sleeping last night. Please check in." or "Trouble sleeping last night, and lots of bathroom visits. Please check in." |
| **Icon** | `snooze` |
| **Recommended header** | "Trouble Sleeping" |
| **Recommended body** | "The resident had difficulty sleeping last night." |
| **Clearing** | Same one-shot resolution and 3 PM / 5 PM `ttl_ms` rule as Poor Sleep Quality. |

### Recent Fall Resolved

| Field | Value |
|---|---|
| **Event name** | `recent_fall_resolved` |
| **Service toggle** | None. Follows any radar or wearable fall. |
| **What it is** | Informational follow-up after a fall alert is resolved. Location-wide, so it counts falls from every device in the last 24 hours. |
| **Title** | "Recent Fall, it has been resolved" for one fall, "Multiple Recent Falls, all is okay now" for more than one. |
| **Comment** | Radar: "A fall occurred at {time} on {m/d} in the {device}. The resident {status}." Wearable: "A fall occurred at {time} on {m/d} in the {device}." Multiple falls: "{n} falls have occurred in the last 24 hours, most recently at {time} on {m/d} in the {device}. All is okay now[, the resident {status}]." |
| **Icon** | `exclamation-triangle` |
| **Recommended header** | "Recent Fall Resolved" |
| **Recommended body** | "A recent fall alert has been resolved." |
| **Clearing** | One-shot. Default `resolution` button "UPDATE STATUS >", option "Resolve" with `{"answer": 0}` to `resolve_dashboard_header`, acknowledgment "Clear". `ttl_ms` is 24 hours. |

### Sedentary (Prolonged Sitting)

| Field | Value |
|---|---|
| **Event name** | `sedentary_{unique_id}`, where the suffix is the radar subregion ID. Prefix-match on `sedentary_`. |
| **Service toggle** | `care.sedentary` (with `care.sedentary.threshold`, `care.sedentary.hoursstart`, `care.sedentary.hoursend`) |
| **What it is** | The resident has been sitting in a tracked chair or couch zone longer than the configured threshold. Multiple chairs alert independently. |
| **Title** | "Sedentary" |
| **Comment** | "Has been sitting in '{zone}' since {time}." |
| **Icon** | `loveseat` |
| **Recommended header** | "Sedentary" |
| **Recommended body** | "Has been sitting in '{zone}' since {time}." |
| **Clearing** | One-shot. `resolution` button "Dismiss", action sheet "Sedentary Alert", option "Dismiss" with `{"answer": 0}` to `resolve_dashboard_header`. `ttl_ms` is 45 minutes. Also deleted when the resident leaves the chair, the home becomes absent or asleep, or the service is disabled. |
| **Notes** | `external_partner` is never set on this header. Route on `name`. |

## Conversation Escalation

Conversation-driven alerts keep the same `name` and `title` while the conversation progresses and rewrite `comment` at each phase. The phases come from the conversation engine:

| Phase | Meaning |
|---|---|
| Conversation started | Alert fires. The header is first published here. |
| To residents | People who live in the home are being messaged. |
| To supporters | Family and friends are being messaged. |
| ECC soon | The Emergency Call Center will be contacted shortly. |
| To ECC | The Emergency Call Center is being contacted. `ecc` becomes `false`. |
| ECC dispatch | The Emergency Call Center has been authorized to dispatch. |
| ECC response | The Emergency Call Center replied with a message. |
| Resolved, timed out, or false alarm | The header is deleted. |

Not every alert publishes on every phase, and the suffix text is owned by each microservice rather than shared. `{service}` below is the deployment's service name (the `SERVICE_NAME` bot property). Each suffix is appended after `"\n\n"` unless noted.

| Alert | To residents | To supporters | ECC soon | To ECC | ECC dispatch | ECC response |
|---|---|---|---|---|---|---|
| `radar_fall*` | "{service} has alerted family and friends." | "{service} has alerted people who live here." | | "{service} has alerted the Emergency Call Center." | | |
| `positional_fall_*` | "{service} has alerted people who live here." | "{service} has alerted family and friends." | | "{service} has alerted the Emergency Call Center." | | |
| `pers` | "{service} has alerted people who live here." | "{service} has alerted family and friends." | | "{service} has alerted the Emergency Call Center." | | |
| `request_assistance` | "{service} has alerted people who live here." | "{service} has alerted everyone in the Trusted Circle." | | "{service} has alerted the Emergency Call Center." | | |
| `morning_inactivity` | "Alerted people who live here." | "Alerted family and friends." | "Will alert the Emergency Call Center soon." | "Alerted the Emergency Call Center." | "The Emergency Call Center has been authorized to dispatch." | "Emergency Call Center responded: {text}." |
| `inactivity_warning` | (priority 5 "Stretch" header) | "The Emergency Call Center will be alerted soon.\nUpdate status to resolve." (priority 6) | same as To supporters | "Alerted the Emergency Call Center." | "The Emergency Call Center has been authorized to dispatch." | "The Emergency Call Center has responded: {text}." |
| `bath_too_long` | | "Alerted family and friends." | "Will alert the Emergency Call Center soon." | "Alerted the Emergency Call Center." | "Emergency Call Center is authorized to dispatch." | "Response from the Emergency Call Center: {text}" |
| `RTLS` | | "Alerted family and friends." | "Will alert the Emergency Call Center soon." | "Alerted the Emergency Call Center." | "Emergency Call Center is authorized to dispatch." | "Response from the Emergency Call Center: {text}" |
| `bedtime` | | "Alerted family and friends." | | | | |
| `not_back_home` | | comment replaced by "Alerted family and friends." | | | | |
| `sleep_out_of_bed_too_long` | | | | | | |

The radar fall microservice appends the "family and friends" text on the residents phase and the "people who live here" text on the supporters phase. This is how the code reads today; do not infer the phase from the suffix text for radar falls.

### Example: Morning Inactivity

Conversation started:

```json
{
  "name": "morning_inactivity",
  "priority": 6,
  "title": "No Morning Activity",
  "comment": "Sleeping in?\nHaven't seen anyone moving this morning.",
  "icon": "bed",
  "icon_font": "far",
  "external_partner": true,
  "call": true,
  "ecc": true,
  "updated_ms": 1714200000000,
  "resolution": { "...": "..." }
}
```

Supporters contacted:

```json
{
  "name": "morning_inactivity",
  "priority": 6,
  "title": "No Morning Activity",
  "comment": "Sleeping in?\nHaven't seen anyone moving this morning.\n\nAlerted family and friends.",
  "icon": "bed",
  "icon_font": "far",
  "external_partner": true,
  "call": true,
  "ecc": true,
  "updated_ms": 1714201200000,
  "resolution": { "...": "..." }
}
```

Emergency Call Center contacted:

```json
{
  "name": "morning_inactivity",
  "priority": 6,
  "title": "No Morning Activity",
  "comment": "Sleeping in?\nHaven't seen anyone moving this morning.\n\nAlerted the Emergency Call Center.",
  "icon": "bed",
  "icon_font": "far",
  "external_partner": true,
  "call": true,
  "ecc": false,
  "updated_ms": 1714202400000,
  "resolution": { "...": "..." }
}
```

`ecc` is `true` only while the location has professional monitoring and the Emergency Call Center has not yet been contacted.

## Severity Mapping

| Priority | Level | Meaning | Suggested color |
|---|---|---|---|
| `6` | Critical | Immediate attention: falls, SOS, prolonged inactivity, bed exit. | Red |
| `5` | Warning | Advisory: worth a look, not necessarily an emergency. | Orange or yellow |

Priorities 0 to 4 are status and system information. The full table is in [Dashboard Header](dashboard_header.md#priority).

## Other headers at priority 5 or 6

These headers also reach priority 5 or 6 but are not flagged with `external_partner`. They are listed so your application can recognize them if it renders on `priority` alone. Names in `{braces}` are substituted at runtime.

| Event name | Priority | Title | Source | Clearing |
|---|---|---|---|---|
| `assist` | 6 | "Assist Button Pressed" (or "{device} Pressed" for the Develco audio assistant) | Button presses on Intrex, Comarch, Becklar, Develco, LinkHigh buttons; `rules/device_button*_microservice.py` | Conversation, `ttl_ms` 12 hours |
| `health` | 6 | "Help needed!" | Apple Health movement or heart-rate conversation; `health/location_health_microservice.py` | Conversation, `ttl_ms` 12 hours |
| `water_leak` | 6 | "Water Leak" | `rules/device_leak_rules_intelligence.py`, `care_control/device_leak_rules_intelligence.py` | Conversation |
| `alarm` | 5 or 6 | Arming states, "Alarm Triggered", "Security Alarm", "Alarm Activated!" | `prosecurity/location_security_intelligence.py`, `rules/location_alarm_microservice.py` | Conversation or custom resolution |
| `keypad` | 6 | "SOS" | `rules/location_keypad_microservice.py` | Conversation |
| `wiredsecurity` | 6 | "Wired Security Alarm" | `rules/device_iorules_microservice.py` | Conversation, `ttl_ms` 30 minutes |
| `offline_{device_id}` | 6 | "Offline" | `rules/device_gateway_microservice.py` | Deleted by the gateway microservice when the condition clears |
| `battery_{device_id}` | 6 (4 while merely on battery) | "Critically low battery", "Battery Depleted" | `rules/device_gateway_microservice.py` | Deleted by the gateway microservice when the condition clears |
| `{device_id}` | 6 | "Mold and Mildew!", "Mold and Mildew Warning" | `rules/device_environmental_rules_intelligence.py` | One-shot, `ttl_ms` 1 hour |
| `{device_id}` | 5 | "Refrigerator Warning", "Freezer Warning", "Medicine Warning" | `rules/device_environmental_rules_intelligence.py` | One-shot, `ttl_ms` 12 hours or 30 minutes |
| `{device_id}` | 6 | "Oven Warning" | `rules/device_smartbreaker_microservice.py` | Custom resolution to `oven_circuitbreaker` |
| `{subregion_id}` | 5 | "Did someone get out of bed recently?" and similar yes/no feedback questions | `radar/device_radartrends_microservice.py` | One-shot, `ttl_ms` 15 minutes |
| `vayyar` | 6 | "Help needed!" | Legacy Vayyar fall path; `radar/location_radarvayyar_microservice.py` | Conversation, `ttl_ms` 12 hours |
| `audio_assistant` | 6 during a call | "Audio Assistant Call" | `rules/device_develco_audio_assistant_proxy_microservice.py` | `ttl_ms` 5 minutes |
| `assessment_status` | 5 | "Fall Risk Elevated" | `assessment/location_assessment_microservice.py` | One-shot |
| `health_reminder` | 5 | "We're missing some information!" | `health/location_health_reminder_microservice.py` | Conversation |
| `occupancy_away` | 5 | "Left home?" | `occupancy/away/location_away_microservice.py` | Conversation |
| `reminder_to_arm` | 5 | "Remember to Arm" | `occupancy_to_reminder/location_occupancy_reminder_microservice.py` | Custom resolution |
| `dr_out_of_bounds`, `demand_response` | 6, 5 | "Energy Savings Paused", "Energy Savings Active" | Demand response microservices | One-shot, `ttl_ms` 6 hours |

Proprietary deployments may add `pers` from the Intrex wearable (with `external_partner: true`), `etectrx` ("Check the brief", priority 6), `grip_able_fall_risk_{device_id}` (priority 5), and `glass_breaking` (priority 6).

Headers that do not exist despite similar features: the Kallos band wandering microservice, radar stability events, and Intrex position tracking publish no priority 5 or 6 header. Device offline conditions publish `offline_{device_id}` above and a priority 4 `location.offline` header.

## Event Name Quick Reference

| Event name | Alert | Priority | Escalates | `external_partner` | Clears |
|---|---|---|---|---|---|
| `radar_fall_*` | Fall Detected (radar) | 6 | Yes | First publish only | Conversation, TTL 12 h |
| `positional_fall_*` | Fall Detected (wearable) | 6 | Yes | First publish only | Conversation, TTL 12 h |
| `pers` | Emergency SOS | 6 | Yes | Yes | Conversation, TTL 12 h |
| `request_assistance` | Assistance Requested | 6 | Yes | Yes | Conversation, TTL 12 h |
| `morning_inactivity` | No Morning Activity | 6 | Yes | Yes | Conversation |
| `inactivity_warning` | Stretch / Unusually Quiet | 5 then 6 | Yes | Yes | Conversation |
| `sleep_bedexit_alert` | Bed Exit | 6 | No | Yes | Dismiss, TTL 10 min |
| `sleep_out_of_bed_too_long` | Out of Bed Too Long | 6 | Conversation only | Yes | Conversation |
| `bath_too_long` | Check the Bathroom | 6 | Yes | Yes | Conversation |
| `RTLS` | Wandering | 6 | Yes | Yes, except final ECC response | Conversation |
| `sleep_score` | Poor Sleep Quality / Trouble Sleeping | 6 or 5 | No | Yes | Resolve, TTL to 3 PM or 5 PM |
| `not_back_home` | Didn't Return Home | 5 | Yes | Yes | Conversation, TTL 12 h |
| `bedtime` | It's Bedtime | 5 | Yes | Yes | Conversation, TTL 12 h |
| `out_of_bedroom` | Out of Bedroom Activity | 5 | No | Yes | Resolve, TTL 30 min |
| `pacing` | Pacing Detected | 5 | No | Yes | When pacing stops |
| `recent_fall_resolved` | Recent Fall Resolved | 5 | No | Yes | Resolve, TTL 24 h |
| `sedentary_*` | Sedentary | 5 | No | No | Dismiss, TTL 45 min, or leaves chair |

## References

All paths are under `com.ppc.Microservices/intelligence/` in botlab-core unless noted.

* `com.ppc.Bot/signals/dashboard.py` (the `update_dashboard_header` signal, `oneshot_resolution_object`, priority constants)
* `com.ppc.BotProprietary/signals/services.py` (service toggle keys)
* `com.ppc.BotProprietary/signals/conversation_callback.py` (escalation phase constants)
* `dashboard/location_dashboardheader_microservice.py` (prioritization, `resolve_dashboard_header`, field stripping)
* `conversations/types/conversation_type.py` (default `resolution` and `feedback` objects)
* `conversations/location_conversation_microservice.py` (`conversation_resolved`, `conversation_feedback`, `contact_ecc`)
* `radar/location_radar_microservice.py` (`radar_fall*`, `recent_fall_resolved`)
* `rules/device_positional_fall_microservice.py` (`positional_fall_*`, `recent_fall_resolved`)
* `care/pers/location_sos_microservice.py` (`pers`)
* `care/pers/location_requestassistance_microservice.py` (`request_assistance`)
* `care/inactivity/location_morning_inactivity_microservice.py` (`morning_inactivity`)
* `care/inactivity/location_general_inactivity_microservice.py` (`inactivity_warning`)
* `care/inactivity/location_notbackhome_microservice.py` (`not_back_home`)
* `care/inactivity/location_bedtime_microservice.py` (`bedtime`)
* `care/inactivity/location_sleep_outofbedtoolong_microservice.py` (`sleep_out_of_bed_too_long`)
* `care/activity/location_sleep_bedexit_microservice.py` (`sleep_bedexit_alert`)
* `care/activity/location_sleep_outofbedroom_microservice.py` (`out_of_bedroom`)
* `care/activity/location_bathroom_too_long_microservice.py` (`bath_too_long`)
* `care/activity/location_pacing_microservice.py` (`pacing`)
* `care/activity/location_sleep_quantification_microservice.py` (`sleep_score`)
* `care/sedentary/location_sedentary_microservice.py` (`sedentary_*`)
* `care/wandering/location_wandering_rtls_microservice.py` (`RTLS`)
* `com.ppc.Bot/devices/radar/` and `com.ppc.Bot/devices/button/` (device type IDs)
* botlab-private: `intrex_dev/location_intrex_microservice.py`, `etectrx/location_etectrx_microservice.py`, `grip_able/location_grip_able_microservice.py`, `ip_camera_events/location_ip_camera_events_microservice.py`
