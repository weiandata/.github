import unittest
from pathlib import Path

from operations.waef.render_adapter import (
    render_public_compliance_workflow,
    replace_waef_block,
    update_generated_version,
)


ROOT = Path(__file__).resolve().parents[3]
PUBLIC_BRIDGE_SOURCE_COMMIT = "3f61a59aace865b162f383a95ecb0372c23880e4"
V43_COMMIT = "bd0eaa761c9ca7b9c4801e0bfcae17e66c03210c"


class RenderAdapterTests(unittest.TestCase):
    def test_renders_exact_repository_bound_public_bridge(self):
        source = (
            ROOT / ".github" / "workflows" / "waef-compliance.yml"
        ).read_text(encoding="utf-8")
        expected = source.replace("weiandata/.github", "weiandata/DCC").replace(
            PUBLIC_BRIDGE_SOURCE_COMMIT, V43_COMMIT
        )

        rendered = render_public_compliance_workflow("DCC", V43_COMMIT)

        self.assertEqual(expected, rendered)

    def test_public_bridge_rejects_non_sha_commit(self):
        with self.assertRaisesRegex(
            ValueError, "full lowercase 40-character SHA"
        ):
            render_public_compliance_workflow("DCC", "main")

    def test_public_bridge_rejects_repository_injection(self):
        with self.assertRaisesRegex(ValueError, "valid GitHub repository name"):
            render_public_compliance_workflow(
                'DCC"\n          run: echo bypass',
                V43_COMMIT,
            )

    def test_replaces_only_the_marked_block(self):
        original = (
            "project preface\n"
            "<!-- WAEF:START -->\n"
            "<!-- Generated from WAEF 3.0; do not edit this block directly. -->\n"
            "old governed content\n"
            "<!-- WAEF:END -->\n"
            "project suffix\n"
        )
        rendered = replace_waef_block(original, "new governed content", "4.0")
        self.assertTrue(rendered.startswith("project preface\n"))
        self.assertTrue(rendered.endswith("project suffix\n"))
        self.assertIn("Generated from WAEF 4.0", rendered)
        self.assertIn("new governed content", rendered)
        self.assertNotIn("old governed content", rendered)

    def test_updates_version_marker_without_rewriting_block_body(self):
        original = (
            "<!-- WAEF:START -->\n"
            "<!-- Generated from WAEF 3.0; do not edit this block directly. -->\n"
            "required section\n"
            "<!-- WAEF:END -->\n"
        )
        rendered = update_generated_version(original, "4.0")
        self.assertIn("Generated from WAEF 4.0", rendered)
        self.assertIn("required section", rendered)

    def test_missing_marker_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly one WAEF marker pair"):
            replace_waef_block("project content\n", "new", "4.0")

    def test_duplicate_marker_is_rejected(self):
        text = "<!-- WAEF:START -->\na\n<!-- WAEF:START -->\nb\n<!-- WAEF:END -->\n"
        with self.assertRaisesRegex(ValueError, "exactly one WAEF marker pair"):
            replace_waef_block(text, "new", "4.0")

    def test_reversed_markers_are_rejected(self):
        text = "<!-- WAEF:END -->\ncontent\n<!-- WAEF:START -->\n"
        with self.assertRaisesRegex(ValueError, "start marker must precede"):
            replace_waef_block(text, "new", "4.0")

    def test_nested_markers_in_generated_body_are_rejected(self):
        text = "<!-- WAEF:START -->\nold\n<!-- WAEF:END -->\n"
        with self.assertRaisesRegex(ValueError, "must not contain governance markers"):
            replace_waef_block(text, "<!-- WAEF:START -->", "4.0")


if __name__ == "__main__":
    unittest.main()
