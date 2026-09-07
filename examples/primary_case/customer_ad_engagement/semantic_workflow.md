# Customer Ad Engagement — V1 Semantic Workflow

## Funnel

```mermaid
flowchart LR
    I[Impression<br/>Ad was served to the customer]
    V[View<br/>Source emits the event after its<br/>visibility or attention rule is satisfied]
    C[Click<br/>Customer actively clicked the ad]

    I --> V --> C
```

The V1 funnel is `impression → view → click`. A view is a directly emitted source event; it is not derived in staging. A platform rule may, for example, require the ad to remain visible for at least three seconds before emitting the event.

Conversion and transaction outcomes are outside the V1 workflow.

## Raw-to-Staging Workflow

```mermaid
flowchart TB
    RAE[raw_ad_events<br/>One row per tracked ad interaction event]
    RIM[raw_identity_map<br/>One row per visitor-account<br/>identity state version]
    RAM[raw_ad_metadata<br/>One row per ad configuration version]

    T[Allowed staging operations<br/>rename, cast, trim,<br/>basic case normalization]
    STG[stg_ad_events<br/>One row per tracked ad interaction event]
    OUT[Event types support the V1 funnel<br/>impression → view → click]

    RAE --> T --> STG --> OUT
    RIM --> EX[Not applied in stg_ad_events]
    RAM --> EX
```

`stg_ad_events` preserves the grain and columns of `raw_ad_events`, except that `raw_event_type` is renamed to `event_type`.

Identity resolution, sessionization, metadata enrichment, and aggregation do not occur in `stg_ad_events`. No downstream use of `raw_identity_map` or `raw_ad_metadata` is defined by the confirmed staging design.

See [`raw_source_design.md`](./raw_source_design.md) for the complete confirmed source inventories and staging mapping.
