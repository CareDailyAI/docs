# Synthetic APIs

## Synthetic API Libraries

#### User Interfaces

| Synthetic API                               | Input Addresses                        | Output Address                                                                                    | Description                                                                                                                                                      |
|---------------------------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Dashboard Header](dashboard_header.md)     | `update_dashboard_header`              | `dashboard_header`                                                                                | #1 thing you need to know about this location.                                                                                                                   |
| [Dashboard Status](dashboard_status.md)     | `update_dashboard_content`             | `now`                                                                                             | Interesting events that are happening now, or happened recently.                                                                                                 | 
| [Services and Alerts](services.md)          | `update_dashboard_content` (type 1)    | `services`                                                                                        | List of available services and alerts to turn on or off.                                                                                                         |
| [Insights](insights.md)                     |                                        | `insights`                                                                                        | App-friendly summary of current insights in this location (occupancy, sleep, temperature, etc.).                                                                 |
| [Daily Report](dailyreport.md)              | `report_add_event` (`daily_report_entry` is deprecated) | `dailyreport`, plus `weeklyreport` and `monthlyreport`                                    | Categorized list of important events that have happened at this location each day, week, and month.                                                              |
| [Trends](trends.md)                         | `capture_trend_data` and `remove_trend` | `trends_metadata` containing static overhead information, and `trends` containing dynamic data (plus `trends_recently`, `trends_weekly`, `trends_category`, `trends_highlights`) | Monitor trends across a variety of lifestyle patterns and Activities of Daily Living and identify when those patterns may be trending abnormal.                  |
| [Tasks](tasks.md)                           | `update_task`, `delete_task`, `update_device_bundles` | `tasks`, `device_bundles`                                                          | Assign or update a task to another person, or mark an existing task complete. Also carries system tasks such as adding people or setting up devices.            |
| [Request Assistance](request_assistance.md) | `request_assistance`                   |                                                                                                   | Request assistance from the mobile app or smart speaker, including emergency help.                                                                               | 
| [User Activity](user_activity.md)           | `user_activity`                        |                                                                                                   | Share information about what a user is doing in a mobile app with a bot, so the bot can take action and provide timely and relevant feedback and communications. |
| [Fall History](falls.md)                    |                                        | `falls`                                                                                           | Time-series history of falls detected by radars, wearables, and emergency SOS requests.                                                                          |

#### User Communications

| Synthetic API | Input Addresses | Output Address | Description |
| ------------- | --------------- | -------------- | ----------- |
| [Multistream Messages](multistream.md) | `multistream` | `multistream` | Deliver multiple data stream messages (Synthetic API inputs) simultaneously, now or at a scheduled future time. |
| [Narrate](narrate.md) | `narrate` | | Capture history into the location or organization narratives. |
| [Message](message.md) | `message` | | Communicate with users over push notification, SMS, and email. |
| [Action Plans](action_plans.md) | | `action_plans` | Assist mobile apps with communicating to users about the protocol for resolving problems that require human intervention. |

#### Devices and Automations

| Synthetic API | Input Addresses | Output Address | Description |
| ------------- | --------------- | -------------- | ----------- |
| [Behaviors](behaviors.md) | | `behaviors` | Behaviors provide the available user-selectable context for each device. |
| [Bot-driven Rules](rules.md) | `set_rule`, `delete_rule`, `pause_rule`, `play_rule` | `rules`, `rule_phrases` | Bot-driven rules engine: compose if-this-then-that rules from the phrases each device offers. |
| [Radar Devices](vayyar.md) | `set_radar_room`, `set_radar_subregion`, `delete_radar_subregion`, `set_radar_config`, `submit_radar_fall_feedback` (the `set_vayyar_*` addresses remain as deprecated aliases) | `radar_room`, `radar_subregions`, `radar_subregion_behaviors` (also written as `vayyar_*` for compatibility) | Fully manage radar devices (Vayyar Care, Pontosense, Nobi, AeroSense Assure) to detect falls and occupancy. |

#### Command Centers

| Synthetic API                                                                                             | Input Addresses | Output Address | Description                                                    |
|-----------------------------------------------------------------------------------------------------------|-----------------|----------------|----------------------------------------------------------------|
| [Location Summary](summary.md) | `set_badge`     | `summary`     | Summary of the score and notification badges for each location |


