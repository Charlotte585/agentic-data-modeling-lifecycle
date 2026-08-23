# Agentic Data Modeling Assistant

> **Status:** Planning / v0.1  
> A reusable framework for turning business or ML intent into structured, executable, and validated data models.

## Why this project

Data modeling is more than SQL generation. In real analytics and machine-learning workflows, the difficult work is usually deciding:

- what the target grain should be,
- which source entities are relevant,
- how tables should join,
- which intermediate models are needed,
- how metrics or features should be defined,
- what temporal constraints apply,
- how the resulting model should be validated and documented.

This project treats data modeling as a **structured reasoning problem**.

The goal is to build a domain-agnostic assistant that converts:

**Business Intent + Source Metadata + Modeling Policies**

into:

**Model Specification → Executable Models → Validation → Documentation**

AI agents are used where reasoning is useful, while deterministic tools are used for profiling, execution, and validation.

---

## Design Principles

1. **Domain-agnostic by design**  
   The core framework should not depend on a single dataset, company, or business domain.

2. **Model specification before code generation**  
   The system should create a structured `ModelSpec` before generating SQL or dbt models.

3. **Deterministic checks before AI interpretation**  
   Row counts, null rates, uniqueness, cardinality, schema inspection, and execution results should come from deterministic tools.

4. **AI for reasoning, not for pretending validation passed**  
   Generated models must be compiled, executed, and tested.

5. **Human-readable and machine-readable outputs**  
   Modeling decisions should be inspectable, versionable, and reusable.

6. **Policy-driven modeling**  
   Modeling conventions and quality expectations should be explicit rather than embedded only in prompts.

7. **Portable architecture**  
   The framework should be extensible to additional databases, transformation engines, and business use cases.

---

## Conceptual Architecture

```text
                    ┌──────────────────────┐
                    │   Business Intent    │
                    └──────────┬───────────┘
                               │
┌────────────────────┐         │         ┌────────────────────┐
│   Source Metadata  │─────────┼────────▶│  Modeling Engine   │
└────────────────────┘         │         └─────────┬──────────┘
                               │                   │
┌────────────────────┐         │                   ▼
│  Modeling Policies │─────────┘               ModelSpec
└────────────────────┘                             │
                                                  │
                              ┌───────────────────┼───────────────────┐
                              ▼                   ▼                   ▼
                         Model Compiler      Validation Engine    Documentation
                              │                   │
                              └──────────┬────────┘
                                         ▼
                                  Execution Layer
                                         │
                                    PASS / FAIL
                                         │
                                         ▼
                                  Review / Repair
```

---

## Core Inputs

### 1. Business Intent

A structured description of what the model needs to support.

Examples:

```yaml
objective: measure user activation
entity: user
requirements:
  - activation must occur within 7 days of signup
  - activation requires at least one qualifying event
```

or:

```yaml
objective: create point-in-time-correct features for churn prediction
entity: customer
prediction_window_days: 30
```

### 2. Source Metadata

Schema and profiling information describing available source data.

Potential metadata includes:

- table names,
- columns and data types,
- row counts,
- null rates,
- uniqueness ratios,
- candidate primary keys,
- candidate foreign keys,
- join cardinalities,
- timestamp fields,
- representative sample values.

### 3. Modeling Policies

Reusable rules that constrain modeling decisions.

Example:

```yaml
modeling_rules:
  require_grain_definition: true
  require_primary_key: true
  enforce_staging_layer: true
  prohibit_future_data_for_features: true

quality_rules:
  require_not_null_primary_key: true
  require_unique_primary_key: true
  validate_relationships: true
```

---

## Core Abstraction: `ModelSpec`

The main intermediate artifact is a structured model specification.

Example:

```yaml
model_name: user_activation

purpose: >
  Measure whether a user reaches the activation definition
  within seven days of signup.

grain:
  - user_id

sources:
  - users
  - events

models:
  - stg_users
  - stg_events
  - int_user_activation_events
  - mart_user_activation

outputs:
  - activation_flag
  - activation_timestamp
  - days_to_activation

validation:
  - user_id is not null
  - user_id is unique at the target grain
  - activation_timestamp is not before signup_timestamp
```

The `ModelSpec` separates **modeling decisions** from **implementation details**.  
Compilers can later translate the same specification into dbt, SQL, or other execution targets.

---

# End-to-End Build Plan

## Phase 0 — Project Contract and Evaluation Criteria

**Goal:** Define what the framework is responsible for before implementing agents.

