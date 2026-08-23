# Agentic Data Modeling Lifecycle

> **Status:** Planning / v0.3  
> A reusable framework for translating business requirements and heterogeneous source data into well-designed, validated data products through structured modeling decisions, production-style dbt implementation, and agentic automation.

## Project Thesis

The value of this project is not simply generating code with AI. The goal is to make an end-to-end data-modeling lifecycle explicit, reusable, and executable.

A strong data product starts before SQL. It requires understanding:

- what business problem the data needs to solve,
- which downstream analytical or ML decisions it should support,
- which source systems and business semantics are required,
- how identities and grains differ across sources,
- how reusable models should be structured,
- how those decisions should be implemented and tested in dbt,
- and how the same lifecycle can transfer to other business contexts.

This project therefore treats data modeling as a **business-to-data reasoning problem**, not only a SQL-generation problem.

```text
Business Need
      ↓
Source Landscape & Semantics
      ↓
Identity & Modeling Decisions
      ↓
ModelSpec
      ↓
dbt Implementation
      ↓
Deterministic Validation
      ↓
Reusable Data Products
      ↓
Agentic Assistance & Automation
```

The modeling methodology comes first. AI is added where it can accelerate repeatable planning, review, and repair steps without replacing business judgment or deterministic validation.

---

## Primary Implementation Case

The primary example is **marketing- and digital-journey oriented**, while the framework itself remains domain-agnostic.

Customer journeys and marketing outcomes are commonly distributed across transaction systems, digital behavioral platforms such as Adobe Analytics, campaign metadata, and multiple customer or visitor identifiers. These sources operate at different grains, use different identities, and encode customer behavior through different event and measurement conventions.

The project demonstrates how to transform this heterogeneous source landscape into reusable data products that connect marketing activity, digital behavior, customer identity, and transaction outcomes.

### Raw Data Sources

#### 1. Transaction Data

Typical attributes:

- `transaction_id`
- customer or account identifier
- transaction timestamp
- transaction amount
- transaction status
- product / category
- transaction channel

Purpose: establish business outcomes such as purchases, revenue, and conversion.

#### 2. Digital Behavior & Interaction Data

Typical attributes:

- visitor identifier
- session identifier
- event identifier
- event timestamp
- page views
- page interactions
- product interactions
- navigation or funnel events

The primary example uses **Adobe Analytics / GA4-style behavioral telemetry** as the source pattern, without making the framework dependent on a specific vendor.

Purpose: reconstruct digital journeys and behavioral engagement.

#### 3. Campaign Details Metadata

Typical attributes:

- `campaign_id`
- campaign type / objective
- channel
- audience or segment
- creative / ad identifier
- start and end dates
- source / medium

Optional delivery facts such as impressions, clicks, and spend may be added when required by a downstream measurement use case.

Purpose: provide marketing and acquisition context.

#### 4. Identity Signals

Raw systems may expose different identifiers, for example:

```text
transaction system → customer_id
behavioral platform → visitor_id
session tracking    → session_id / device_id
campaign systems    → click_id / campaign_id
```

The project uses those signals to build an explicit identity-resolution layer rather than assuming the identifiers are already aligned.

Example modeled output:

```text
bridge_customer_identity

visitor_id
customer_id
valid_from
valid_to
match_type
```

Purpose: create trusted cross-source linkage while keeping source-system identities explicit.

#### 5. Measurement Taxonomy & Tracking Metadata

Examples:

- event definitions
- page or content taxonomy
- journey-stage definitions
- required event parameters
- conversion definitions
- campaign or interaction classification rules

Purpose: translate raw tracking events into consistent business semantics.

---

## Reusable Data Products

The primary case will produce several related data products rather than one oversized mart.

### Customer Journey & Engagement

Typical grain:

```text
visitor / customer × session
```

Combines identity, session timing, campaign context, engagement, journey stage, and conversion indicators.

### Campaign & Channel Performance

Typical grain:

```text
date × campaign × channel
```

Combines campaign attributes with downstream sessions, engagement, conversions, transactions, and revenue. Delivery metrics such as impressions, clicks, spend, CPA, or ROAS are included only when the source data supports them.

### Conversion & Transaction Outcomes

Typical grain:

```text
one row per transaction / conversion
```

Connects transaction outcomes with resolved identity, preceding digital behavior, session context, and relevant campaign context.

These data products share common foundation models such as:

```text
bridge_customer_identity
fct_digital_events
fct_sessions
fct_transactions
dim_campaign
dim_measurement_taxonomy
```

---

## Downstream Use Cases

The modeled data products are designed to support three distinct downstream use cases.

### 1. ML Modeling — Campaign-Informed Sales Forecasting

Use historical campaign activity, transaction outcomes, and time-dependent behavioral signals to build point-in-time-correct features for a downstream forecasting project.

A representative ML objective is:

> Forecast future transaction volume or sales while incorporating historical campaign and customer-behavior signals.

