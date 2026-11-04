# Event Streaming

Care Daily's platform is capable of streaming events, subscription information, and insights into a partner's platform.
There are several mechanisms available to stream data into a partner's platform including tools like AWS SQS, AWS EventBridge, Kafka, and others.
This document will capture information about some of the data formats of information available to stream from the Care Daily platform.

| Data Type | Description |
| :-------: | ----------- |
| 1 | [Location Narrative](#narrative-event-streaming) |
| 2 | [Organization Narrative](#narrative-event-streaming) |
| 3 | [Location State](#location-state-streaming) |
| 5 | [Location Time-Series State](#location-state-streaming) |
| 11 | [Escalation](#escalation-streaming) |

| Operation | Description |
| :-------: | ----------- |
| 1 | Create |
| 2 | Update |
| 4 | Delete |


#### General Data Structure

```
{ 
  "timestamp": long int,        // current time in milliseconds
  "cloudname": string,          // 'SBOX', 'Prod'
  "parentOrganizationId": int,  // Parent Organization ID
  "locationExternalId": string, // Location external ID
  "externalUsers": [            // all external user IDs associated with the location
    {
      "userId": int,                // Care Daily internal user ID
      "applicationId": int,         // External cloud application ID
      "externalUserId": string,     // External cloud user ID (e.g. patient ID or resident ID)
      "externalLocationId": string  // External cloud location ID (e.g. room ID)
    }
  ],
  "externalLocations": [        // references to external locations, rooms, units linked to the related location
    {
      "applicationId": int,         // External cloud application ID
      "locationType": int,          // External location type
      "externalLocationId": string  // External cloud location ID (e.g. room ID or unit ID)
    }
  ],
  "data" : { 
    "type": byte,               // data type
    "operation": byte,          // 1 – create, 2 – update, 4 – delete
    "locationId": int,          // Location ID if available
    "organizationId": int,      // Organization ID
    "narrative": {},            // Narrative data
    "locationState": {},        // Location state data
    "escalation": {}            // escalation
  }
}
```


## Narrative Event Streaming

Narratives are time-series information produced by bots. They can be machine-readable (such as analytics) or human-readable.

Note that Narratives can be updated (see the `data.operation` field). The narrative title is typically human-readable, except in the case of analytic narratives (priority=-1) where the title is intended to be machine-readable.

See additional [Narrative documentation](https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Locations/operation/Create%20or%20Update%20a%20Narrative).

| Priority | Description |
| :------: | ----------- |
| -1 | Analytic, machine-readable narrative / analytic |
| 0 | Detail-level logging, human-readable narrative, usually with machine-readable `target` properties. |
| 1 | Info-level logging, human-readable narrative. Default for human-readable information. |
| 2 | Warning-level logging. |
| 3 | Critical-level logging. |


#### Narrative JSON Formatting

```
{ 
  "timestamp": long int,        // current time in milliseconds
  "cloudname": string,          // 'SBOX', 'Prod'
  "parentOrganizationId": int,  // Parent Organization ID
  "locationExternalId": string, // Location external ID
  "data" : { 
    "type": byte,               // 1 - location narrative, 2 - organization narrative
    "operation": byte,          // 1 – create, 2 – update, 4 – delete
    "locationId": int,          // Location ID
    "organizationId": int,      // Organization ID
    "narrative": {
      // narrative fields, many are optional 
      "narrativeId": int,       // auto generated ID, PK 
      "narrativeDate": long int, // part of a PK, can be different from creationDate, e.g. in the future
      "creationDate": long int, // creation time
      "locationId": int,        // location ID 
      "narrativeType": byte,    // 0 - default, 1 - deleted user, 2 - deleted location, 3 - location moved to another organization 
      "priority": byte,
      "status": byte,           // 0 - initial, 1 - deleted, 2 - resolved, 3 - reopened 
      "eventType": string,      // event type
      "appInstanceId": int,     // bot instance ID created this record, optional 
      "icon": string,           // 50 characters max 
      "iconFont": string,       // 50 characters max 
      "title": string,          // 250 characters max 
      "description": string,    // 1000 characters max 
      "target": {},             // flexible JSON structure with maximum serialized size of 10K characters 
      "organizationId": int,    // organization ID for organization narratives 
      "userId": int             // deleted user ID, populated when user is removed and downstream consumers should also purge user data 
    }
  }
}
```


## Location State Streaming

Location State variables are named objects with flexible structure set by bots or user apps for specific location.

Location Time-Series States are location states saved for specific timestamp.

See [Synthetic APIs](../synthetic_apis/README.md) for details.



#### Location State JSON Formatting

```
{ 
  "timestamp": long int,        // current time in milliseconds
  "cloudname": string,          // 'SBOX', 'Prod'
  "parentOrganizationId": int,  // Parent Organization ID
  "locationExternalId": string, // Location external ID
  "data" : { 
    "type": byte,               // 3 - Location State, 5 - Location Time-Series State
    "operation": byte,          // 1 – create, 2 – update, 4 – delete
    "locationId": int,          // Location ID
    "organizationId": int,      // Organization ID
    "locationState": { 
      "locationId": int,        // location ID 
      "name": string,           // variable's name
      "stateDateMs": long int,  // timestamp of time-series state
      "value": {},              // flexible JSON structure
      "deleted": string[]       // string array of deleted top level properties
    }
  }
}
```


## Escalation Streaming

Escalations are significant events captured inside Care Daily platform. For examples, a fall alert, an emergency request, a device outage, "not back home".


#### Escalation JSON Formatting

```
{ 
  "timestamp": long int,        // current time in milliseconds
  "cloudname": string,          // 'SBOX', 'Prod'
  "parentOrganizationId": int,  // Parent Organization ID
  "data" : { 
    "type": byte,               // 11 - escalation
    "operation": byte,          // 1 – create
    "locationId": int,          // Location ID
    "organizationId": int,      // Organization ID
    "escalation": {
      "escalationId": int,
      "escalationType": int,
      "status": int,
      "title": string,
      "description": string,
      "creationDate": long int,
      "eventDate": long int,
      "userId": int,
      "deviceId": string,
      "eventSourceType": int,
      "resolutionDate": long int,
      "resolveUserId": int,
      "resolveSourceType": int
    }
  }
}
```
