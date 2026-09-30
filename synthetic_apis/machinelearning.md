# Synthetic API: Machine Learning

<!-- at-a-glance -->
> **Data stream in** `download_data`  ·  [All Synthetic APIs](README.md)

Request all machine learning models to recalculate. 

**When to use it:** you are developing or testing bots and want the models on a location to recalculate from history.

Useful primarily for bot developer activities.

#### Properties
| Property | Type | Description |
| -------- | ---- | ----------- |
| force    | Boolean | True to force the recalculation of machine learning models. Without it, a request with reference "all" is skipped if another "all" request was made within the last hour. |
| reference | String | Reference for internal microservices to understand what data is provided from the server, use "all" to capture all data from the user's account and properly recalculate all models that rely upon all data. Default is "all". |
| oldest_timestamp_ms | int | Optional. Oldest timestamp in milliseconds to retrieve data from. Default is 6 months ago. If set, `reference` must not be "all" or the request is rejected. |

## Inputs

Data Stream Address : `download_data`

#### Content

```json
{
    "force": true,
    "reference": "all"
}
```

## Related

- [Bots and services](../concepts/bots_and_services.md)
- [Data streams and state](../concepts/data_streams_and_state.md)

## References
* `com.ppc.Microservices/intelligence/data_request/location_datarequest_microservice.py`
