# Synthetic API: Action Plans

When a problem occurs, an action plan oversees the resolution of the problem. This Synthetic API helps mobile apps communicate to users about how various problems are resolved. While the real action plans are much more detailed and complex, the objective here is to keep the content consumable by regular users.

| Property    | Type | Description |
| ----------- | ---- | ----------- |
| `action_plans` | Dictionary | Dictionary of action plans. The key in each entry is the name of the unique identifier for service related to this action plan. |
| `group_1` | List of Dictionary user objects | List of people who would get contacted first. In some apps, this is the list of people who are marked "I live here". |
| `group_2` | List of Dictionary user objects | List of people who would get contacted second. In some apps, this is the list of people who are marked "Family / Friend". |
| `push_only` | Boolean | True if this alert will prefer a push notification only. Note that alerts will still fail-over to SMS if they cannot be delivered via push. Currently always False. |
| `contact_group_1` | Boolean | True if group 1 will be contacted for this alert. |
| `contact_group_2` | Boolean | True if group 2 could be contacted for this alert. |
| `group_2_delay_ms` | Integer | Milliseconds delay between contacting group 1 and then escalating to group 2 if the alert is not resolved. You would normally turn this into minutes or hours to communicate the value to users. |
| `allow_ecc` | Boolean | True if this alert could escalate to the Emergency Call Center *without dispatch*. This is `ecc_eligible` combined with the user's professional monitoring subscription, registration, and Emergency Call Center service being on. `allow_dispatch` can only be True when `allow_ecc` is True. |
| `ecc_delay_ms` | Integer | Milliseconds delay between contacting group 2 and then escalating to the Emergency Call Center. |
| `allow_dispatch` | Boolean | True if this alert could trigger a dispatch from emergency services. This is `dispatch_eligible` combined with `allow_ecc` and the user's dispatch service being on. |
| `dispatch_delay_ms` | Integer | Milliseconds delay between contacting the Emergency Call Center without dispatch, and then contacting the Emergency Call Center again with authorization to dispatch. Currently exported with the same value as `ecc_delay_ms`. |
| `ecc_eligible` | Boolean | True if this action plan is eligible for escalation to the Emergency Call Center, regardless of whether the user is subscribed or has their Emergency Call Center turned on or off. |
| `dispatch_eligible` | Boolean | True if this action plan is eligible for emergency dispatch, regardless of whether the user is subscribed or has their Emergency Call Center turned on or off. |

## Output

State Variable : `action_plans`

The `action_plans` dictionary currently contains an entry for each of these service keys: `care.button.supernova`, `care.button.supernova_not_dispatch`, `care.button.medical`, `care.button.help_from_anyone`, `care.button.help_from_occupants`, `care.generalinactivity`, `care.notbackhome`, `care.bathroomactivity`, `care.latenight`, `care.midnightsnack`, `care.wandering`, `care.radar`, `care.radar_stability`, `care.apple`, and `care.outofbedtoolong`. Every entry also includes `ecc_eligible` and `dispatch_eligible`, which are not shown in the example below.

#### Example

```
{
  "value": {
    "action_plans": {
      "care.bathroomactivity": {
        "allow_dispatch": true,
        "allow_ecc": true,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 3600000,
        "ecc_delay_ms": 600000,
        "group_2_delay_ms": 300000,
        "push_only": false
      },
      "care.button.help_from_anyone": {
        "allow_dispatch": false,
        "allow_ecc": false,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 7200000,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 0,
        "push_only": false
      },
      "care.button.help_from_occupants": {
        "allow_dispatch": false,
        "allow_ecc": false,
        "contact_group_1": true,
        "contact_group_2": false,
        "dispatch_delay_ms": 7200000,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 0,
        "push_only": false
      },
      "care.button.medical": {
        "allow_dispatch": true,
        "allow_ecc": true,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 900000,
        "ecc_delay_ms": 120000,
        "group_2_delay_ms": 0,
        "push_only": false
      },
      "care.button.supernova": {
        "allow_dispatch": true,
        "allow_ecc": true,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 900000,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 0,
        "push_only": false
      },
      "care.generalinactivity": {
        "allow_dispatch": true,
        "allow_ecc": true,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 7200000,
        "ecc_delay_ms": 600000,
        "group_2_delay_ms": 600000,
        "push_only": false
      },
      "care.latenight": {
        "allow_dispatch": false,
        "allow_ecc": false,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 7200000,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 900000,
        "push_only": false
      },
      "care.midnightsnack": {
        "allow_dispatch": false,
        "allow_ecc": false,
        "contact_group_1": true,
        "contact_group_2": false,
        "dispatch_delay_ms": 0,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 0,
        "push_only": true
      },
      "care.notbackhome": {
        "allow_dispatch": false,
        "allow_ecc": true,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 7200000,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 600000,
        "push_only": false
      },
      "care.radar": {
        "allow_dispatch": true,
        "allow_ecc": true,
        "contact_group_1": true,
        "contact_group_2": true,
        "dispatch_delay_ms": 900000,
        "ecc_delay_ms": 120000,
        "group_2_delay_ms": 0,
        "push_only": false
      },
      "care.wandering": {
        "allow_dispatch": false,
        "allow_ecc": false,
        "contact_group_1": true,
        "contact_group_2": false,
        "dispatch_delay_ms": 0,
        "ecc_delay_ms": 0,
        "group_2_delay_ms": 0,
        "push_only": true
      }
    },
    "group_1": [
      {
        "email": {
          "status": 0,
          "verified": true
        },
        "firstName": "Mick",
        "id": 12345,
        "lastName": "Jagger",
        "locationAccess": 30,
        "phoneType": 1,
        "smsPhone": "123456789",
        "smsStatus": 1,
        "temporary": false
      }
    ],
    "group_2": [
      {
        "email": {
          "status": 0,
          "verified": false
        },
        "firstName": "Aretha",
        "id": 35,
        "language": "en",
        "lastName": "Franklin",
        "locationAccess": 30,
        "phoneType": 1,
        "smsPhone": "123456789",
        "smsStatus": 0,
        "temporary": false
      },
      {
        "email": {
          "status": 0,
          "verified": false
        },
        "firstName": "Daryl",
        "id": 12345,
        "language": "en",
        "lastName": "Hall",
        "locationAccess": 30,
        "phoneType": 1,
        "smsPhone": "123456789",
        "smsStatus": 1,
        "temporary": false
      }
    ]
  }
}
```