#### Developer Tools

| Synthetic API | Input Addresses | Output Address | Description |
| ------------- | --------------- | -------------- | ----------- |
| [Machine Learning](machinelearning.md) | `download_data` | | Request the bot to re-download historical data and recalculate its machine learning models. |


#### Other State Variables

These outputs are produced by bot microservices but do not yet have a dedicated page. Names marked *time-series* are keyed by timestamp. The writing microservice is listed so developers can read the JSON shape from the source.

| Output Address | Type | Written by | Description |
| -------------- | ---- | ---------- | ----------- |
| `occupancy` | time-series | `occupancy/location_occupancy_microservice.py` | Occupancy status over time: `PRESENT`, `ABSENT`, `SLEEP`, `VACATION`. |
| `occupancy_overview` | | `occupancy/location_occupancy_microservice.py` | Current occupancy status, override flag, and the time the status began. |
| `dashboard_overview` | | `dashboard/location_dashboard_overview_microservice.py` | Combined occupancy, sleep, header, and status cards for a single dashboard read. |
| `location_highlights` | | `highlights/location_highlights_microservice.py` | Weighted highlight elements (sleep, bathroom, safety, occupancy, medication, devices) with status colors and tags. |
| `checkin_status` | time-series | `checkin/location_checkin_microservice.py` | Daily check-in state: occupancy reason, bed occupancy, predicted and actual wake-up and bedtime. |
| `stability_events` | time-series | `falls/location_stability_microservice.py` | Radar stability events, same shape as [Fall History](falls.md) entries. |
| `movements` | time-series | `movements/location_movements_microservice.py` | Radar-tracked movement episodes with distances travelled. |
| `visitors` | time-series | `visitors/location_visitor_microservice.py` | Detected visits: contributing devices, source, visitor count, and duration. |
| `assessment_results` | time-series | `assessment/location_assessment_microservice.py` | Physical assessment results (gait speed, timed up-and-go, chair stand, grip strength, balance, and more). |
| `goals` | | `goals/location_goals_microservice.py` | User goals keyed by goal ID with category, timestamps, and completion. |
| `sleep_model` | | `occupancy/sleep/location_sleep_microservice.py` | Learned going-to-sleep, waking-up, and peak-morning times for each weekday. |
| `sleep_flow` | | `occupancy/sleep/location_sleepflow_microservice.py` | Per-weekday history of sleeping and awake hours used to shape the sleep model. |
| `security_state` | | `prosecurity/location_security_intelligence.py` | Security arm state and alarm description. |
| `survey_results`, `survey_statistics` | time-series, regular | `surveys/location_survey_microservice.py` | Individual survey answers, and completion statistics for the survey list. |
| `resident_report` | time-series | `reports/location_reports_resident_microservice.py` | Resident-facing edition of the periodic report. |

All paths are under `com.ppc.Microservices/intelligence/` in botlab-core.

#### Other Input Addresses

| Input Address | Handled by | Description |
| ------------- | ---------- | ----------- |
| `clear_dashboard_content` | `dashboard/location_dashboard_microservice.py` | Remove every card from the `now` and `services` state variables. No content required. |
| `clear_dashboard_headers` | `dashboard/location_dashboardheader_microservice.py` | Remove every dashboard header. No content required. |
| `capture_fall` | `falls/location_fall_microservice.py` | Record or close a fall event in the `falls` time-series (see [Fall History](falls.md)). Content: `start_time_ms`, `device_id`, `device_desc`, `device_type`, `targets`, and `end_time_ms` to close. |
| `capture_stability_event` | `falls/location_stability_microservice.py` | Same content as `capture_fall`, written to `stability_events`. |
| `capture_movement` | `movements/location_movements_microservice.py` | Record or close a movement episode in `movements`, with `distance_m` in place of `targets`. |
| `report_generate` | `reports/location_reports_microservice.py` | Generate a daily, weekly, or monthly report on demand (see [Daily Report](dailyreport.md)). |

<!---
#### Energy Management
+ [Demand Response](demandresponse.md)
+ [Time-of-Use Pricing](toupricing.md)
--->