Deliverables:

- project scope and non-goals,
- initial `BusinessIntent` schema,
- initial `ModelingPolicy` schema,
- initial `ModelSpec` schema,
- definition of a valid modeling plan,
- evaluation rubric for generated models.

Initial evaluation dimensions:

- correct target grain,
- appropriate source selection,
- valid join relationships,
- sensible model decomposition,
- correct time-window logic,
- absence of feature leakage,
- executable generated code,
- passing data-quality checks,
- useful documentation.

**Exit criteria:** A modeling proposal can be evaluated independently of whether an LLM generated it.

---

## Phase 1 — Project Foundation

**Goal:** Create a reproducible local development environment.

Initial stack:

- Python
- Pydantic
- DuckDB
- dbt Core + dbt-duckdb
- pytest

Deliverables:

- Python project configuration,
- initial package structure,
- dbt project,
- local DuckDB environment,
- test framework,
- configuration management,
- sample fixture data.

**Exit criteria:**

```bash
pytest
dbt debug
```

both succeed.

---

## Phase 2 — Metadata and Schema Intelligence

**Goal:** Convert physical source data into reusable structured metadata.

Build deterministic profiling utilities for:

- schema discovery,
- row counts,
- null rates,
- distinct counts,
- uniqueness ratios,
- numeric and timestamp ranges,
- candidate keys,
- candidate relationships,
- table cardinality.

Then add a reasoning layer that interprets the deterministic profile to infer:

- probable table grain,
- business entities,
- likely relationships,
- relevant source tables,
- modeling risks.

Deliverables:

```text
Source Data
    ↓
Deterministic Profiler
    ↓
SourceMetadata
    ↓
Schema Intelligence
```

**Exit criteria:** Multiple unrelated source schemas can be represented through the same metadata contract.

---

## Phase 3 — Modeling Planner

**Goal:** Convert business intent, source metadata, and policies into a `ModelSpec`.

The planner should reason about:

- target grain,
- source relevance,
- entity relationships,
- join paths,
- staging / intermediate / mart decomposition,
- dimensions and measures,
- feature definitions,
- temporal windows,
- target definitions,
- quality requirements,
- potential leakage.

Initial workflow:

```text
BusinessIntent
      +
SourceMetadata
      +
ModelingPolicy
      ↓
Modeling Planner
      ↓
ModelSpec
```

Add a separate reviewer step that critiques the proposed specification before implementation.

Reviewer checks:

- grain consistency,
- many-to-many join risks,
- unnecessary complexity,
- ambiguous definitions,
- temporal correctness,
- feature leakage,
- missing validation rules.

**Exit criteria:** The planner produces a valid structured specification rather than free-form prose or raw SQL.

---

## Phase 4 — Model Compiler

**Goal:** Translate `ModelSpec` into executable artifacts.

Initial compiler target: **dbt**

Generate:

- staging models,
- intermediate models,
- marts / feature models,
- `schema.yml`,
- data tests,
- model descriptions,
- column descriptions.

Architecture:

```text
ModelSpec
    ↓
dbt Compiler
    ↓
SQL + YAML + Tests + Documentation
```

Future compiler targets may include:

- generic SQL,
- PySpark transformations,
- feature definitions,
- semantic-layer configuration.

**Exit criteria:** Generated dbt artifacts compile against the provided source environment.

---

## Phase 5 — Validation Engine

**Goal:** Validate the model structurally, semantically, and operationally.

### Structural validation

- required primary keys,
- target-grain uniqueness,
- null checks,
- relationship integrity,
- join cardinality.

### Semantic validation

- grain consistency across transformations,
- metric and feature definitions,
- temporal constraints,
- model-layer policies.

### ML-oriented validation

- feature timestamps do not exceed snapshot timestamps,
- prediction windows are isolated from feature windows,
- target leakage checks,
- snapshot consistency.

### Execution validation

```bash
dbt parse
dbt run
dbt test
```

Validation results should be structured and machine-readable.

**Exit criteria:** The framework can distinguish "SQL runs" from "the model satisfies its modeling contract."

---

## Phase 6 — Review and Repair Loop

**Goal:** Use concrete validation evidence to repair failed artifacts.

Workflow:

```text
Generated Model
      ↓
Deterministic Validation
      ↓
Structured Failure
      ↓
Repair Agent
      ↓
Updated Model / ModelSpec
      ↓
Validation
```

The repair process should:

