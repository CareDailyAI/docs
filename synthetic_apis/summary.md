# Synthetic API: Location Summary

The `summary` state variable assists user interfaces by providing snapshots of 'scores' back in time which rank
how well this location is doing or was doing. It can also include a 'badge' which may notify a person
to pay more attention to this location, plus methods to clear or set ("Mark as unread") that badge.

These location summaries are used when loading a list of locations where we want to identify the
location we should focus human attention upon.

The `summary` is produced by `com.ppc.Microservices/intelligence/score_wellness/location_wellness_score_microservice.py`. The score is the 0-100 wellness score, which is also published as the `wellness_score` field of the `location_properties` state variable and as the `trend.wellness_score` trend.

| Property  | Type  | Description                                     |
|-----------|-------|-------------------------------------------------|
| `badge`   | int   | 0 = No notification; 1 = Show a notification badge |
| `badgeDate` | str | ISO 8601 UTC timestamp of when the badge was last set or cleared, or null |
| `badgeDateMs` | int | Same as `badgeDate` in unix epoch milliseconds, or null |
| `divergence` | dict | Optional. Present when the composite score is moving in the opposite direction to the dimensions underneath it. Contains `detected` (bool), `composite_delta`, `composite_baseline`, `baseline_days`, `falling` / `rising` (lists of trend IDs), `falling_weight` / `rising_weight`, and `dimensions`. |
| `now` key | dict  | Latest snapshot                            |
| `now.value` | int | Current wellness score (0-100) |
| `now.diff` | int | Always 0 for the latest snapshot |
| `now.avg` | float | Today's average of the `trend.wellness_score` trend, or the current score if no trend is available |
| `now.distribution` | dict | How each weighted trend contributed to the score. Contains `total_trend_weight`, optional `unavailable` (`{trend_id: reason}` for trends that aged out), and one entry per trend ID with `total_time_weight`, `total_score_contribution`, and per-interval (`"now"`, `"0"`, `"15"`, ...) `trend_weight_percent`, `time_weight_percent`, `percent_contribution`, `normalized_score`, `score`. |
| `0` key   | dict  | 7-day averaged trends from the past 7-days      |
| `15` key  | dict  | 7-day averaged trends from 15 days ago |
| `30` key  | dict  | 7-day averaged trends from 30 days ago |
| `45` key  | dict  | 7-day averaged trends from 45 days ago |
| `60` key  | dict  | 7-day averaged trends from 60 days ago |
| `90` key  | dict  | 7-day averaged trends from 90 days ago |
| `{interval}.value` | float | Average wellness score over that historical interval |
| `{interval}.diff`  | int | Rounded difference between the latest snapshot and this past value |
| `{interval}.diff_suppressed` | bool | Optional. True when a positive `diff` was forced to 0 because `divergence.detected` is true (the rise is not supported by the underlying dimensions). |

All keys are strings (`"now"`, `"0"`, `"15"`, ...). Interval keys are only present when historical weekly trends exist for that interval.

| Badge Value | Description       |
|-------------|-------------------|
| 0           | No notification   |
| 1           | Show Notification |


## Output

State Variable : `summary`

#### Example

```
{
    "value": {
        "badge": 0,
        "badgeDate": "2022-04-05T18:22:10.000+0000",
        "badgeDateMs": 1649182930000,
        "now": {
            "value": 76,
            "diff": 0,
            "avg": 75.5,
            "distribution": {
                "total_trend_weight": 55,
                "trend.sleep_score": {
                    "total_time_weight": 70,
                    "total_score_contribution": 41.2,
                    "now": {
                        "trend_weight_percent": 0.55,
                        "time_weight_percent": 0.57,
                        "percent_contribution": 0.31,
                        "normalized_score": 80.0,
                        "score": 24.8
                    },
                    "0": { ... }
                },
                "trend.mobility_score": { ... }
            }
        },
        "0": {
            "value": 71.37,
            "diff": 4
        },
        "15": {
            "value": 68.9,
            "diff": 7
        }
    }
}
```

## Input

#### Data stream address

`set_badge`

Sent internally by `signals.badge.set_badge()` (`com.ppc.BotProprietary/signals/badge.py`, `BADGE_NONE = 0`, `BADGE_NOTIFY = 1`). Setting the badge to 0 also updates `badgeDate` / `badgeDateMs`.

#### Data stream content

Clear the badge
```
{
    "badge": 0
}
```

Mark unread (set the badge again)
```
{
    "badge": 1
}
```