## About
Synthetic APIs are provided by the *bot application layer*, on top of the platform. Synthetic APIs effectively allow bot and UI developers to invent new application features beyond what the AI+IoT platform offers alone. You can create your own application APIs on this platform, with bots.

These asynchronous APIs offered by bot application developers leverage `data stream messages` to communicate data into the bot, and `state` variables to communicate responses back from the bot. 

The Synthetic APIs we document here are for our most popular bot microservice packages that drive user interfaces. Not all Synthetic APIs have both inputs and outputs, but all offer some interaction with the bots.

## Inputs: Data Stream Messages

Bots receive messages from the outside world (and between microservices running inside the bot) via `data stream messages`. These messages have an address and arbitrary JSON content.

[Data Stream Message API Documentation](https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Synthetic-APIs/operation/Stream%20message)

#### Properties of Data Stream Messages

* Bots and apps and other tools capable of making RESTful API calls can send data stream messages.
* Each data stream message contains an address and arbitrary JSON content.
* Each bot has to specify which data stream addresses it can receive messages for. Addresses can be populated in the bot's `runtime.json` files.
* Most data stream messages are distributed in the context of an individual location (`scope=1` if you're reading the API docs). 
* Bots within a location can communicate bi-directionally with organization bots operating at an administrative level (`scope=2` to send messages to the organization bots). 
* When messages are sent from an administrator or from an organization bot, they can be further addressed to be delivered to specific bot instance ID's or to specific location ID's.
* Data stream messages cannot send data or responses back instantaneously - they operate asynchronously. That's why we have a separate mechanism, `state` variables, to get data back out again.
* JSON content is arbitrary and agreed upon by app developers.

Mobile app developers can [get a list of data stream addresses](https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Synthetic-APIs/operation/Get%20Summary) to understand if the bots and services offer some set of capabilities.

#### Best practices for managing objects

In an implementation of a synchronous platform API for POST operations where the app would create an object on the server,
developers would normally expect the platform to reply back with an ID of the object that was created.
This, of course, allows you to edit or delete the content later.

But this kind of synchronous response isn't possible with a data stream message.
Therefore, when object management is needed, a best practice is to have the app generate a unique ID for its own object and pass in this ID with the content.
A UUID is an obvious choice for an app-generated unique ID for objects created and stored via Synthetic API.


## Outputs: Location State Variables

Bots can create `state` variables to provide data back out to applications or voice UI's. These state variables are stored in a way that can be accessed at any time through a RESTful API call or WebSocket.

[Location States API Documentation](https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Synthetic-APIs/operation/Get%20Location%20State)

#### Properties of State Variables
* Like data stream messages, state variables have an address and arbitrary JSON content.
* State variables are stored in the context of a location.
* A state variable can optionally have timestamps associated with its data, in the form of a `time-series state variable`.
* State variables are considered non-volatile memory and persist within the location, even if the bot that created it is destroyed. This can help the bot remember settings and configurations that happened in the past, without relying on the bot's internal memory which is tied to the existence of the bot.
* Apps can subscribe to multiple state variables simultaneously with WebSockets and get updated immediately as bots update the state variable content.
* JSON content is arbitrary and agreed upon by app developers.

Many times, state variables may contain extra JSON information that simply helps bots manage the objects contained within those variables.

#### Discovering which state variables a location has

Bots register the names of the state variables they write in the `location_properties` state variable: the `additional_properties` list holds the names of regular state variables, and the `timeseries_properties` dictionary maps each time-series state variable name to the timestamp of its most recent entry. Read `location_properties` first to learn which Synthetic API outputs are available in a location.


## Icons

Both `icon` and `icon_font` are fields used throughout Synthetic APIs.

+ [FontAwesome icon fonts](https://fontawesome.com)
+ [People Power icon fonts](https://webmedia.peoplepowerco.com/icons/index.html)

| icon_font value | Description |
| --------------- | ----------- |
| far             | FontAwesome - Regular |
| fab             | FontAwesome - Bold |
| fal             | FontAwesome - Light |
| fas             | FontAwesome - Solid |
| iotr            | People Power - Regular |
| iotl            | People Power - Light |
| wir             | People Power Weather - Regular |
| wil             | People Power Weather - Light |



