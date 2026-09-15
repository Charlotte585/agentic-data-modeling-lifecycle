# Agentic Data Modeling Lifecycle

> **Status:** Reference data product design and dbt implementation in progress

An end-to-end data modeling project that translates business requirements and heterogeneous source data into reusable, validated data products.

The project covers the lifecycle from source semantics and dimensional modeling to dbt implementation, testing, and eventually agent-assisted development.

```text
Business Requirements
        ↓
Source Semantics & Modeling Decisions
        ↓
dbt Transformation
        ↓
Validated Data Products
        ↓
Analytics / Feature Engineering / ML
```

## Data Products

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
- **GitHub Actions** — CI
- **LLM / agents** — implementation assistance, review, and targeted repair