This use case becomes the bridge to the separate **ML Feature Engineering Lifecycle** project, where the focus shifts to feature specifications, observation windows, leakage prevention, and time-series model inputs.

### 2. Analytics Reporting — Customer Attrition & Journey Loss Analysis

Measure where customers disengage or are lost across the journey and how attrition varies by relevant dimensions such as:

- acquisition or interaction channel,
- geography,
- customer segment or available demographic attributes,
- journey stage,
- campaign exposure.

The purpose is not merely to calculate a churn rate, but to identify **which stages and dimensions are associated with customer loss**.

### 3. Analytics / Experimentation — GTM & Campaign Impact Analysis

Support go-to-market analysis for new campaigns, ads, or customer-acquisition strategies by defining measurable treatment and outcome data for experimentation.

Typical questions include:

- Did a new campaign improve conversion or acquisition?
- Which customer segments responded differently?
- Did downstream transaction behavior change after exposure?
- How should an A/B test be structured and evaluated using trusted campaign, behavioral, identity, and transaction data?

This use case connects the modeled data foundation to experimental design and statistical analysis rather than treating campaign reporting as simple descriptive aggregation.

---

## What This Project Demonstrates

### Business-first

Start from the decision and required data product, not from a dataset or SQL query.

### Semantic-aware

Model not only schemas and keys, but also identity, event meaning, measurement taxonomy, grain, and metric behavior.

### Implementation-backed

Translate explicit modeling decisions into production-style dbt models, tests, documentation, and CI.

### Agent-assisted, not agent-defined

Use agents to accelerate planning, review, and repair while keeping business semantics and validation explicit and deterministic.

### Transferable

The primary implementation is marketing-oriented, but the contracts and lifecycle are intended to transfer to other domains that require multi-source modeling and reusable data products.

---

## Core Concepts

### `BusinessIntent`

Defines why a data product exists, who will consume it, and which decisions it needs to support.

Example:

```yaml
name: marketing_customer_journey

objective: >
  Build reusable data products that connect campaign activity,
  digital behavior, customer identity, and transaction outcomes.

consumers:
  - marketing_analytics
  - customer_analytics
  - data_science

supported_use_cases:
  - campaign_informed_sales_forecasting
  - customer_attrition_analysis
  - gtm_campaign_impact_analysis
```

### `SourceMetadata`

Describes the physical and semantic characteristics of available source data.

Typical metadata includes:

- source table / system,
- columns and data types,
- grain,
- primary and foreign-key candidates,
- identifier semantics,
- join cardinality,
- timestamp fields,
- null and uniqueness patterns,
- freshness assumptions,
- business meaning of tracked events or attributes.

### `ModelSpec`

Captures modeling decisions before implementation.

A `ModelSpec` defines, for each target model:

- purpose,
- grain,
- source dependencies,
- identity strategy,
- transformations,
- model layer,
- materialization strategy,
- business rules,
- validation expectations.

`ModelSpec` is the bridge between business and modeling decisions and their physical dbt implementation.

---

# End-to-End Build Plan

## Phase 1 — Business & Data Product Definition

**Goal:** Define the business problem, source landscape, downstream consumers, and reusable data products before implementation.

Deliverables:

- primary business problem,
- raw source landscape,
- `BusinessIntent`,
- expected data products and grains,
- downstream analytical and ML use cases,
- key modeling decisions and assumptions.

**Exit criteria:** The intended data products and their business value can be explained without referring to implementation code.

---

## Phase 2 — Source & Modeling Design

**Goal:** Translate heterogeneous raw sources into an explicit modeling plan.

Key activities:

- profile physical source schemas,
- identify source grains and authoritative fields,
- interpret identity signals,
- map measurement taxonomy to business concepts,
- define relationships and join cardinalities,
- design identity-resolution logic,
- define staging, intermediate, foundation, and mart boundaries,
- document metric behavior and modeling assumptions,
- produce `SourceMetadata` and `ModelSpec` artifacts.

```text
BusinessIntent
      +
SourceMetadata
      +
Semantic / Identity Decisions
      ↓
   ModelSpec
```

**Exit criteria:** The proposed data products can be reviewed independently of dbt code.

---

## Phase 3 — dbt Reference Implementation

**Goal:** Implement the approved `ModelSpec` as a production-style dbt project.

Core model flow:

```text
raw sources
    ↓
staging
    ↓
intermediate / identity / semantic foundation
    ↓
facts & dimensions
    ↓
reusable marts / data products
```

Concepts to implement:

- `source()` and source definitions,
- `ref()` and dependency management,
- staging, intermediate, fact, dimension, and mart models,
- `view`, `table`, `ephemeral`, and `incremental` materializations where appropriate,
- incremental strategies and `unique_key` handling,
- late-arriving or updated records where relevant,
- `schema.yml`,
- `not_null`, `unique`, `relationships`, and `accepted_values` tests,
- singular tests,
- reusable generic tests,
- macros for reusable transformation logic,
- model and column documentation,
- dbt lineage and documentation generation.

