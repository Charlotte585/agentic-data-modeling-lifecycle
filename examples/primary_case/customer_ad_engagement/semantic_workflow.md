# Customer Ad Engagement — Semantic Workflow

> **Grain:** one row per engagement event (most detailed event-level data product).

```mermaid
flowchart TB
    subgraph FUNNEL[Customer Journey Funnel]
        S[Serve / Delivery] --> I[Impression] --> V[View] --> C[Click] --> ES[Engaged Session] --> CV[Conversion]
    end

    subgraph ID[Identity Resolution]
        AV[Anonymous Visitor\nvisitor_id] --> IL[Identity Linkage] --> KC[Known Customer\ncustomer_id]
    end

    subgraph TAG[Direct Ad / Campaign Tagging & Context]
        CAM[campaign_id]
        AD[ad_id]
        CR[creative_id]
        PL[placement_id]
        MC[marketing_channel]
        DT[device_type]
    end

    subgraph SESSION[Derived Session Enrichment]
        SID[session_id]
        SD[Groups temporally continuous events\nfor the same visitor/customer]
        SJ[Supports journey reconstruction,\ncompletion and drop-off analysis]
        SID --> SD --> SJ
    end

    subgraph EVENT[Unified Event-Level Record]
        E1[Direct Event Data]
        E2[Direct Tagging / Context]
        E3[Resolved / Derived Enrichment]
        E1 --> ROW[ONE ROW PER EVENT]
        E2 --> ROW
        E3 --> ROW
    end

    FUNNEL --> EVENT
    AV --> EVENT
    KC --> EVENT
    TAG --> EVENT
    SESSION --> EVENT

    CV --> BOUNDARY[Business Boundary\nConversion = actual transaction completed\nand confirmed back to the ad platform]
```

## Semantic Blocks

### 1. Funnel Events

The event journey runs from ad delivery/exposure through engagement and ends at conversion. Not every visitor completes the journey; the event-level design preserves incomplete journeys and drop-off points rather than requiring a completed funnel.

### 2. Identity

Raw events retain an anonymous `visitor_id`. When identity resolution is available, the same event can be enriched with `customer_id` and identity-resolution metadata without changing the event grain.

### 3. Ad / Campaign Tagging

Campaign and ad identifiers attach marketing context directly to the interaction so engagement can later be connected to the relevant campaign, ad, creative, placement, and marketing channel.

### 4. Device / Channel Context

`device_type` describes the device on which the interaction occurred (for example, mobile or desktop). `marketing_channel` describes the marketing delivery context; these are separate business concepts.

### 5. Session

A session is a **derived grouping of temporally continuous events for the same visitor/customer**. It is used to reconstruct customer journeys, distinguish multiple independent visits, and evaluate journey completeness and drop-off even when the customer does not convert.

`session_id` does not define the grain and is not the primary conversion-attribution key. The data product remains one row per event; sessionization is an event-level enrichment derived from visitor/customer identity, event timestamps, and agreed inactivity rules.

### 6. Conversion Boundary

For this data product, `conversion` means an **actual transaction completed at the merchant and subsequently confirmed back to the advertising platform** through an available tracking/postback mechanism.

The conversion event marks the boundary of Customer Ad Engagement. Detailed transaction economics such as order amount, SKU, tax, refund, and merchant revenue remain outside this product and can be modeled separately.

## Event-Level Data Composition

```text
ONE ROW PER EVENT
=
DIRECT EVENT DATA
+
DIRECT TAGGING / CONTEXT
+
RESOLVED / DERIVED EVENT-LEVEL ENRICHMENT
```

No session-, customer-, campaign-, or daily-level aggregation is introduced in this product.
