# Agentic Data Modeling Lifecycle

**Advertising data products built with Python, SQL, dbt, and DuckDB.**

This project explores how to turn business requirements and heterogeneous source data into reusable data products for analytics and downstream ML. The current implementation validates and loads synthetic sources, standardizes advertising data, and matches engagement events to the identity record valid at the time of each event.

**Business problem:** A visitor's identity and account status can change over time. Joining historical events to the latest identity record can misrepresent who the visitor was when the event occurred. This project makes event grain, temporal validity, and data quality explicit modeling decisions.

> **Status:** In development. Source validation, raw loading, three staging models, and event-time identity resolution are implemented. Ad metadata enrichment, sessionization, final marts, CI automation, and reusable agent workflows are planned.

## Start Here

- [Business context and reference case](examples/primary_case/README.md)
- [Customer Ad Engagement specification](examples/primary_case/customer_ad_engagement/data_product_spec.md)
- [Event-time identity resolution SQL](dbt%20project/models/intermediate/int_ad_events_identity_resolved.sql)
- [Model documentation and tests](dbt%20project/models/intermediate/intermediate.yml)
- [Local validation commands](#local-validation)

## What Is Implemented

| Component | Current implementation |
| --- | --- |
| Source data | Synthetic ad events, identity history, and advertising API payloads |
| Python | Source fixture validation, validation unit tests, and raw loading |
| dbt staging | Ad events, identity history, and versioned ad metadata |
| dbt intermediate | Event-time identity resolution using effective-date windows |
| Data quality | Event uniqueness, identity-history integrity, and ad configuration window checks |

## Example: Identity at the Time of the Event

Visitor `V200` is anonymous before February 1, 2025, and becomes a verified customer on that date. Visitor `V999` has no identity history record.

The table below shows **expected selected output**, derived from the checked-in [event fixtures](fixtures/ad_events.jsonl), [identity history](fixtures/identity_map.csv), and current SQL. It is an explanatory example, not a captured dbt run.

| Event | Event timestamp (UTC) | Visitor | Customer | Identity type | History matched | Identity resolved |
| --- | --- | --- | --- | --- | --- | --- |
| E004 | 2025-01-15 10:00:00 | V200 | NULL | anonymous | true | false |
| E006 | 2025-02-01 00:00:00 | V200 | C200 | verified_customer | true | true |
| E028 | 2025-09-01 13:00:00 | V999 | NULL | NULL | false | false |

The join uses an inclusive start and exclusive end: `event_timestamp >= effective_from` and `event_timestamp < effective_to`. The left join retains events without an identity match. History-window checks and event uniqueness tests guard against ambiguous matches and duplicate events.

## Data Product Design

The sections below describe the target data products and downstream uses; final marts and ML models are not yet implemented.

### 1. Customer Ad Engagement

**Purpose:** Build a detailed behavioral dataset describing how customers interact with digital ads.

The V1 funnel is:

```text
Impression → View → Click
```

The product preserves one row per engagement event and combines:

- customer / visitor identity
- session context
- campaign and ad context
- creative and placement information
- device and marketing channel
- event timestamp and interaction type

This product is selected because customer-level event data provides a flexible foundation for both analytics and machine-learning use cases.

**Downstream uses:**

- customer journey and funnel analysis
- engagement and drop-off analysis
- behavioral feature engineering
- recency / frequency / interaction-sequence features
- click or engagement propensity models
- audience segmentation

### 2. Campaign Intelligence

**Purpose:** Provide reusable campaign and advertising context with historical configuration changes preserved.

Representative outputs include:

- `dim_campaign`
- `fct_campaign_economics`

along with campaign, ad, and creative metadata used by the engagement product.

This product is separated from customer engagement because campaign configuration and economics have different grains and change patterns from behavioral events.

**Downstream uses:**

- campaign performance analytics
- campaign-level feature engineering
- campaign-informed forecasting models
- experiment and GTM measurement
- budget and channel analysis

## Why These Data Products

The two products represent complementary parts of the same business system:

```text
Campaign Intelligence
        ↓
What was configured and running?

Customer Ad Engagement
        ↓
How did customers respond?
```

Keeping them separate preserves their natural grains while allowing them to be combined for downstream analysis.

Together they provide the foundation for:

```text
Customer Behavior
        +
Campaign Context
        +
Historical Identity
        ↓
Feature Engineering
        ↓
ML-Ready Datasets
        ↓
Prediction / Forecasting / Experimentation
```

This also creates the upstream data foundation for a future ML Feature Engineering Lifecycle project focused on point-in-time feature construction, leakage prevention, training datasets, and model development.

## Reference Architecture

```text
Raw Sources
    ↓
Staging
    ↓
Intermediate
    ↓
Facts & Dimensions
    ↓
Reusable Data Products
```

## Technical Stack

- **dbt Core** — transformation and modeling
- **DuckDB** — local execution
- **SQL / Python** — data processing and validation
- **GitHub Actions** — planned CI automation
- **LLM / agents** — planned reusable workflows for implementation assistance, review, and targeted repair

## Current Implementation

Implemented: synthetic event, identity, and advertising API fixtures; Python fixture
validation and raw loading; three dbt staging models; event-time identity resolution;
and event-time ad metadata enrichment in `int_ad_events_enriched`, with temporal
integrity and event-preservation tests. Sessionization and the final marts remain
in development.

The enrichment model reuses `int_ad_events_identity_resolved` and left joins
`stg_ad_metadata` by `ad_id` and the half-open version window `[start, end)`.
It preserves unmatched events and all upstream event/identity fields, exposing
version campaign/creative IDs separately from the original event IDs.

## Local Validation

These commands assume Python dependencies, dbt Core with the DuckDB adapter, and the `agentic_data_modeling` dbt profile have already been configured. A complete bootstrap guide is still planned.

Run from the repository root:

```bash
python -m scripts.validate_source_fixtures
python -m unittest discover -s tests -p 'test_*.py'
python scripts/load_raw_data.py
cd "dbt project"
dbt build --select +int_ad_events_enriched
```

The fixture validator checks source payloads before ingestion. dbt tests check
modeled grains, identity history, and ad configuration windows after loading.
The enrichment checks compare input/output counts for every event_id and test
version boundaries, gaps, unmatched ads, and unchanged event/identity fields.
