# Synthetic API: Machine Learning

Request all machine learning models to recalculate. 

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

```
{
    "force": true,
    "reference": "all"
}
```

## References
* `com.ppc.Microservices/intelligence/data_request/location_datarequest_microservice.py`
