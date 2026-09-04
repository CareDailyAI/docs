# Synthetic API: Fall History

Fall history will maintain a time-series record of each fall incident detected at the location. The start time of the fall, in milliseconds, is the unique identifier (timestamp) of each entry in this time-series state variable.

Falls are recorded from every fall-detecting device supported by the bot:

* Radar devices: Vayyar Care (device type `2000`), AeroSense Assure (`2020`), Pontosense (`2007`) and Nobi (`2003`).
* Wearable / mobile PERS buttons with fall detection: Intrex Multi Button (`2031`), Comarch MPers Button (`2006`) and Becklar Belle X (`4280`).
* Emergency SOS fall alerts relayed from a wearable (Apple Watch, Samsung Watch, etc.). These entries have no `device_id`, `device_desc` or `device_type`.

Only Vayyar Care, AeroSense Assure and Pontosense report 3D target positions, so `targets` is an empty list for the other sources.

| Property            | Type          | Description                                                                                                                                                                           |
|---------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `device_id`         | String        | Device ID that detected the fall. Absent for Emergency SOS falls.                                                                                                                     |
| `device_desc`       | String        | Nickname / description of the device that detected the fall. Absent for Emergency SOS falls.                                                                                          |
| `device_type`       | int           | Device type that detected the fall. Absent for Emergency SOS falls.                                                                                                                   |
| `goal_id`           | int           | Behavior (goal) ID of the device that detected the fall, as defined in the `behaviors` state (for radars: 0 = Bedroom, 1 = Bathroom, 2 = Living Room, 3 = Kitchen, 4 = Other, 5 = Office). |
| `targets`           | List of Dicts | 3D target data points recorded during the fall. Each entry is a dictionary of `{ "target_id": { "x": x, "y": y, "z": z } }` in centimeters, captured when the fall started and again when it ended. |
| `end_time_ms`       | int           | End timestamp of the fall event in milliseconds. If this exists, the fall has concluded. Note the start time is recorded as the unique identifier in this time-series state variable. |
| `duration_ms`       | int           | Duration of the fall event in milliseconds. If this exists, the fall has concluded.                                                                                                   |
| `test`              | Boolean       | True until a fall alert (conversation) is started for this fall; False means this was a real, alerted fall. Falls that never produce an alert stay `true`.                             |
| `confirmed`         | int           | Confirmation status: 0 = unconfirmed, 1 = confirmed (a person accepted the alert), 2 = true positive, 3 = false positive, 4 = true negative, 5 = false negative. Set to 0 when the fall ends if nobody confirmed it. |
| `fall_confirmation_<status>` | int  | Timestamp in milliseconds when `confirmed` was set to the given status, where `<status>` is one of `unconfirmed`, `confirmed`, `true_positive`, `false_positive`, `true_negative`, `false_negative` (for example `fall_confirmation_true_positive`). |
| `fall_confirmation_<status>_user_id` | int | User ID of the person who confirmed / labeled the fall with the given status, if known.                                                                                          |
| `alert_start_ms`    | int           | Timestamp in milliseconds when the fall alert (conversation) was started. Present only for alerted falls.                                                                              |
| `alert_end_ms`      | int           | Timestamp in milliseconds when the fall alert was resolved.                                                                                                                           |
| `alert_duration_ms` | int           | `alert_end_ms` minus `alert_start_ms`.                                                                                                                                                |
| `alert_reason`      | String        | Why the alert ended. Currently always `"resolved"`.                                                                                                                                    |
| `notified_residents_ms` | int       | Timestamp in milliseconds when residents were notified of the alert by SMS / push.                                                                                                    |
| `notified_supporters_ms` | int      | Timestamp in milliseconds when supporters (family / friends) were notified.                                                                                                           |
| `notified_admins_ms` | int          | Timestamp in milliseconds when organization admins were notified by email.                                                                                                            |
| `notified_ecc_ms`   | int           | Timestamp in milliseconds when the alert was escalated to the Emergency Call Center.                                                                                                   |
| `first_response_ms` | int           | Timestamp in milliseconds of the first chat / SMS response to the alert. Only the first response is recorded.                                                                          |
| `feedback_ms`       | int           | Timestamp in milliseconds when a user gave feedback on the alert.                                                                                                                      |
| `feedback_type`     | String        | `"okay"` (the alert was a real fall) or `"wrong"` (the alert was a false alarm).                                                                                                        |
| `labeled_ms`        | int           | Timestamp in milliseconds when a user labeled the fall in the follow-up labeling conversation.                                                                                          |
| `label`             | int           | Labeling option chosen: 1 = true positive, 2 = expected (neither true nor false positive), 3 = false positive, 4 = caused by another party, 5 = unlabeled.                             |
| `trend_logged`, `trend_logged_duration_ms` | Boolean, int | Internal bookkeeping used to keep the falls trends consistent when a fall is later re-classified. Ignore.                                                                |

## Output

State Variable Name : `falls`

#### Example

```
{
  "device_id": "id_MzA6QUUQTQ6RTM6OY6RUMF",
  "device_type": 2000,
  "device_desc": "Office",
  "goal_id": 5,
  "duration_ms": 163909,
  "end_time_ms": 1644866319396,
  "test": false,
  "confirmed": 2,
  "fall_confirmation_true_positive": 1644866402117,
  "fall_confirmation_true_positive_user_id": 123456,
  "alert_start_ms": 1644866157011,
  "alert_end_ms": 1644866402117,
  "alert_duration_ms": 245106,
  "alert_reason": "resolved",
  "notified_residents_ms": 1644866157204,
  "notified_supporters_ms": 1644866217390,
  "first_response_ms": 1644866260882,
  "labeled_ms": 1644866402117,
  "label": 1,
  "locationId": 271383,
  "organizationId": 100,
  "targets": [
    {
      "0": {
        "x": 104,
        "y": 37,
        "z": 40
      }
    },
    {
      "1": {
        "x": 107,
        "y": 38,
        "z": 32
      }
    },
    {
      "2": {
        "x": 110,
        "y": 38,
        "z": 38
      }
    },
    {
      "3": {
        "x": 108,
        "y": 36,
        "z": 43
      }
    }
  ]
}
```

## References
* `com.ppc.BotProprietary/signals/falls/falls.py` (fall lifecycle signals and `FallConfirmation` values)
* `com.ppc.Microservices/intelligence/falls/location_fall_microservice.py` (writes the `falls` state variable)
