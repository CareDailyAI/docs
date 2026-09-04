# Synthetic API: Insights

Insights provide situational awareness and current predictions taking place in the home. The content captured in insights is intended to enable mobile applications to dynamically render useful information.

Insights are captured in a JSON dictionary structure where the key is a unique (predictable) **Insight ID**, and the JSON object underneath includes the value, a developer-readable description, an optional device ID, and the timestamp of the last update in milliseconds.

Insights are captured internally by bot microservices through `com.ppc.Bot/signals/insights.py` (`capture_insight()` / `delete_insight()`) and stored by `com.ppc.Microservices/intelligence/insights/location_insights_microservice.py`. An insight is deleted from the `insights` state variable when it is captured again with a `null` value.

#### Standardized Insights

Insights are based on available data and not guaranteed to exist in the `insights` state variable.

| Insight ID              | Value Type | Description | 
| ----------------------- | ---------- | ----------- |
| `ambient_temperature_c` | float      | The ambient temperature in Celsius. The fastest update interval is once every 5 minutes. Motion sensors with temperature sensing capabilities will update this value based on where occupants were last observed. If no motion is detected recently, the value will fall back to a reading from a connected thermostat, if available. |
| `ambient_temperature.zscore` | float | Z-score of ambient temperature based on the previous 15-day hourly history. Appears only when the home is unusually warm or unusually cold. |
| `sleep.wake_prediction_ms` | int | Predicted wake-up time in unix epoch milliseconds. Could be in the past if occupants have not woken up yet. |
| `sleep.sleep_prediction_ms` | int | Predicted go-to-sleep time in unix epoch milliseconds. Could be in the past if occupants have not gone to sleep yet. | 
| `bathroom_visits.high` | int | Abnormally high number of bathroom visits today. The value is the total number of visits. |
| `bathroom_visits.low` | int | Abnormally low number of bathroom visits today. The value is the total number of visits. |
| `care.inactivity.time_to_stretch` | True | Appears when occupants have been inactive for a long time during the day and it is time to get up and stretch. The `device_id` references the sensor where activity was last observed. |
| `care.inactivity.warning` | True | Appears when inactivity has continued long enough to become an inactivity alert. Replaces `care.inactivity.time_to_stretch`. The `device_id` references the sensor where activity was last observed. |
| `care.inactivity.good_morning_sleeping_in` | True | Appears when occupants are usually awake by now and movement near a bed sensor indicates someone may be sleeping in. |
| `care.inactivity.good_morning_problem_critical` | True | Appears when occupants are usually awake by now and no morning activity has been detected. |
| `care.inactivity.good_morning_problem_critical_bed_only` | True | Appears when occupants are usually awake by now and are still in bed. |
| `care.inactivity.bedtime_awake_too_late` | True | Appears when occupants are still up late relative to their usual bedtime. |
| `care.inactivity.not_back_home.warning` | True | Appears when someone was expected to be back home and has not returned. |
| `care.activity.bathroom_no_activity_detected` | True | Appears when someone has been in the bathroom too long. |
| `care.activity.bathroom_activity_detected` | True | Incontinence warning: a brief sensor detected wetness. |
| `care.activity.sleep.out_of_bedroom.morning_summary` | True | Morning summary of out-of-bedroom activity overnight. The `description` contains the summary. |
| `care.activity.wandering_far_away` | True | Appears when a tracked wearable is far away from home. |
| `care.sms_sos` | True | Emergency SOS received over SMS. The `description` contains the message text. |
| `request_assistance` | int | Assistance was requested from the mobile app or smart speaker. The value is the request type: 0 = emergency, direct to call center; 1 = standard emergency; 2 = request assistance from occupants; 3 = request assistance from anyone. |
| `rules.buttonpanic.alert` | True | A button with a panic / call-for-help behavior was pressed. |
| `rules.buttononeshot.alert` | True | A one-shot button was pressed to call for help. |
| `rules.buttonmulti.alert` | True | A multi-button was pressed to call for help. |
| `rules.buttonmobile.alert` | True | A mobile button was pressed to call for help. |
| `rules.audio_assistant.alert` | True | An audio assistant was used to call for help. |
| `rules.leak.{device_id}` | True | The leak detector with this device ID detected a water leak. |
| `radar.fall_confirmed_alert` | True | A radar device confirmed a fall. |
| `vayyar.stability_event_confirmed_alert` | True | A Vayyar radar device confirmed a stability event. |
| `health_high_heart_rate_warning` | True | A health device detected a higher than normal heart rate. |
| `health_movement_confirmed_alert` | True | A health device detected movement. |
| `onscreen.pain_level_increasing` | float | Pain level appears to be increasing based on AI Assessment results. The value is the current trend value. |
| `onscreen.pain_level_declining` | float | Pain level appears to be declining based on AI Assessment results. The value is the current trend value. |
| `onscreen.happiness_level_increasing` | float | Happiness level appears to be increasing based on AI Assessment results. The value is the current trend value. |
| `onscreen.happiness_level_declining` | float | Happiness level appears to be declining based on AI Assessment results. The value is the current trend value. |
| `device.blindspot.{device_id}` | True | Appears when there is a blind spot identified near a sensor with this device ID. Indicates a missing entry or motion sensor nearby. |
| `device.alwaysopen.{device_id}` | True | Appears when the entry sensor with this device ID appears to be always open, and therefore broken (magnet fell off, door is always open, etc.). |
| `device.name_behavior_mismatched.{device_id}` | True | Appears when the descriptive name of the device does not match the behavior selected for that device. For example, an entry sensor with a behavior for a perimeter door named 'Medicine Cabinet'. |
| `device.wall_powered.{device_id}` | True | Appears when the gateway is on wall power. |
| `device.battery_powered.{device_id}` | True | Appears when the gateway with the given device ID is being powered by battery. |
| `device.cellular.{device_id}` | True | Appears when the gateway with the given device ID is connected to cellular. |
| `device.broadband.{device_id}` | True | Appears when the gateway with the given device ID is connected to broadband internet (WiFi/Ethernet). |
| `device.offline.{device_id}` | True | The device with the given ID is offline. |
| `device.low_battery.{device_id}` | int | This device has a low battery. The value is the current battery level from 0-100%. |
| `device.low_signal.{device_id}` | float | This device appears to have a low wireless signal strength. The value is the average RSSI (receive signal strength indicator). |
| `device.fall.{device_id}` | True | The device with the given ID detected a positional fall. |
| `device.far_away.{device_id}` | float | The tracked device with the given ID is far away from home. The value is the distance from home. |
| `device.reboot_toomany.{device_id}` | int | The device with the given ID has rebooted too many times. The value is the reboot count. |
| `occupancy.return_ms` | int | Approximate time in unix epoch ms occupants are expected to return. This could be in the past if occupants were expected home earlier. | 

