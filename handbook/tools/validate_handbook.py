#!/usr/bin/env python3
"""Validate the structural and machine-readable publication contract."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "handbook-manifest.json"
REGISTRY_PATH = ROOT / "rule-registry.json"
REQUIRED_METADATA = ("Version", "Status", "Owner", "Effective date")
REQUIRED_SECTIONS = (
    "Purpose",
    "Scope",
    "Philosophy",
    "Principles",
    "Standards",
    "Best Practices",
    "Examples",
    "Checklist",
    "Summary",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TBD|TODO|FIXME)\b")
NORMATIVE_PATTERN = re.compile(r"\b(?:MUST|MUST NOT|SHOULD|SHOULD NOT|MAY)\b")


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name}: root value must be an object")
        return {}
    return value


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"[ ]+", "-", text)


def headings(path: Path) -> set[str]:
    slugs: set[str] = set()
    counts: Counter[str] = Counter()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            base = github_slug(match.group(1))
            count = counts[base]
            counts[base] += 1
            slugs.add(base if count == 0 else f"{base}-{count}")
    return slugs


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if path.is_file())


def resolve_local(source: Path, target: str) -> tuple[Path | None, str]:
    target = target.strip().strip("<>")
    file_part, _, anchor = target.partition("#")
    if file_part:
        resolved = (source.parent / unquote(file_part)).resolve()
    else:
        resolved = source.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return None, anchor
    return resolved, anchor


def validate_manifest(manifest: dict, errors: list[str]) -> list[Path]:
    version = manifest.get("handbook_version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("handbook-manifest.json: handbook_version must use MAJOR.MINOR.PATCH")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if isinstance(version, str) and f"| Release | v{version} |" not in readme:
        errors.append("README.md: release does not match handbook-manifest.json")

    for target in manifest.get("authority", []):
        if not (ROOT / target).is_file():
            errors.append(f"handbook-manifest.json: missing authority document {target}")

    entries = manifest.get("chapters", [])
    if not isinstance(entries, list) or not entries:
        errors.append("handbook-manifest.json: chapters must be a non-empty array")
        return []

    numbers = [entry.get("number") for entry in entries if isinstance(entry, dict)]
    expected = [f"{number:02d}" for number in range(len(entries))]
    if numbers != expected:
        errors.append(f"handbook-manifest.json: chapter sequence must be {expected}")

    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    if len(ids) != len(set(ids)):
        errors.append("handbook-manifest.json: chapter ids must be unique")

    paths: list[Path] = []
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("handbook-manifest.json: each chapter entry must be an object")
            continue
        for field in ("number", "id", "path", "topic", "owner", "default_risk"):
            if not entry.get(field):
                errors.append(f"handbook-manifest.json: chapter entry missing {field}")
        path = ROOT / str(entry.get("path", ""))
        if not path.is_file():
            errors.append(f"handbook-manifest.json: missing chapter {entry.get('path')}")
        else:
            paths.append(path)
            if not path.name.startswith(f"{entry.get('number')}-"):
                errors.append(f"handbook-manifest.json: number/path mismatch for {path.name}")

    declared_numbers = set(numbers)
    profile_paths = {entry.get("path") for entry in manifest.get("profiles", []) if isinstance(entry, dict)}
    for group in ("profiles", "templates"):
        for entry in manifest.get(group, []):
            if not isinstance(entry, dict) or not entry.get("id") or not entry.get("path"):
                errors.append(f"handbook-manifest.json: invalid {group} entry")
                continue
            if not (ROOT / entry["path"]).is_file():
                errors.append(f"handbook-manifest.json: missing {group} path {entry['path']}")

    for route_id, route in manifest.get("task_routes", {}).items():
        if not isinstance(route, dict):
            errors.append(f"handbook-manifest.json: route {route_id} must be an object")
            continue
        if route.get("mode") not in {"Lightweight", "Standard", "Controlled"}:
            errors.append(f"handbook-manifest.json: route {route_id} has invalid mode")
        if route.get("profile") not in profile_paths:
            errors.append(f"handbook-manifest.json: route {route_id} has unknown profile")
        unknown = set(route.get("required_chapters", [])) - declared_numbers
        if unknown:
            errors.append(f"handbook-manifest.json: route {route_id} has unknown chapters {sorted(unknown)}")

    return paths


def validate_chapters(chapters: list[Path], errors: list[str]) -> None:
    for path in chapters:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for field in REQUIRED_METADATA:
            if not re.search(rf"^\| {re.escape(field)} \| .+ \|$", text, re.MULTILINE):
                errors.append(f"{relative}: missing metadata field {field}")
        found = [
            (int(match.group(1)), match.group(2).strip())
            for match in re.finditer(r"^## (\d+)\. (.+)$", text, re.MULTILINE)
        ]
        required = list(enumerate(REQUIRED_SECTIONS, start=1))
        valid = found == required or found == required + [(10, "References")]
        if not valid:
            errors.append(f"{relative}: required sections are missing or out of order: {found}")

    toc = (ROOT / "README.md").read_text(encoding="utf-8")
    toc_links = [target.split("#", 1)[0] for target in LINK_PATTERN.findall(toc)]
    chapter_counts = Counter(target for target in toc_links if target.startswith("chapters/"))
    for path in chapters:
        target = str(path.relative_to(ROOT))
        if chapter_counts[target] != 1:
            errors.append(f"README must link {target} exactly once; found {chapter_counts[target]}")


def validate_registry(registry: dict, heading_cache: dict[Path, set[str]], errors: list[str]) -> int:
    rules = registry.get("rules", [])
    if not isinstance(rules, list) or not rules:
        errors.append("rule-registry.json: rules must be a non-empty array")
        return 0
    ids: list[str] = []
    topics: list[str] = []
    for rule in rules:
        if not isinstance(rule, dict):
            errors.append("rule-registry.json: each rule must be an object")
            continue
        for field in ("id", "topic", "owner", "source", "risk", "applies_to", "summary"):
            if not rule.get(field):
                errors.append(f"rule-registry.json: rule missing {field}")
        rule_id = str(rule.get("id", ""))
        ids.append(rule_id)
        topics.append(str(rule.get("topic", "")))
        if not re.fullmatch(r"WD-[A-Z]+-\d{3}", rule_id):
            errors.append(f"rule-registry.json: invalid rule id {rule_id}")
        owner = ROOT / str(rule.get("owner", ""))
        source_path, anchor = resolve_local(ROOT / "rule-registry.json", str(rule.get("source", "")))
        if not owner.is_file():
            errors.append(f"rule-registry.json: missing owner {rule.get('owner')}")
        if source_path is None or not source_path.is_file():
            errors.append(f"rule-registry.json: missing source {rule.get('source')}")
        else:
            if source_path != owner.resolve():
                errors.append(f"rule-registry.json: owner/source mismatch for {rule_id}")
            if anchor and anchor not in heading_cache.get(source_path, set()):
                errors.append(f"rule-registry.json: missing source anchor for {rule_id}")
    if len(ids) != len(set(ids)):
        errors.append("rule-registry.json: rule ids must be unique")
    if len(topics) != len(set(topics)):
        errors.append("rule-registry.json: rule topics must be uniquely owned")
    return len(rules)


def validate_markdown(all_markdown: list[Path], heading_cache: dict[Path, set[str]], errors: list[str]) -> None:
    normative_locations: defaultdict[str, list[str]] = defaultdict(list)
    for path in all_markdown:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if CJK_PATTERN.search(text):
            errors.append(f"{relative}: contains CJK characters")
        if PLACEHOLDER_PATTERN.search(text):
            errors.append(f"{relative}: contains unresolved placeholder token")

        in_fence = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.startswith("```"):
                if not in_fence and line.strip() == "```":
                    errors.append(f"{relative}:{line_number}: fenced code block has no language")
                in_fence = not in_fence
                continue
            if not in_fence and NORMATIVE_PATTERN.search(line) and len(line.strip()) >= 60:
                normalized = re.sub(r"\s+", " ", line.strip().lstrip("- "))
                normative_locations[normalized].append(f"{relative}:{line_number}")
        if in_fence:
            errors.append(f"{relative}: unclosed fenced code block")

        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved, anchor = resolve_local(path, target)
            if resolved is None:
                errors.append(f"{relative}: link escapes handbook root: {target}")
            elif not resolved.is_file():
                errors.append(f"{relative}: missing link target {target}")
            elif anchor and anchor not in heading_cache.get(resolved, set()):
                errors.append(f"{relative}: missing anchor in {target}")

    for statement, locations in normative_locations.items():
        files = {location.rsplit(":", 1)[0] for location in locations}
        if len(files) > 1:
            errors.append(f"exact normative duplication across files: {locations}: {statement}")


def validate() -> tuple[list[str], int, int]:
    errors: list[str] = []
    manifest = load_json(MANIFEST_PATH, errors)
    registry = load_json(REGISTRY_PATH, errors)
    chapters = validate_manifest(manifest, errors) if manifest else []
    validate_chapters(chapters, errors)

    all_markdown = markdown_files()
    heading_cache = {path.resolve(): headings(path) for path in all_markdown}
    validate_markdown(all_markdown, heading_cache, errors)
    rule_count = validate_registry(registry, heading_cache, errors) if registry else 0
    if manifest and registry and manifest.get("handbook_version") != registry.get("handbook_version"):
        errors.append("manifest and rule registry handbook versions differ")
    return errors, len(chapters), rule_count


def main() -> int:
    errors, chapter_count, rule_count = validate()
    if errors:
        print(f"FAIL: {len(errors)} handbook validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: handbook v1.1 publication contract is satisfied")
    print(f"Markdown files checked: {len(markdown_files())}")
    print(f"Chapter files checked: {chapter_count}")
    print(f"Stable rule identifiers checked: {rule_count}")
    print("Machine-readable manifest and task routes: valid")
    print("Required chapter sections: 1-9; References optional")
    return 0


if __name__ == "__main__":
    sys.exit(main())

