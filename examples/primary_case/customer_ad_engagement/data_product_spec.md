# Customer Ad Engagement Data Product — V1 Design Spec

> **Status:** Primary data product / schema defined; data contract in progress

## Purpose

Provide a reusable, customer-side, event-level representation of advertising exposure and engagement so downstream analytics can reconstruct the ad journey, evaluate journey completeness and drop-off, and connect engagement back to campaign and identity context.

The product is intentionally modeled at the **most detailed event grain** and is continuously updated as new engagement events arrive.

## Business Boundary

The customer journey represented by this product ends at `conversion`.

For V1, **conversion means an actual transaction completed at the merchant and subsequently confirmed back to the advertising platform** through an available tracking or postback mechanism.

Detailed transaction economics such as order amount, SKU, tax, refund, and merchant revenue are outside the scope of Customer Ad Engagement and can be modeled separately.

## Grain

> **One row per engagement event.**

The product does not aggregate to session, customer, campaign, or daily grain. Sessionization and identity resolution are event-level enrichments attached back to individual event records.

## Semantic Design

See [`semantic_workflow.md`](./semantic_workflow.md) for the customer journey, identity, campaign/ad tagging, device/channel context, sessionization, and conversion-boundary workflow.

The event-level composition is:

```text
ONE ROW PER EVENT
=
DIRECT EVENT DATA
+
DIRECT TAGGING / CONTEXT
+
RESOLVED / DERIVED EVENT-LEVEL ENRICHMENT
```

## V1 Schema

See [`schema.md`](./schema.md) for the standalone V1 candidate schema and attribute data types.

The schema currently includes:

- direct event fields such as event ID, event timestamp, event type, and visitor ID
- direct campaign/ad context such as campaign, ad, creative, placement, marketing channel, and device type
- resolved/derived identity and session attributes
- a merchant-confirmed conversion identifier for conversion events

## Relationship to Campaign Intelligence

Campaign setup, lifecycle status, and campaign economics remain in the supporting **Campaign Intelligence** data product rather than being duplicated here.

Customer Ad Engagement retains the campaign/ad identifiers needed to connect individual engagement events to that supporting context.

## Confirmed V1 Decisions

- Customer Ad Engagement is the primary data product for the implementation case.
- Grain is one row per engagement event.
- The journey is event based and supports incomplete journeys as well as completed conversions.
- Identity resolution enriches events without changing event grain.
- Session is derived and used for journey reconstruction, completeness, and drop-off analysis.
- Session ID is not the primary conversion-attribution key.
- `marketing_channel` and `device_type` are separate concepts.
- Conversion is the end of this product and means an actual merchant transaction completed and confirmed back to the ad platform.
- Detailed transaction data and transaction economics are out of scope.

## Next Step Toward the Data Contract

With business purpose, grain, semantic workflow, and candidate attributes defined, the next design work will finalize contract-level metadata such as:

1. required versus optional fields
2. accepted values and business taxonomy
3. nullability, uniqueness, and relationship rules
4. source lineage and raw-versus-derived logic
5. sessionization and identity-resolution definitions
6. freshness / update expectations
7. data-quality tests and validation rules

Raw-source selection and dbt implementation will follow these contract decisions.