- receive specific validation evidence,
- avoid rewriting unaffected components,
- record what changed and why,
- retry only up to a configurable limit,
- surface unresolved issues to the user.

**Exit criteria:** At least several intentionally constructed failure cases can be detected and repaired or clearly escalated.

Example failure cases:

- nonexistent column,
- incorrect join key,
- duplicate target grain,
- orphan foreign key,
- invalid time window,
- feature leakage,
- failed dbt test.

---

## Phase 7 — Cross-Domain Examples

**Goal:** Demonstrate that the framework is not tied to one Kaggle dataset or business domain.

Keep example datasets intentionally small. They exist to test the framework, not to become the project itself.

### Example A — Product Analytics

Sources:

```text
users
events
```

Intent:

> Build a seven-day user activation model.

Demonstrates:

- behavioral modeling,
- event logic,
- time-window reasoning,
- analytics marts.

### Example B — Commerce / Dimensional Modeling

Sources:

```text
customers
orders
order_items
products
```

Intent:

> Build a reusable customer performance mart.

Demonstrates:

- dimensional modeling,
- entity relationships,
- measures and dimensions,
- reusable semantic definitions.

### Example C — ML Feature Modeling

Sources:

```text
customers
transactions
events
```

Intent:

> Build point-in-time-correct features for a future customer outcome.

Demonstrates:

- ML-ready data,
- snapshot modeling,
- feature windows,
- leakage prevention.

**Exit criteria:** The same core interfaces and modeling engine work across all three examples without domain-specific branching in the core framework.

---

## Phase 8 — Portfolio Hardening

**Goal:** Make the repository understandable and credible to someone who did not build it.

Add:

- architecture diagram,
- example CLI runs,
- sample `BusinessIntent`,
- sample `ModelSpec`,
- generated dbt output,
- validation report,
- repair-loop example,
- automated tests,
- GitHub Actions CI,
- clear limitations,
- roadmap.

Potential CLI:

```bash
modeling-assistant plan \
  --intent examples/product_activation/intent.yml \
  --sources examples/product_activation/sources.yml \
  --policies config/modeling_policies.yml
```

Potential build command:

```bash
modeling-assistant build \
  --spec outputs/model_spec.yml \
  --target dbt
```

---

## Proposed Repository Structure

```text
agentic-data-modeling-assistant/
│
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
│
├── src/
│   └── modeling_assistant/
│       ├── contracts/
│       │   ├── business_intent.py
│       │   ├── source_metadata.py
│       │   ├── modeling_policy.py
│       │   └── model_spec.py
│       │
│       ├── profiling/
│       ├── intelligence/
│       ├── planning/
│       ├── review/
│       ├── compilers/
│       │   └── dbt/
│       ├── validation/
│       ├── repair/
│       └── cli/
│
├── dbt_project/
│
├── config/
│   └── modeling_policies.yml
│
├── examples/
│   ├── product_activation/
│   ├── dimensional_mart/
│   └── ml_features/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── scenarios/
│
└── docs/
    └── architecture/
```

---

## What This Project Is Not

This project is **not** intended to be:

- a solution optimized for one Kaggle dataset,
- a generic text-to-SQL chatbot,
- an LLM wrapper that assumes generated SQL is correct,
- a replacement for data-modeling judgment,
- a production data platform for every warehouse from day one.

The initial objective is narrower:

> Build a reusable framework that makes data-modeling reasoning explicit, generates executable models from structured specifications, and verifies those models through deterministic validation.

---

## Initial Milestones

- [ ] Define contracts: `BusinessIntent`, `SourceMetadata`, `ModelingPolicy`, `ModelSpec`
- [ ] Set up Python + DuckDB + dbt development environment
- [ ] Implement deterministic schema profiler
- [ ] Implement schema-intelligence layer
- [ ] Implement modeling planner
- [ ] Implement ModelSpec reviewer
- [ ] Implement dbt compiler
- [ ] Implement structural and semantic validation
- [ ] Implement execution feedback and repair loop
- [ ] Add three cross-domain examples
- [ ] Add CI and portfolio-quality documentation

---

## Long-Term Extensions

Possible future extensions include:

- Snowflake and BigQuery metadata connectors,
- dbt manifest ingestion,
- semantic-layer compilation,
- PySpark compiler,
- model lineage visualization,
- human approval checkpoints,
- policy packs for analytics vs. ML modeling,
- model-plan evaluation benchmarks,
- multiple LLM-provider adapters.

The core abstraction should remain stable even as execution targets and reasoning implementations evolve.
