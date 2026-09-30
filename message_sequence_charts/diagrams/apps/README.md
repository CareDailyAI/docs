# Application MSC Diagrams

Client application message sequences: how a User, a Client, a Device, the Server and the bots
actually talk to each other, in order.

Each flow below has its own page with the charts and, alongside them, links to the specific API
calls each arrow represents.

---

## User Login and Registration

[8 charts](user_login_and_registration/README.md) covering the whole authentication surface: signing
up, signing in, the second step where an account requires one, and password reset. The branches are
drawn as branches, so you can see which path a given account takes rather than inferring it.

Pair it with the [Authentication guide](../../../platform_apis/authentication.md), which covers the
key types and the traps.

## Device Onboarding

[5 charts](device_onboarding/README.md) taking a device from unboxed to reporting: registering it to
a location, letting it find its device server, and the point at which it starts producing
measurements. This is the flow to read when a device pairs successfully and then never appears
where you expected it.

## Device Configuration

[Changing a device](device_configuration/README.md) once it is installed. Short, and it is the one
that explains where a configuration change actually lands.

## Device UI

[How a device screen is assembled](device_ui/README.md), which is more involved than it sounds
because the content comes from two places at once: the platform for the device itself, and the bots
for everything interpreted on top of it. If you cannot work out where a field on a device screen
comes from, it is answered here.

## Mobile App Schema

[13 charts](mobile_app_schema/README.md) of the app's overall structure: what loads when, in what
order, and what depends on what. This is the one to read before building a whole client rather than
a single screen.

## Services and Alerts

[Turning services on and off](services_and_alerts/README.md), and how an alert reaches a person.
Sits directly on top of the [Services](../../../synthetic_apis/services.md) and
[Action Plans](../../../synthetic_apis/action_plans.md) Synthetic APIs.

## Related

- [Message Sequence Charts](../../README.md)
- [Guides](../../../guides/README.md), the same flows told as stories
