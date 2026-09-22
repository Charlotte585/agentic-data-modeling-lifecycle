#!/usr/bin/env python3
"""Load synthetic source fixtures into the local DuckDB raw schema."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURES_DIR = PROJECT_ROOT / "fixtures"
DEFAULT_DATABASE = PROJECT_ROOT / "dbt project" / "dev.duckdb"

AD_EVENT_COLUMNS = (
    "event_id",
    "event_timestamp",
    "raw_event_type",
    "visitor_id",
    "campaign_id",
    "ad_id",
    "creative_id",
    "placement_id",
    "device_type",
)

IDENTITY_COLUMNS = (
    "visitor_id",
    "customer_id",
    "account_id",
    "identity_type",
    "account_status",
    "effective_from",
    "effective_to",
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=DEFAULT_FIXTURES_DIR,
        help=f"Fixture directory (default: {DEFAULT_FIXTURES_DIR})",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help=f"DuckDB database path (default: {DEFAULT_DATABASE})",
    )
    return parser.parse_args()


def require_fields(record: dict[str, Any], fields: Iterable[str], context: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise ValueError(f"{context} is missing required fields: {', '.join(missing)}")


def required_text(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context} must be a non-empty string")
    return value


def nullable_text(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise ValueError("Nullable text fields must contain strings or null values")
    return value


def parse_timestamp(value: Any, context: str) -> datetime:
    text = required_text(value, context)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{context} must be an ISO-8601 timestamp") from error
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def read_ad_events(path: Path) -> list[tuple[Any, ...]]:
    rows: list[tuple[Any, ...]] = []
    with path.open(encoding="utf-8") as fixture:
        for line_number, line in enumerate(fixture, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            context = f"{path.name} line {line_number}"
            if not isinstance(record, dict):
                raise ValueError(f"{context} must contain a JSON object")
            require_fields(record, AD_EVENT_COLUMNS, context)
            rows.append(
                (
                    required_text(record["event_id"], f"{context} event_id"),
                    parse_timestamp(
                        record["event_timestamp"], f"{context} event_timestamp"
                    ),
                    required_text(
                        record["raw_event_type"], f"{context} raw_event_type"
                    ),
                    required_text(record["visitor_id"], f"{context} visitor_id"),
                    required_text(record["campaign_id"], f"{context} campaign_id"),
                    required_text(record["ad_id"], f"{context} ad_id"),
                    required_text(record["creative_id"], f"{context} creative_id"),
                    required_text(record["placement_id"], f"{context} placement_id"),
                    required_text(record["device_type"], f"{context} device_type"),
                )
            )
    return rows


def read_identity_map(path: Path) -> list[tuple[Any, ...]]:
    rows: list[tuple[Any, ...]] = []
    with path.open(newline="", encoding="utf-8") as fixture:
        reader = csv.DictReader(fixture)
        if reader.fieldnames is None:
            raise ValueError(f"{path.name} must contain a header row")
        missing_columns = [
            column for column in IDENTITY_COLUMNS if column not in reader.fieldnames
        ]
        if missing_columns:
            raise ValueError(
                f"{path.name} is missing required columns: {', '.join(missing_columns)}"
            )

        for line_number, record in enumerate(reader, start=2):
            context = f"{path.name} line {line_number}"
            rows.append(
                (
                    required_text(record["visitor_id"], f"{context} visitor_id"),
                    nullable_text(record["customer_id"]),
                    nullable_text(record["account_id"]),
                    required_text(record["identity_type"], f"{context} identity_type"),
                    nullable_text(record["account_status"]),
                    parse_timestamp(
                        record["effective_from"], f"{context} effective_from"
                    ),
                    parse_timestamp(record["effective_to"], f"{context} effective_to"),
                )
            )
    return rows


def read_ad_metadata(path: Path) -> list[tuple[Any, ...]]:
    with path.open(encoding="utf-8") as fixture:
        response = json.load(fixture)
    if not isinstance(response, dict) or not isinstance(response.get("records"), list):
        raise ValueError(f"{path.name} must contain a top-level records array")

    rows: list[tuple[Any, ...]] = []
    for record_number, record in enumerate(response["records"], start=1):
        context = f"{path.name} record {record_number}"
        if not isinstance(record, dict):
            raise ValueError(f"{context} must be a JSON object")
        require_fields(
            record,
            ("ad_id", "ad_name", "campaign", "creative", "delivery", "version"),
            context,
        )
        campaign = record["campaign"]
        creative = record["creative"]
        delivery = record["delivery"]
        version = record["version"]
        for field_name, nested_record in (
            ("campaign", campaign),
            ("creative", creative),
            ("delivery", delivery),
            ("version", version),
        ):
            if not isinstance(nested_record, dict):
                raise ValueError(f"{context} {field_name} must be a JSON object")

        require_fields(campaign, ("campaign_id",), f"{context} campaign")
        require_fields(
            creative, ("creative_id", "creative_name"), f"{context} creative"
        )
        require_fields(
            delivery, ("marketing_channel", "status"), f"{context} delivery"
        )
        require_fields(
            version, ("start_timestamp", "end_timestamp"), f"{context} version"
        )
        rows.append(
            (
                required_text(record["ad_id"], f"{context} ad_id"),
                required_text(record["ad_name"], f"{context} ad_name"),
                required_text(campaign["campaign_id"], f"{context} campaign_id"),
                required_text(creative["creative_id"], f"{context} creative_id"),
                required_text(creative["creative_name"], f"{context} creative_name"),
                required_text(
                    delivery["marketing_channel"], f"{context} marketing_channel"
                ),
                required_text(delivery["status"], f"{context} status"),
                parse_timestamp(
                    version["start_timestamp"], f"{context} start_timestamp"
                ),
                parse_timestamp(
                    version["end_timestamp"], f"{context} end_timestamp"
                ),
            )
        )
    return rows


def insert_rows(
    connection: duckdb.DuckDBPyConnection,
    table_name: str,
    placeholders: int,
    rows: Sequence[tuple[Any, ...]],
) -> None:
    values = ", ".join("?" for _ in range(placeholders))
    connection.executemany(f"INSERT INTO {table_name} VALUES ({values})", rows)


def load_raw_tables(
    database: Path,
    ad_events: Sequence[tuple[Any, ...]],
    identity_map: Sequence[tuple[Any, ...]],
    ad_metadata: Sequence[tuple[Any, ...]],
) -> dict[str, int]:
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(database))
    try:
        connection.execute("BEGIN TRANSACTION")
        try:
            connection.execute("CREATE SCHEMA IF NOT EXISTS raw")
            connection.execute("DROP TABLE IF EXISTS raw.ad_events")
            connection.execute("DROP TABLE IF EXISTS raw.identity_map")
            connection.execute("DROP TABLE IF EXISTS raw.ad_metadata")
            connection.execute(
                """
                CREATE TABLE raw.ad_events (
                    event_id VARCHAR,
                    event_timestamp TIMESTAMPTZ,
                    raw_event_type VARCHAR,
                    visitor_id VARCHAR,
                    campaign_id VARCHAR,
                    ad_id VARCHAR,
                    creative_id VARCHAR,
                    placement_id VARCHAR,
                    device_type VARCHAR
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE raw.identity_map (
                    visitor_id VARCHAR,
                    customer_id VARCHAR,
                    account_id VARCHAR,
                    identity_type VARCHAR,
                    account_status VARCHAR,
                    effective_from TIMESTAMPTZ,
                    effective_to TIMESTAMPTZ
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE raw.ad_metadata (
                    ad_id VARCHAR,
                    ad_name VARCHAR,
                    campaign_id VARCHAR,
                    creative_id VARCHAR,
                    creative_name VARCHAR,
                    marketing_channel VARCHAR,
                    ad_status VARCHAR,
                    ad_version_start_timestamp TIMESTAMPTZ,
                    ad_version_end_timestamp TIMESTAMPTZ
                )
                """
            )
            insert_rows(
                connection, "raw.ad_events", len(AD_EVENT_COLUMNS), ad_events
            )
            insert_rows(
                connection, "raw.identity_map", len(IDENTITY_COLUMNS), identity_map
            )
            insert_rows(connection, "raw.ad_metadata", 9, ad_metadata)
        except Exception:
            connection.execute("ROLLBACK")
            raise
        else:
            connection.execute("COMMIT")

        counts = {}
        for table_name in ("ad_events", "identity_map", "ad_metadata"):
            counts[table_name] = connection.execute(
                f"SELECT COUNT(*) FROM raw.{table_name}"
            ).fetchone()[0]
        return counts
    finally:
        connection.close()


def main() -> None:
    arguments = parse_arguments()
    fixtures_dir = arguments.fixtures_dir.resolve()
    database = arguments.database.resolve()

    ad_events = read_ad_events(fixtures_dir / "ad_events.jsonl")
    identity_map = read_identity_map(fixtures_dir / "identity_map.csv")
    ad_metadata = read_ad_metadata(fixtures_dir / "ad_metadata.json")
    counts = load_raw_tables(database, ad_events, identity_map, ad_metadata)

    print(f"Loaded raw source fixtures into {database}")
    for table_name, row_count in counts.items():
        print(f"raw.{table_name}: {row_count} rows")


if __name__ == "__main__":
    main()
