# Data Product Modeling Framework

> **Status:** Planning / v0.2  
> A reusable framework for translating business needs into well-designed, validated data models, with dbt as the reference implementation layer and AI used selectively for planning, review, and automation.

## Project Thesis

The value of this project is not simply generating code with AI. The goal is to make an end-to-end data-product modeling process explicit, reusable, and executable.

A strong data model starts before SQL. It requires understanding:

- what business problem the data product needs to solve,
- what downstream decision, analytics workflow, or model will consume it,
- what the final data product should contain and at what grain,
- which source data is required and how those sources relate,
- how the model should be structured for reuse and maintainability,
- how the design should be implemented and tested in dbt,
- and how the same methodology can transfer to a different business context.

This project therefore treats data modeling as a **business-to-data reasoning problem**, not only a SQL-generation problem.

The core workflow is:

```text
Business Need
     ↓
Data Product Definition
     ↓
Source & Modeling Design
     ↓
ModelSpec
     ↓
dbt Implementation
     ↓
Validation & Engineering Workflow
     ↓
Validated Data Model
     ↓
Agentic Assistance & Automation
```

The framework is designed to demonstrate both **data-product judgment** and **implementation depth**. The modeling methodology comes first; AI is added only where it can automate repeatable reasoning or review steps.

---

## What This Project Demonstrates

### Business-first data modeling

The project begins with the business problem and the expected downstream use of the data product rather than with a dataset or a technology choice.

### Reusable modeling methodology

Business requirements, source metadata, modeling decisions, and implementation rules are represented through explicit contracts instead of being embedded only in ad hoc SQL or prompts.

### Production-style dbt implementation

The reference implementation goes beyond basic SQL models and covers layered modeling, materializations, tests, reusable macros, documentation, and incremental processing.

### Validation as part of modeling

A model is not considered complete simply because SQL executes. Grain, relationships, assumptions, data-quality rules, and dbt tests are part of the modeling contract.

### AI as an accelerator, not the source of judgment

Agents can help draft plans, review artifacts, diagnose failures, and automate repeatable steps after the underlying methodology and reference implementation are established.

### Transferability across business contexts

The framework should work across multiple domains without changing its core modeling principles.

---

## Core Concepts

### `BusinessIntent`

Defines why the model exists and how it will be used.

Example:

```yaml
objective: measure customer engagement and transaction performance
entity: customer
use_case: customer analytics
required_outputs:
  - customer_id
  - engagement_metrics
  - transaction_metrics
  - customer_attributes
```

### `SourceMetadata`

Describes the source data available to satisfy the business requirement.

Typical metadata includes:

- source table and platform,
- columns and data types,
- grain,
- candidate primary keys,
- candidate foreign keys,
- join cardinality,
- timestamp fields,
- null and uniqueness patterns,
- freshness assumptions.

### `ModelSpec`

Captures the modeling decisions before implementation.

Example:

```yaml
model_name: customer_performance
purpose: provide a reusable customer-level analytics model

grain:
  - customer_id

sources:
  - customers
  - orders
  - engagement_events

layers:
  staging:
    - stg_customers
    - stg_orders
    - stg_engagement_events
  intermediate:
    - int_customer_orders
    - int_customer_engagement
  marts:
    - mart_customer_performance

validation:
  - customer_id is not null
  - customer_id is unique at the final grain
  - order relationships are valid
```

`ModelSpec` is the central bridge between business and data-modeling decisions and their physical dbt implementation.

---

# End-to-End Build Plan

## Phase 1 — Business & Data Product Definition

**Goal:** Start from the business problem and define the data product before choosing implementation details.

Key questions:

- What business problem are we solving?
- What decision or downstream use case will consume this data?
- What should the final data product contain?
- What is the target grain?
- Which outputs are required versus optional?

Deliverables:

- `BusinessIntent`,
- expected output contract,
- target grain,
- key business definitions,
- assumptions and constraints.

**Exit criteria:** The desired data product can be explained without referring to implementation code.

---

## Phase 2 — Source & Modeling Design

**Goal:** Translate the desired output into a clear source and modeling plan.

Key activities:

- identify the required entities,
- map required outputs to available source data,
- identify authoritative sources,
- define source grains,
- define primary and foreign keys,
- evaluate join cardinality,
- define staging, intermediate, and mart boundaries,
- document assumptions and reusable logic.

Deliverables:

```text
BusinessIntent
      +
SourceMetadata
      ↓
   ModelSpec
```

The initial implementation may use deterministic profiling for basic schema statistics, but the emphasis of this phase is modeling judgment rather than building a large schema-discovery system.

**Exit criteria:** The proposed model can be reviewed before any dbt model is written.

---

## Phase 3 — dbt Reference Implementation

**Goal:** Implement the approved `ModelSpec` as a production-style dbt project.

This is the primary implementation and learning layer of the project.

### Project structure

```text
raw sources
    ↓
staging
    ↓
intermediate
    ↓
marts
```

### dbt concepts to implement

- `source()` and source definitions,
- `ref()` and dependency management,
- staging models,
- intermediate models,
- mart models,
- `view`, `table`, `ephemeral`, and `incremental` materializations,
- incremental loading strategies,
- `unique_key` handling,
- late-arriving or updated records where relevant,
- `schema.yml`,
- `not_null`, `unique`, `relationships`, and `accepted_values` tests,
- singular tests,
- at least one reusable generic test,
- macros for reusable transformation logic,
- model and column documentation,
- `dbt docs generate` and lineage inspection.

### Reference-first approach