### Reference-first approach

The first complete implementation is designed and reviewed as a human reference implementation before agentic generation is introduced.

**Exit criteria:**

```bash
dbt build
dbt docs generate
```

complete successfully and the modeled outputs satisfy the agreed `ModelSpec`.

---

## Phase 4 — Validation & Engineering Workflow

**Goal:** Make data-model development reproducible and testable through an engineering workflow.

Validation includes:

```bash
pytest
dbt parse
dbt build
dbt test
```

GitHub Actions will run relevant checks on pull requests.

Validation should cover not only whether SQL executes, but also:

- target-grain uniqueness,
- relationship integrity,
- identity-bridge consistency,
- transaction integrity,
- campaign / event classification rules,
- semantic assumptions encoded by the measurement taxonomy.

**Exit criteria:** Model changes are automatically checked against both technical and modeling expectations.

---

## Phase 5 — Agentic Assistance & Automation

**Goal:** Automate repeatable parts of the lifecycle after the methodology and reference implementation are established.

Potential agent roles:

```text
BusinessIntent + SourceMetadata
              ↓
       Draft ModelSpec
              ↓
        Model Review
              ↓
   Suggested dbt Changes
              ↓
 Deterministic Validation
              ↓
      Targeted Repair
```

Agents may assist with:

- drafting modeling plans,
- checking grain and join logic,
- reviewing identity decisions,
- identifying missing tests,
- reviewing materialization strategies,
- diagnosing validation failures,
- suggesting targeted corrections.

The agent layer does not decide whether validation passed; deterministic tools do.

**Exit criteria:** Agent-assisted outputs can be compared against the human reference implementation and validated through the same execution path.

---

## Phase 6 — Cross-Business Reusability

**Goal:** Demonstrate that the lifecycle can transfer beyond the primary marketing-oriented example.

The primary implementation will be completed end-to-end. Additional lightweight transfer cases can test the same contracts and methodology in other domains such as product analytics, commerce, subscription, or operational data products.

**Exit criteria:** The core lifecycle does not require domain-specific branching to represent a different business problem.

---

## Technical Stack

- **Python** — framework utilities, contracts, testing, and automation
- **Pydantic** — structured modeling contracts
- **DuckDB** — local execution environment
- **dbt Core + dbt-duckdb** — reference transformation and modeling layer
- **pytest** — Python-level testing
- **GitHub Actions** — lightweight CI
- **LLM / agent layer** — modeling assistance, review, and repair after the reference workflow is established

---

## Proposed Repository Structure

```text
agentic-data-modeling-lifecycle/
│
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── src/
│   └── agentic_data_modeling/
│       ├── contracts/
│       │   ├── business_intent.py
│       │   ├── source_metadata.py
│       │   └── model_spec.py
│       ├── modeling/
│       ├── validation/
│       ├── automation/
│       └── cli/
│
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   ├── dimensions/
│   │   ├── facts/
│   │   └── marts/
│   ├── macros/
│   ├── tests/
│   └── dbt_project.yml
│
├── examples/
│   ├── primary_case/
│   └── transfer_cases/
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── .github/
    └── workflows/
```

---

## Development Milestones

- [ ] Finalize the primary business use case and raw source landscape
- [ ] Define `BusinessIntent`, source contracts, and expected data products
- [ ] Define identity, taxonomy, and grain decisions
- [ ] Create `SourceMetadata` and `ModelSpec`
- [ ] Set up Python, DuckDB, dbt, and pytest
- [ ] Build the human-designed reference dbt implementation
- [ ] Add dbt tests, macros, incremental logic, and documentation
- [ ] Add Python validation and GitHub Actions CI
- [ ] Add agent-assisted ModelSpec planning and review
- [ ] Add agent-assisted dbt implementation and targeted repair
- [ ] Validate the lifecycle against additional business contexts
- [ ] Package the project for portfolio presentation

---

## How Success Will Be Evaluated

The project is successful if it demonstrates that heterogeneous source data and business requirements can be translated into reusable, validated data products through a repeatable modeling lifecycle.

Key evaluation dimensions include:

- clarity of business-to-data reasoning,
- correctness of source grain and entity relationships,
- explicit treatment of identity and measurement semantics,
- quality of dbt layering and dependency design,
- appropriate use of materializations and incremental logic,
- meaningful data tests and documentation,
- reproducible CI validation,
- usefulness of agentic automation without outsourcing core modeling judgment,
- transferability of the lifecycle to another business context.

---

## Downstream Continuation

The validated data products produced here become upstream inputs to a separate **ML Feature Engineering Lifecycle** project.

```text
Reusable Data Products
      ↓
Feature Requirements
      ↓
FeatureSpec
      ↓
Point-in-Time Feature Engineering
      ↓
Leakage Validation
      ↓
ML-Ready Time-Series Dataset
      ↓
Campaign-Informed Sales Forecasting
```

Together, the two projects demonstrate the data foundation between business requirements, analytical consumption, and downstream machine-learning modeling.
