# Primary Implementation Case — Customer-Side Advertising Engagement

The primary implementation case is now centered on customer-side advertising engagement rather than merchant-side campaign management.

The business flow is intentionally broad enough to represent an advertising platform where merchants or advertisers run campaigns and customers interact with promoted content:

```text
Advertiser / Merchant
        ↓
Advertising Platform
        ↓
Ad exposure / impression
        ↓
Customer engagement
        ↓
Click / conversion
        ↓
Optional downstream transaction outcome
```

The implementation will emphasize reusable customer-engagement modeling, including event grain, campaign context, identity, temporal relationships, conversion linkage, and downstream analytical or ML readiness.

## Data Product Hierarchy

### 1. Customer Ad Engagement — Primary

The primary data product will model customer-side advertising exposure and engagement behavior. Its detailed grain, schema, and dbt design are the next modeling decisions to be completed.

### 2. Campaign Intelligence — Supporting

Provides reusable campaign setup, lifecycle, and economics context through `dim_campaign` and `fct_campaign_economics`. Campaign performance metrics are intentionally excluded from this product.

### 3. Conversion / Transaction Outcomes — Downstream

Represents downstream conversion and, where source data permits, transaction outcomes connected to preceding customer engagement. The final boundary and schema remain to be designed.

## Raw Source Direction

The preferred source strategy is to use real public customer-engagement data where it provides valid event semantics, and use purpose-built synthetic fixtures only where public data cannot provide required campaign or commercial context.

Candidate source categories are:

1. Ad exposure and engagement events
2. Campaign metadata
3. Identity / customer signals
4. Conversion or transaction outcomes
5. Measurement taxonomy and event definitions

The exact public datasets and source-to-model mappings are not yet locked.

## Design Principle

The data products should be driven by business semantics and downstream reuse rather than by the shape of a convenient public dataset. Public source data may inform or populate the implementation, but it should not redefine the intended business entities or grains without an explicit modeling decision.
