"""Unit tests for Python checks on the three synthetic source patterns."""

import unittest

from scripts.validate_source_fixtures import (
    extract_ad_creative_ids,
    find_duplicate_current_identities,
    validate_ad_events,
)


class SourceFixtureValidationTests(unittest.TestCase):
    def test_valid_event(self):
        event = {
            "event_id": "E001", "visitor_id": "V001", "campaign_id": "C001",
            "ad_id": "A001", "creative_id": "CR001", "placement_id": "P001",
            "raw_event_type": "CLICK", "device_type": "mobile",
        }
        self.assertFalse(any(validate_ad_events([event]).values()))

    def test_invalid_event_type_missing_identifiers_and_device(self):
        issues = validate_ad_events([{
            "event_id": "E002", "visitor_id": "V001", "campaign_id": " ",
            "ad_id": "A001", "creative_id": "CR001", "placement_id": "P001",
            "raw_event_type": "purchase", "device_type": " ",
        }])
        self.assertEqual(issues["invalid_event_type"], ["E002"])
        self.assertEqual(issues["missing_required_id"], ["E002"])
        self.assertEqual(issues["missing_device_type"], ["E002"])

    def test_duplicate_event_id(self):
        event = {
            "event_id": "E001", "visitor_id": "V001", "campaign_id": "C001",
            "ad_id": "A001", "creative_id": "CR001", "placement_id": "P001",
            "raw_event_type": "view", "device_type": "desktop",
        }
        self.assertEqual(validate_ad_events([event, event])["duplicate_event_id"], ["E001"])

    def test_duplicate_current_identity_pair_only(self):
        records = [
            {"visitor_id": "V001", "account_id": "A001", "effective_to": "9999-12-31"},
            {"visitor_id": "V001", "account_id": "A001", "effective_to": "9999-12-31"},
            {"visitor_id": "V001", "account_id": "A001", "effective_to": "2026-01-01"},
            {"visitor_id": "V002", "account_id": "A002", "effective_to": "9999-12-31"},
        ]
        self.assertEqual(find_duplicate_current_identities(records), {("V001", "A001"): 2})

    def test_nested_api_metadata_extraction(self):
        payload = {"records": [{
            "ad_id": "A001", "campaign": {"campaign_id": "C001"},
            "creative": {"creative_id": "CR001", "creative_name": "Sample"},
        }]}
        self.assertEqual(extract_ad_creative_ids(payload), [{
            "campaign_id": "C001", "ad_id": "A001", "creative_id": "CR001",
        }])

    def test_missing_nested_api_metadata_fails(self):
        with self.assertRaisesRegex(ValueError, "missing nested IDs"):
            extract_ad_creative_ids({"records": [{"ad_id": "A001", "campaign": {}}]})

    def test_missing_records_array_fails(self):
        with self.assertRaisesRegex(ValueError, "records array"):
            extract_ad_creative_ids({"ads": []})


if __name__ == "__main__":
    unittest.main()
