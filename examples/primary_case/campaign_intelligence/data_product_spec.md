# Campaign Intelligence Data Product — V1 Design Spec

> **Status:** Draft for review  
> This document captures the current agreed design decisions for the Campaign Intelligence data product. The dbt structure remains proposed and should be reviewed before implementation.

## Product Scope

Campaign Intelligence focuses on reusable campaign setup and campaign economics information. It does **not** include campaign performance outcomes such as impressions, clicks, conversions, revenue, spend efficiency, CPA, or ROAS.

A data product is treated as a governed, reusable package composed of one or more curated models plus explicit business purpose, grain, contracts, lineage, quality rules, and documentation. A curated dataset is therefore an output of a data product, not the full data product itself.

For V1, the Campaign Intelligence data product exposes two curated models:

- `dim_campaign`
- `fct_campaign_economics`

Supported campaign channels are limited to:

- `direct search`
- `email`
- `direct mail`
- `paid search`

---

## `dim_campaign`

### Purpose

Represent campaign setup and lifecycle state while preserving historical campaign-status changes for downstream time-series and point-in-time analysis.

### Grain

One row per campaign × effective campaign-status version.

### Business Attributes

| Attribute | Description |
|---|---|
| `campaign_id` | Business identifier for the campaign |
| `campaign_channel` | Campaign delivery channel |
| `campaign_desired_start_date` | Planned campaign start date |
| `campaign_desired_end_date` | Planned campaign end date |
| `campaign_actual_start_timestamp` | Timestamp when the campaign actually becomes active |
| `campaign_actual_end_timestamp` | Timestamp when the campaign actually ends |
| `campaign_status` | Campaign lifecycle status: `live`, `freeze`, or `inactive` |

### History Strategy

`dim_campaign` preserves campaign lifecycle history using an SCD Type 2-style design.

The SCD2 change driver is:

- `campaign_status`

The remaining campaign setup attributes are treated as stable campaign context. In particular, `campaign_actual_start_timestamp` and `campaign_actual_end_timestamp` are lifecycle timestamps that are populated as the campaign progresses, but once established they are assumed to remain fixed rather than independently creating new historical versions.

This design assumes that corrections to actual start/end timestamps do not occur independently of the corresponding campaign lifecycle transition. If that assumption changes, the tracked-field strategy should be revisited.

### Technical Attributes

| Attribute | Description |
|---|---|
| `campaign_version_key` | Surrogate primary key for each historical campaign version |
| `valid_from` | Timestamp when the campaign-status version becomes effective |
| `valid_to` | Timestamp when the campaign-status version stops being effective |
| `is_current` | Indicates the current campaign version |
| `source_updated_at` | Timestamp of the source-side update |
| `loaded_at` | Warehouse load timestamp |

---

## `fct_campaign_economics`

### Purpose

Represent campaign-level funding configuration without mixing in downstream campaign performance outcomes.

### Grain

One row per campaign.

### Business Attributes

| Attribute | Description |
|---|---|
| `campaign_id` | Business identifier for the campaign |
| `budget_effective_timestamp` | Timestamp when the campaign budget becomes effective; expected to equal `campaign_actual_start_timestamp` |
| `campaign_budget_amount` | Final campaign budget amount established before campaign launch |
| `budget_currency` | Currency associated with the budget |
| `budget_type` | Budget basis, such as lifetime, daily, or another defined period |

### History Strategy

`fct_campaign_economics` does **not** maintain historical versions in V1.

The business assumption is that the campaign budget is finalized before the campaign begins and becomes effective when the campaign actually starts. Therefore:

```text
budget_effective_timestamp = campaign_actual_start_timestamp
```

Under this assumption, campaign economics are modeled as one record per campaign rather than as an effective-period history table.

### Relationship to `dim_campaign`

The fact retains `campaign_id` and `budget_effective_timestamp` as business relationship attributes. Because `dim_campaign` is historical, the appropriate campaign version can be resolved through an as-of relationship using the campaign identifier and effective timestamp rather than storing `campaign_version_key` as the primary business relationship in the fact.

Conceptually:

```text
fct_campaign_economics.campaign_id = dim_campaign.campaign_id
AND budget_effective_timestamp falls within dim_campaign.valid_from / valid_to
```

This is a temporal/as-of relationship rather than a conventional composite foreign-key constraint.

### Technical Attributes

| Attribute | Description |
|---|---|
| `source_updated_at` | Timestamp of the source-side economics record update |
| `loaded_at` | Warehouse load timestamp |

---

## Proposed dbt Structure

> **Review required before implementation.**

The current proposal uses staging → intermediate → marts, with a separate snapshot/history mechanism only for campaign lifecycle history.

```text
Raw Sources
    ↓
Staging
    ↓
Snapshot / History Tracking   ← campaign only
    ↓
Intermediate
    ↓
Marts
  ├── dimensions/
  │    └── dim_campaign
  └── facts/
       └── fct_campaign_economics
```

### Proposed Models

```text
dbt_project/
├── models/
│   ├── staging/
│   │   ├── stg_campaign.sql
│   │   └── stg_campaign_economics.sql
│   │
│   ├── intermediate/
│   │   ├── int_campaign_history.sql
│   │   └── int_campaign_economics.sql
│   │
│   └── marts/
│       ├── dimensions/
│       │   └── dim_campaign.sql
│       └── facts/
│           └── fct_campaign_economics.sql
│
└── snapshots/
    └── snap_campaign_history.sql
```

### Layer Responsibilities

**Staging**
- source-aligned renaming and casting
- basic null cleanup
- standardization of campaign channel and status values
- minimal business logic

**Snapshot / History**
- preserve campaign-status changes when the source only exposes current state
- use campaign status as the V1 SCD2 change driver

**Intermediate**
- translate snapshot technical fields into reusable campaign-history logic
- prepare standardized campaign economics before mart exposure

**Marts**
- expose the consumer-facing dimension and fact models that form the Campaign Intelligence data product

---

## Confirmed V1 Decisions

- Campaign Intelligence contains campaign setup and economics, not campaign performance.
- `dim_campaign` is historical and uses SCD2-style status versioning.
- `campaign_status` is the V1 SCD2 change driver.
- Actual campaign start/end are timestamps and are assumed fixed once established.
- `fct_campaign_economics` has one row per campaign and does not maintain history.
- Campaign budget is finalized before launch.
- `budget_effective_timestamp` equals the campaign actual start timestamp.
- The fact-to-dimension relationship is modeled as a campaign ID + effective-time as-of relationship.

## Open Decisions

The following items remain for the dbt-structure review:

1. Confirm whether a dbt snapshot is the preferred mechanism once the raw campaign source behavior is defined.
2. Confirm whether both intermediate models add sufficient reusable logic or whether either can be simplified.
3. Define the exact source-to-model mapping and source requirements.

## Next Step

Review the proposed dbt structure, then define the raw source requirements and source-to-model mapping needed to build `dim_campaign` and `fct_campaign_economics`.
