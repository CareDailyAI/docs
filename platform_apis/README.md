# Care Daily AI+IoT SaaS Documentation

All of the interactive *platform* documentation is updated and managed online.
Please follow these links for more details.

## Application API
http://iotapps.docs.apiary.io

This documentation describes available APIs for mobile apps and web consoles. 

These Application APIs are primarily synchronous RESTful APIs, and WebSocket alternatives do exist for some APIs.
The Application API primarily focuses on APIs for end-user applications, although some APIs can be called with an `ADMIN_API_KEY` to execute as an administrator of an organization.

In addition, there are several APIs toward the beginning of the documentation for devices, allowing them to understand which of the device servers they should communicate with in a cloud deployment composed of multiple device servers.

## WebSockets API

[WebSockets API Documentation](websockets.md)

Use WebSockets in some time-critical experiences (such as updating the UI with bot-driven [Synthetic APIs](../synthetic_apis/README.md) or displaying alerts on an administrative console), instead of polling with RESTful APIs.

## Cloud-to-Cloud Streaming 

[Event Streaming Documentation](event_streaming.md)

Care Daily's platform can stream events, insights, subscriptions, and more to partner platforms.

## Administrative API
http://iotadmins.docs.apiary.io

This document captures admin-specific APIs that were not documented in the Application API.
These APIs are primarily used by administrative command centers to manage people, places, and things.

## Device API

[AWS IoT Core](mqtt.md)

Care Daily recommends using MQTT protocol through AWS IoT Core to communicate devices data to the cloud.

In addition Care Daily supports a set of asynchronous HTTP and WebSocket Device APIs.

http://iotdevices.docs.apiary.io

Devices, identified by their globally unique IDs, first need to be understood through the definition of a *device type* on the server, and then need to be registered to a specific location before they can start communicating. 

## Bot API
http://iotbots.docs.apiary.io

This is private bot API documentation for bot infrastructure developers. The APIs documented in this private area are implemented as software APIs inside the `botengine`.
The documentation also describes the management and lifecycles of a bot.

Today, we link bots to subscriptions manually on the backend, and there are no APIs publicly or privately exposed to manage the definitions of these subscriptions.
We rely on communications with our server team to define and manage the available subscription services in each organization.


## Security Modes and Occupancy Status

[Security Modes and Occupancy Status](modes.md)

Explanation on how to configure and interpret the "Location Scene" field to be recognized by existing application layers.

