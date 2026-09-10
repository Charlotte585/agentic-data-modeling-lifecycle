# Agentic Data Modeling Lifecycle

> **Status:** Data product design + dbt foundation in progress

A reusable framework for turning ambiguous business requirements and heterogeneous source data into governed, validated data products through semantic modeling, dbt, and agent-assisted development.

## Project Thesis

The core problem is not generating SQL with AI. It is translating business intent into reliable data products.

```text
Business Need
    ↓
Source Semantics
    ↓
Grain & Modeling Decisions
    ↓
dbt Implementation
    ↓
Validation
    ↓
Reusable Data Products
    ↓
Agentic Assistance
```

## Customer Ad Engagement V1

The primary implementation models customer-side ad engagement across a focused funnel:

```text
impression → view → click
```

Conversion and transaction outcomes are explicitly out of scope for V1.

### Confirmed Raw Sources

- `raw_ad_events` — ad interaction events
- `raw_identity_map` — visitor-to-customer/account identity states
- `raw_ad_metadata` — versioned ad and campaign context

### dbt Model Flow

```text
raw → staging → intermediate → marts
```

This structure keeps source cleanup, identity and temporal modeling, and reusable analytical outputs separated and testable.