The first complete dbt implementation will be designed and reviewed as a human reference implementation before agentic generation is introduced.

This creates a benchmark for evaluating whether automated implementations make appropriate modeling decisions.

**Exit criteria:**

```bash
dbt build
dbt docs generate
```

complete successfully and the resulting model satisfies the agreed `ModelSpec`.

---

## Phase 4 — Validation & Engineering Workflow

**Goal:** Make model development reproducible and testable through an engineering workflow.

Validation will cover both dbt execution and modeling expectations.

### dbt validation

```bash
dbt parse
dbt build
dbt test
```

### Supporting Python tests

Use `pytest` for framework-level logic such as:

- contract validation,
- ModelSpec parsing,
- deterministic utility functions,
- generated configuration checks.

### Lightweight CI

GitHub Actions will run relevant checks on pull requests:

```text
Pull Request
     ↓
Install dependencies
     ↓
pytest
     ↓
dbt parse
     ↓
dbt build
     ↓
PASS / FAIL
```

The goal is to understand and demonstrate a practical analytics-engineering CI workflow without turning the project into a full deployment platform.

**Exit criteria:** A pull request cannot be considered valid without automated model and code checks passing.

---

## Phase 5 — Agentic Assistance & Automation

**Goal:** Automate repeatable parts of the modeling workflow after the methodology and reference implementation are established.

Potential agent roles:

### Modeling Assistant

```text
BusinessIntent
+
SourceMetadata
      ↓
Draft ModelSpec
```

### dbt Implementation Assistant

```text
Approved ModelSpec
      ↓
Suggested dbt implementation
```

### Reviewer

Review:

- grain consistency,
- join logic,
- model layering,
- missing tests,
- incremental strategy,
- documentation quality.

### Repair Assistant

```text
dbt or validation failure
      ↓
Specific diagnostic evidence
      ↓
Targeted correction
      ↓
Re-run deterministic validation
```

The agent layer should not replace the deterministic execution and validation system. Its purpose is to accelerate a methodology that has already been defined.

**Exit criteria:** Automated suggestions can be compared against the human reference implementation and validated through the same dbt and testing workflow.

---

## Phase 6 — Cross-Business Reusability

**Goal:** Demonstrate that the same modeling process can be transferred to different business situations.

The project will use one primary end-to-end case and a small number of lighter transfer cases.

### Primary case

A complete workflow including:

```text
Business Problem
      ↓
Data Product Definition
      ↓
Source Design
      ↓
ModelSpec
      ↓
dbt Implementation
      ↓
Validation
      ↓
Agentic Review / Automation
```

### Transfer case examples

Potential domains include:

- product analytics: users, events, sessions,
- commerce: customers, orders, products,
- subscription: accounts, subscriptions, payments, usage.

The secondary cases do not need to reproduce the entire implementation. Their purpose is to test whether the same contracts and modeling methodology remain useful under a different business problem.

**Exit criteria:** The framework can represent and reason about multiple business contexts without changing the core modeling approach.

---

## Technical Stack

Initial implementation:

- **Python** — framework utilities, contracts, testing, and automation,
- **Pydantic** — structured modeling contracts,
- **DuckDB** — local execution environment,
- **dbt Core + dbt-duckdb** — reference transformation and modeling layer,
- **pytest** — Python-level testing,
- **GitHub Actions** — lightweight CI,
- **LLM / agent layer** — modeling assistance, review, and repair after the reference workflow is established.

The initial stack is intentionally local and reproducible. Additional warehouses or execution platforms can be introduced later without changing the core modeling methodology.

---

## Proposed Repository Structure

```text
data-product-modeling-framework/
│
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── src/
│   └── data_product_modeling/
│       ├── contracts/
│       │   ├── business_intent.py
│       │   ├── source_metadata.py
│       │   └── model_spec.py
│       │
│       ├── modeling/
│       ├── validation/
│       ├── automation/
│       └── cli/
│
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
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

- [ ] Define the primary business use case and expected data product
- [ ] Define `BusinessIntent`, `SourceMetadata`, and `ModelSpec`
- [ ] Set up Python, DuckDB, dbt, and pytest
- [ ] Build the human-designed reference dbt implementation
- [ ] Add dbt tests, macros, incremental logic, and documentation
- [ ] Add Python validation and GitHub Actions CI
- [ ] Add agent-assisted ModelSpec planning and review
- [ ] Add agent-assisted dbt implementation and targeted repair
- [ ] Validate the framework against additional business contexts
- [ ] Package the project for portfolio presentation

---

## How Success Will Be Evaluated

The project is successful if it demonstrates that a business requirement can be translated into a reusable data model through a repeatable process and that the implementation can withstand both modeling review and automated validation.

Key evaluation dimensions include:

- clarity of the business-to-data reasoning,
- correctness of model grain and entity relationships,
- quality of dbt layering and dependency design,
- appropriate use of materializations and incremental logic,
- meaningful data tests and documentation,
- reproducible CI validation,
- usefulness of agentic automation without outsourcing core modeling judgment,
- transferability of the methodology to another business context.

---

## Downstream Continuation

The validated models produced here are intended to become the starting point for a separate downstream project focused on **ML feature engineering**.

That project will extend the same data-product mindset into:

```text
Validated Data Model
      ↓
Feature Requirements
      ↓
FeatureSpec
      ↓
Point-in-Time Feature Engineering
      ↓
Leakage Validation
      ↓
ML-Ready Dataset
```

Together, the two projects are intended to demonstrate the data foundation between a business problem and downstream analytics or machine-learning consumption.
