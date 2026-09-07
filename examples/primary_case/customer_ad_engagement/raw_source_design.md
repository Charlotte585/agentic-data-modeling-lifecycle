# Customer Ad Engagement — V1 Raw Source Design

> **Status:** Confirmed V1 raw-source and `stg_ad_events` design

## Source Strategy

All three V1 raw sources will use realistic synthetic fixtures. Public advertising datasets are semantic references only and are not implementation inputs.

## `raw_ad_events`

> **Grain:** one row per tracked ad interaction event.

| Column |
|---|
| `event_id` |
| `event_timestamp` |
| `raw_event_type` |
| `visitor_id` |
| `campaign_id` |
| `ad_id` |
| `creative_id` |
| `placement_id` |
| `device_type` |

The V1 event funnel is `impression → view → click`:

- `impression`: the ad was served to the customer.
- `view`: the source directly emits a view event once the platform's visibility or attention rule is satisfied, such as remaining visible for at least three seconds.
- `click`: the customer actively clicked the ad.

Conversion and transaction outcomes are not V1 event types.

## `raw_identity_map`

> **Grain:** one row per visitor-account identity state version.

| Column |
|---|
| `visitor_id` |
| `customer_id` |
| `account_id` |
| `identity_type` |
| `account_status` |
| `effective_from` |
| `effective_to` |

Current records use `effective_to = '9999-12-31'`.

## `raw_ad_metadata`

> **Grain:** one row per ad configuration version.

| Column |
|---|
| `ad_id` |
| `ad_name` |
| `campaign_id` |
| `creative_id` |
| `creative_name` |
| `marketing_channel` |
| `ad_status` |
| `ad_version_start_timestamp` |
| `ad_version_end_timestamp` |

Current versions use `ad_version_end_timestamp = '9999-12-31'`.

## Confirmed `stg_ad_events` Mapping

> **Grain:** one row per tracked ad interaction event, unchanged from `raw_ad_events`.

| Raw source column | Staging column | Confirmed mapping |
|---|---|---|
| `event_id` | `event_id` | Name preserved |
| `event_timestamp` | `event_timestamp` | Name preserved |
| `raw_event_type` | `event_type` | Renamed |
| `visitor_id` | `visitor_id` | Name preserved |
| `campaign_id` | `campaign_id` | Name preserved |
| `ad_id` | `ad_id` | Name preserved |
| `creative_id` | `creative_id` | Name preserved |
| `placement_id` | `placement_id` | Name preserved |
| `device_type` | `device_type` | Name preserved |

Staging transformations are limited to:

- rename
- cast
- trim
- basic case normalization

The confirmed decisions do not assign specific casts or case-normalization rules to individual columns.

`stg_ad_events` does not perform identity resolution, sessionization, metadata enrichment, or aggregation. It does not add columns from `raw_identity_map` or `raw_ad_metadata`.
