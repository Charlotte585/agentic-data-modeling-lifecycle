# Customer Ad Engagement Data Product — Design Placeholder

> **Status:** Primary data product / design in progress

## Purpose

Provide a reusable customer-side view of advertising exposure, engagement, and downstream conversion behavior across campaigns.

The product is intended to support analysis of the customer journey from ad exposure through engagement and conversion while preserving campaign and identity context.

## Current Scope Direction

Primary behavioral concepts:

```text
ad exposure / impression
        ↓
click / engagement
        ↓
conversion
        ↓
optional downstream transaction
```

Campaign setup and economics remain in the supporting **Campaign Intelligence** data product rather than being duplicated here.

## Design Decisions Still Open

The following items will be defined next:

1. Core fact grain: impression-level versus normalized event-level modeling
2. Business attributes and technical metadata
3. Relationship to campaign and identity models
4. Raw public source selection and semantic mapping
5. Staging, intermediate, and mart structure
6. Conversion versus transaction boundary
7. Data-quality and validation rules

No final schema or dbt implementation is locked in this document yet.