#### Legacy Insights

The following insight IDs were produced by earlier versions of the bots and may still appear in older `insights` state variables. The current sleep quantification microservice (`com.ppc.Microservices/intelligence/care/activity/location_sleep_quantification_microservice.py`) only deletes them, and no microservice in `botlab-core` or `botlab-private` currently captures `security_mode`, `occupancy.status`, or `occupancy.last_seen`. Apps should not depend on them.

`sleep.duration_ms`, `sleep.sleep_score`, `sleep.cycle_score`, `sleep.bedtime_score`, `sleep.wakeup_score`, `sleep.restlessness_score`, `sleep.bedtime_ms`, `sleep.wakeup_ms`, `sleep.overslept`, `sleep.underslept`, `sleep.low_sleep_quality.warning`, `sleep.too_many_bathrooms.warning`

## Output

State Variable : `insights`

#### Insight Properties

| Property    | Description |
| ----------- | ----------- |
| value | The current value of this insight. |
| title | Human-readable title recommended for end-users. |
| description | Human-readable description for end-users. |
| icon | Optional recommended icon name, may be None / Null |
| icon_font | Optional icon font package, for example `far` means 'FontAwesome Regular', may be None / Null. |
| device_id | Optional field used to capture the device ID string of the device producing this insight, if applicable. |
| device_desc | Optional field used to capture the nickname of the device producing this insight, if applicable. |
| device_type | Optional field used to capture the device type, if applicable. |
| confidence_state | Optional confidence state associated with this insight, if the producing microservice supplied one. |
| confidence_reason | Optional human-readable reason for the confidence state. Only present when `confidence_state` is present. |
| updated_ms | Timestamp of the last update to this insight, in unix epoch milliseconds. Can be used to render display information like "5 minutes ago", or simply see if this insight was updated. |

#### Insight JSON Content Example

