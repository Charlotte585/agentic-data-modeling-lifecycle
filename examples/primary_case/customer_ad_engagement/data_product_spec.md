# Customer Ad Engagement Data Product — V1 Design Spec

> **Status:** Confirmed V1 scope and source/staging design

## Purpose

Provide the event-level foundation for analyzing customer ad exposure and engagement across the V1 funnel:

```text
impression → view → click
```

The design preserves individual tracked ad interaction events so downstream business modeling can be defined separately.

## V1 Business Boundary

V1 includes these funnel events:

- `impression`: the ad was served to the customer.
- `view`: the source directly emits a view event once the platform's visibility or attention rule is satisfied, such as the ad remaining visible for at least three seconds.
- `click`: the customer actively clicked the ad.

Conversion and transaction outcomes are outside the V1 boundary. V1 does not define conversion events, conversion attributes, transaction attributes, or conversion-attribution logic.

## Confirmed Raw Sources

V1 uses three raw sources:

| Source | Grain |
|---|---|
| `raw_ad_events` | One row per tracked ad interaction event |
| `raw_identity_map` | One row per visitor-account identity state version |
| `raw_ad_metadata` | One row per ad configuration version |

All three sources will use realistic synthetic fixtures. Public advertising datasets may inform semantics, but they are not V1 implementation inputs.

See [`raw_source_design.md`](./raw_source_design.md) for the confirmed source columns, version-record conventions, and `stg_ad_events` mapping.

## Confirmed Staging Boundary

`stg_ad_events`:

- preserves the `raw_ad_events` grain of one row per tracked ad interaction event
- renames `raw_event_type` to `event_type`
- performs only rename, cast, trim, and basic case normalization
- does not perform identity resolution, sessionization, metadata enrichment, or aggregation

No other staging model behavior is confirmed in this V1 design.

## Schema and Semantic Workflow

- [`schema.md`](./schema.md) records only the confirmed raw and `stg_ad_events` attributes; it does not assign unconfirmed data types or add derived attributes.
- [`semantic_workflow.md`](./semantic_workflow.md) shows the V1 funnel and the boundary between raw inputs and `stg_ad_events`.

## Not Defined in V1

The confirmed decisions do not yet define downstream intermediate or mart models, identity-resolution behavior, session logic, metadata joins, aggregations, source YAML, tests, or detailed data contracts.
