# Customer Ad Engagement — V1 Candidate Schema

> **Grain:** one row per engagement event.

| Lineage | Attribute | Data type | Notes |
|---|---|---|---|
| Direct Event | `event_id` | `VARCHAR` | Unique identifier for the event |
| Direct Event | `event_timestamp` | `TIMESTAMP` | Timestamp when the event occurred |
| Direct Event | `event_type` | `VARCHAR` | Engagement event such as impression, view, click, or conversion |
| Direct Event | `visitor_id` | `VARCHAR` | Anonymous visitor identifier captured with the event |
| Direct Tagging / Context | `campaign_id` | `VARCHAR` | Campaign identifier |
| Direct Tagging / Context | `ad_id` | `VARCHAR` | Ad identifier |
| Direct Tagging / Context | `creative_id` | `VARCHAR` | Creative identifier, if supported by source |
| Direct Tagging / Context | `placement_id` | `VARCHAR` | Placement identifier, if supported by source |
| Direct Tagging / Context | `marketing_channel` | `VARCHAR` | Marketing delivery channel |
| Direct Tagging / Context | `device_type` | `VARCHAR` | Device context such as mobile or desktop |
| Resolved / Derived | `customer_id` | `VARCHAR` | Resolved known-customer identifier; nullable for anonymous traffic |
| Resolved / Derived | `identity_type` | `VARCHAR` | Identity state, for example anonymous, authenticated, or resolved |
| Resolved / Derived | `identity_resolved_flag` | `BOOLEAN` | Whether the visitor identity is successfully mapped to a customer |
| Resolved / Derived | `session_id` | `VARCHAR` | Derived visit/session identifier used for journey reconstruction |
| Conversion | `conversion_id` | `VARCHAR` | Merchant-confirmed conversion identifier; populated only for conversion events |

## Confirmed Schema Principles

- Event grain is the most detailed level: **one row per event**.
- Direct event data and direct campaign/ad context are retained at event level.
- Identity resolution and sessionization enrich individual events without changing the grain.
- `marketing_channel` and `device_type` are separate concepts.
- `event_sequence_in_session`, browser, OS, geo attributes, source/medium, tracking code, and conversion type are not part of V1.
- `conversion` is defined as an actual merchant transaction completed and confirmed back to the ad platform.
- Detailed transaction economics are out of scope for this data product.

## Next Schema Decisions

The following will be finalized as the data contract is developed:

- required versus optional attributes
- accepted values / taxonomy for `event_type`, `marketing_channel`, `device_type`, and `identity_type`
- nullability rules
- uniqueness and relationship rules
- source-to-target derivation for resolved / derived attributes
- event freshness and update expectations
