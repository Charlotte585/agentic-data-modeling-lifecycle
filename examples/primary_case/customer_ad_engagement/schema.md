# Customer Ad Engagement — Confirmed V1 Schema

This document records only the attributes confirmed for the V1 raw sources and `stg_ad_events`. Data types, constraints, nullability, and additional derived attributes have not been specified.

## `raw_ad_events`

> **Grain:** one row per tracked ad interaction event.

| Attribute |
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

## `raw_identity_map`

> **Grain:** one row per visitor-account identity state version.

| Attribute |
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

| Attribute |
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

## `stg_ad_events`

> **Grain:** one row per tracked ad interaction event, preserved from `raw_ad_events`.

| Attribute | Source attribute |
|---|---|
| `event_id` | `raw_ad_events.event_id` |
| `event_timestamp` | `raw_ad_events.event_timestamp` |
| `event_type` | `raw_ad_events.raw_event_type` |
| `visitor_id` | `raw_ad_events.visitor_id` |
| `campaign_id` | `raw_ad_events.campaign_id` |
| `ad_id` | `raw_ad_events.ad_id` |
| `creative_id` | `raw_ad_events.creative_id` |
| `placement_id` | `raw_ad_events.placement_id` |
| `device_type` | `raw_ad_events.device_type` |

The staging model is limited to rename, cast, trim, and basic case normalization. It adds no identity-resolution, session, metadata-enrichment, aggregation, conversion, or transaction attributes.