```
{
  "device.low_battery.00155F00F861FCF5-03B7": {
    "description": "'Garage Back Door' has a low battery.",
    "device_desc": "Garage Back Door",
    "device_id": "00155F00F861FCF5-03B7",
    "device_type": 9114,
    "icon": "battery-empty",
    "icon_font": "far",
    "title": "Low battery",
    "updated_ms": 1630956432881,
    "value": 1
  },
  "device.low_battery.FFFFFFFF006b34e8": {
    "description": "'Front Door' has a low battery.",
    "device_desc": "Front Door",
    "device_id": "FFFFFFFF006b34e8",
    "device_type": 9114,
    "icon": "battery-empty",
    "icon_font": "far",
    "title": "Low battery",
    "updated_ms": 1630627884736,
    "value": 10
  },
  "device.low_signal.94f3b202008d1500": {
    "description": "Low wireless signal strength on 'TV'.",
    "device_desc": "TV",
    "device_id": "94f3b202008d1500",
    "device_type": 9135,
    "icon": null,
    "icon_font": null,
    "title": "Low signal strength",
    "updated_ms": 1632351525676,
    "value": -89
  },
  "device.offline.00155F0074838333-0375": {
    "description": "Device 'Bathroom' is offline.",
    "device_desc": "Bathroom",
    "device_id": "00155F0074838333-0375",
    "device_type": 9138,
    "icon": "unlink",
    "icon_font": "far",
    "title": "Device Offline",
    "updated_ms": 1629964522663,
    "value": true
  },
  "device.offline.020000013000042E": {
    "description": "'Smart Home Center Develco' is disconnected",
    "device_desc": "Smart Home Center Develco",
    "device_id": "020000013000042E",
    "device_type": 36,
    "icon": "unlink",
    "icon_font": "far",
    "title": "Disconnected",
    "updated_ms": 1632749668747,
    "value": true
  },
  "device.wall_powered.020000013000042E": {
    "description": "'Smart Home Center Develco' is on wall power",
    "device_desc": "Smart Home Center Develco",
    "device_id": "020000013000042E",
    "device_type": 36,
    "icon": "battery-bolt",
    "icon_font": "far",
    "title": "Wall Powered",
    "updated_ms": 1630020688468,
    "value": true
  },
  "occupancy.last_seen": {
    "description": "Last seen closing the 'Front Door'.",
    "device_desc": "Front Door",
    "device_id": "FFFFFFFF006b34e8",
    "device_type": 9114,
    "icon": null,
    "icon_font": null,
    "title": "Last seen",
    "updated_ms": 1633445856657,
    "value": 0
  },
  "occupancy.return_ms": {
    "description": "Occupants are predicted to return around 8:42 PM on Monday.",
    "icon": "house-return",
    "icon_font": "far",
    "title": "Expected home later",
    "updated_ms": 1633405346951,
    "value": 1633432002178.5
  },
  "occupancy.status": {
    "description": "Appears to be away for a long time.",
    "icon": null,
    "icon_font": null,
    "title": "Vacation",
    "updated_ms": 1633527002299,
    "value": "VACATION"
  },
  "security_mode": {
    "description": "Security system is armed.",
    "icon": null,
    "icon_font": null,
    "title": "Armed",
    "updated_ms": 1633446324363,
    "value": "AWAY"
  },
  "sleep.bedtime_ms": {
    "description": "Appears to have gone to sleep around 11:31 PM on Monday.",
    "icon": null,
    "icon_font": null,
    "title": "Likely asleep",
    "updated_ms": 1633415519404,
    "value": 1633415519404
  },
  "sleep.bedtime_score": {
    "description": "15% bedtime consistency score.",
    "icon": null,
    "icon_font": null,
    "title": "Bedtime consistency",
    "updated_ms": 1633443242664,
    "value": 15.0
  },
  "sleep.duration_ms": {
    "description": "7.7 hours of sleep.",
    "icon": "alarm-clock",
    "icon_font": "far",
    "title": "Sleep Duration",
    "updated_ms": 1633443242664,
    "value": 27723260
  },
  "sleep.restlessness_score": {
    "description": "23% restlessness score while sleeping.",
    "icon": null,
    "icon_font": null,
    "title": "Restlessness",
    "updated_ms": 1633443242664,
    "value": 23.0
  },
  "sleep.sleep_prediction_ms": {
    "description": "Expected to go to sleep tonight around 11:24 PM.",
    "icon": "bed",
    "icon_font": "far",
    "title": "Predicted Bedtime",
    "updated_ms": 1633550600399,
    "value": 1633587840000
  },
  "sleep.sleep_score": {
    "description": "46% sleep score.",
    "icon": null,
    "icon_font": null,
    "title": "Sleep score",
    "updated_ms": 1633443242664,
    "value": 46.0
  },
  "sleep.wakeup_ms": {
    "description": "Woke up around 7:14 AM on Tuesday.",
    "icon": null,
    "icon_font": null,
    "title": "Good morning",
    "updated_ms": 1633443242664,
    "value": 1633443242664
  },
  "sleep.wakeup_score": {
    "description": "14% wakeup consistency score.",
    "icon": null,
    "icon_font": null,
    "title": "Wakeup consistency",
    "updated_ms": 1633443242664,
    "value": 14.0
  }
}
```
