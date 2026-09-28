#!/usr/bin/env python3
"""Validate synthetic upstream fixtures before loading them into DuckDB.

These checks cover source payload quality, not downstream identity resolution.
Intentionally unmatched visitors and ads remain valid test scenarios.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EVENT_TYPES = {"impression", "view", "click"}
REQUIRED_EVENT_IDS = (
    "event_id", "visitor_id", "campaign_id", "ad_id", "creative_id", "placement_id"
)


def validate_ad_events(records: Iterable[Mapping[str, Any]]) -> dict[str, list[str]]:
    """Return event IDs (or row labels) for source-level event violations."""
    issues: dict[str, list[str]] = {
        "invalid_event_type": [],
        "missing_required_id": [],
        "missing_device_type": [],
        "duplicate_event_id": [],
    }
    seen_event_ids: set[str] = set()
    for row_number, event in enumerate(records, start=1):
        raw_id = event.get("event_id")
        event_id = raw_id.strip() if isinstance(raw_id, str) else ""
        label = event_id or f"<row {row_number}>"

        event_type = event.get("raw_event_type")
        if not isinstance(event_type, str) or event_type.strip().lower() not in ALLOWED_EVENT_TYPES:
            issues["invalid_event_type"].append(label)
        if any(not isinstance(event.get(key), str) or not event[key].strip() for key in REQUIRED_EVENT_IDS):
            issues["missing_required_id"].append(label)
        device_type = event.get("device_type")
        if not isinstance(device_type, str) or not device_type.strip():
            issues["missing_device_type"].append(label)
        if event_id:
            if event_id in seen_event_ids:
                issues["duplicate_event_id"].append(label)
            seen_event_ids.add(event_id)
    return issues


def find_duplicate_current_identities(
    records: Iterable[Mapping[str, Any]],
) -> dict[tuple[str, str | None], int]:
    """Find repeated current (visitor_id, account_id) pairs in a batch extract."""
    counts = Counter(
        (record["visitor_id"], record.get("account_id") or None)
        for record in records
        if str(record.get("effective_to", "")).startswith("9999-12-31")
    )
    return {key: count for key, count in counts.items() if count > 1}


def extract_ad_creative_ids(payload: Mapping[str, Any]) -> list[dict[str, str]]:
    """Extract campaign/ad/creative identifiers from a nested API response."""
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Ad metadata response must contain a records array")
    output = []
    for row_number, record in enumerate(records, start=1):
        try:
            campaign_id = record["campaign"]["campaign_id"]
            ad_id = record["ad_id"]
            creative_id = record["creative"]["creative_id"]
        except (KeyError, TypeError) as error:
            raise ValueError(f"Ad metadata record {row_number} has missing nested IDs") from error
        values = (campaign_id, ad_id, creative_id)
        if any(not isinstance(value, str) or not value.strip() for value in values):
            raise ValueError(f"Ad metadata record {row_number} has blank nested IDs")
        output.append(
            {"campaign_id": campaign_id, "ad_id": ad_id, "creative_id": creative_id}
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures-dir", type=Path, default=PROJECT_ROOT / "fixtures")
    args = parser.parse_args()
    fixture_dir = args.fixtures_dir

    with (fixture_dir / "ad_events.jsonl").open(encoding="utf-8") as file:
        events = [json.loads(line) for line in file if line.strip()]
    with (fixture_dir / "identity_map.csv").open(newline="", encoding="utf-8") as file:
        identities = list(csv.DictReader(file))
    with (fixture_dir / "ad_metadata.json").open(encoding="utf-8") as file:
        ad_metadata = json.load(file)

    event_issues = validate_ad_events(events)
    identity_duplicates = find_duplicate_current_identities(identities)
    try:
        ad_creatives = extract_ad_creative_ids(ad_metadata)
    except ValueError as error:
        print(f"Invalid API metadata: {error}")
        return 1

    report = {
        "row_counts": {
            "ad_events": len(events),
            "identity_versions": len(identities),
            "ad_metadata_versions": len(ad_creatives),
        },
        "event_issues": {key: value for key, value in event_issues.items() if value},
        "duplicate_current_identities": [
            {"visitor_id": visitor, "account_id": account, "count": count}
            for (visitor, account), count in identity_duplicates.items()
        ],
    }
    print(json.dumps(report, indent=2))
    return 1 if report["event_issues"] or report["duplicate_current_identities"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
