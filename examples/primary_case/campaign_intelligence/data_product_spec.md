# Campaign Intelligence Data Product — V1 Design Spec

> **Status:** Draft for review  
> This document captures the current agreed design decisions for the Campaign Intelligence data product. The dbt structure is proposed and should be reviewed before implementation.

## Product Scope

Campaign Intelligence focuses on reusable campaign setup and economics information. It does **not** include campaign performance outcomes such as impressions, clicks, conversions, revenue, spend efficiency, CPA, or ROAS.

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

Represent campaign setup and lifecycle state while preserving historical campaign status changes for downstream time-series and point-in-time analysis.

### Grain

One row per campaign × effective campaign version.

### Business Attributes

| Attribute | Description |
|---|---|
| `campaign_id` | Business identifier for the campaign |
| `campaign_channel` | Campaign delivery channel |
| `campaign_desired_start_date` | Planned campaign start date |
| `campaign_desired_end_date` | Planned campaign end date |
| `campaign_actual_start_date` | Actual campaign start date |
| `campaign_actual_end_date` | Actual campaign end date |
| `campaign_status` | Campaign lifecycle status: `live`, `freeze`, or `inactive` |

### History Strategy

`dim_campaign` will preserve campaign history using an SCD Type 2-style design.

The primary tracked changes are:

- `campaign_status`
- `campaign_actual_start_date`
- `campaign_actual_end_date`

These attributes are related to campaign lifecycle execution and may change as a campaign moves between inactive, live, and frozen states.

The following attributes are currently treated as setup context rather than primary historical-change drivers:

- `campaign_channel`
- `campaign_desired_start_date`
- `campaign_desired_end_date`

This decision can be revisited if the source data or business requirements show that planned setup values require versioned history.

### Technical Attributes

| Attribute | Description |
|---|---|
| `campaign_version_key` | Surrogate primary key for each historical campaign version |
| `valid_from` | Timestamp/date when the version becomes effective |
| `valid_to` | Timestamp/date when the version stops being effective |
| `is_current` | Indicates the current campaign version |
| `source_updated_at` | Timestamp of the source-side update |
| `loaded_at` | Warehouse load timestamp |

---

## `fct_campaign_economics`

### Purpose

Represent campaign-level economics and funding configuration without mixing in downstream campaign performance outcomes.

### Business Attributes

| Attribute | Description |
|---|---|
| `campaign_id` | Business identifier for the campaign |
| `campaign_budget_amount` | Campaign budget amount |
| `budget_currency` | Currency associated with the budget |
| `budget_type` | Budget basis, such as lifetime, daily, or another defined period |

### Grain and History

The final fact-table grain and history strategy are intentionally **TBD** until the budget source behavior is confirmed.

The key design question is whether campaign budgets are immutable or can be revised over time. If revised budgets must be preserved, the fact will require an effective-period history design.

### Technical Attributes

Technical keys and effective-period fields are **TBD** pending the final grain decision and the relationship strategy between `fct_campaign_economics` and the historical `dim_campaign`.

---

## Proposed dbt Structure

> **Review required before implementation.**

The current proposal uses a three-layer modeling pattern with a separate snapshot/history mechanism for campaign lifecycle history.

```text
Raw Sources
    ↓
Staging
    ↓
Snapshot / History Tracking
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
- preserve changes in campaign lifecycle state when the source only exposes current state
- track campaign status and related actual start/end-date changes

**Intermediate**
- translate snapshot technical fields into reusable business-facing history logic
- standardize campaign economics before mart exposure

**Marts**
- expose the consumer-facing dimensional and fact models that form the Campaign Intelligence data product

---

## Open Decisions

The following items should be reviewed before implementation:

1. Confirm whether planned dates (`campaign_desired_start_date`, `campaign_desired_end_date`) should remain static context or become SCD2-tracked fields.
2. Confirm whether campaign budgets can change over time and therefore require history.
3. Define the final grain of `fct_campaign_economics`.
4. Decide whether `fct_campaign_economics` should join directly to `campaign_version_key` or use campaign ID plus effective-time logic.
5. Confirm whether dbt snapshot is necessary based on the raw source's ability to provide historical campaign state.

## Next Step

After this design is reviewed, define the raw source requirements and source-to-model mapping needed to build `dim_campaign` and `fct_campaign_economics`.