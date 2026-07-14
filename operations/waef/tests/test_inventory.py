import json
import tempfile
import unittest
from pathlib import Path

from operations.waef.models import InventoryError, load_inventory


ROOT = Path(__file__).resolve().parents[3]
INVENTORY = ROOT / "operations" / "waef" / "repositories.json"
EXPECTED_REPOSITORIES = {
    ".github",
    "DCC",
    "IRTC",
    "LISTR",
    "WAEF",
    "WFC",
    "mergecalib",
    "ratecalib",
    "repository-template",
    "website",
    "website-global-preview",
}


class InventoryTests(unittest.TestCase):
    def load_document(self):
        return json.loads(INVENTORY.read_text(encoding="utf-8"))

    def write_document(self, document):
        temporary = tempfile.TemporaryDirectory()
        path = Path(temporary.name) / "repositories.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        self.addCleanup(temporary.cleanup)
        return path

    def test_inventory_registers_exactly_the_approved_repositories(self):
        records = load_inventory(INVENTORY)
        self.assertEqual(EXPECTED_REPOSITORIES, {record.name for record in records})
        self.assertEqual(11, len(records))

    def test_inventory_records_required_governance_fields(self):
        for record in load_inventory(INVENTORY):
            with self.subTest(repository=record.name):
                self.assertTrue(record.owner)
                self.assertIn(record.lifecycle, {"active", "planned"})
                self.assertTrue(record.profiles)
                self.assertEqual("WAEF Compliance", record.expected_waef_check)
                self.assertIn(record.migration_wave, {1, 2, 3})

    def test_inventory_assigns_profiles_and_waves_from_the_approved_design(self):
        records = {record.name: record for record in load_inventory(INVENTORY)}
        for name in {"DCC", "IRTC", "WFC", "mergecalib", "ratecalib"}:
            self.assertEqual(("r-package",), records[name].profiles)
        for name in {"website", "website-global-preview"}:
            self.assertEqual(("static-website",), records[name].profiles)
        for name in {".github", "WAEF"}:
            self.assertEqual(("governance-framework",), records[name].profiles)
        self.assertEqual(("repository-template",), records["repository-template"].profiles)
        self.assertEqual(("planned-project",), records["LISTR"].profiles)

        self.assertEqual(
            {"WAEF", "repository-template", "DCC", "website"},
            {name for name, record in records.items() if record.migration_wave == 1},
        )
        self.assertEqual(
            {"IRTC", "WFC", "mergecalib", "ratecalib"},
            {name for name, record in records.items() if record.migration_wave == 2},
        )
        self.assertEqual(
            {".github", "website-global-preview", "LISTR"},
            {name for name, record in records.items() if record.migration_wave == 3},
        )

    def test_duplicate_repository_is_rejected(self):
        document = self.load_document()
        document["repositories"].append(dict(document["repositories"][0]))
        with self.assertRaisesRegex(InventoryError, "duplicate repository"):
            load_inventory(self.write_document(document))

    def test_unknown_record_field_is_rejected(self):
        document = self.load_document()
        document["repositories"][0]["unreviewed"] = True
        with self.assertRaisesRegex(InventoryError, "unknown fields"):
            load_inventory(self.write_document(document))

    def test_missing_required_field_is_rejected(self):
        document = self.load_document()
        del document["repositories"][0]["owner"]
        with self.assertRaisesRegex(InventoryError, "missing fields"):
            load_inventory(self.write_document(document))

    def test_unapproved_repository_set_is_rejected(self):
        document = self.load_document()
        document["repositories"][0]["name"] = "unregistered"
        with self.assertRaisesRegex(InventoryError, "approved repository set"):
            load_inventory(self.write_document(document))


if __name__ == "__main__":
    unittest.main()
