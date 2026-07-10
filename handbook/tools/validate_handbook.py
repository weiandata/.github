#!/usr/bin/env python3
"""Validate the structural publication contract of the WeianData handbook."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
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
    "References",
)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TBD|TODO|FIXME)\b")


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


def validate() -> list[str]:
    errors: list[str] = []
    chapters = sorted(CHAPTERS.glob("*.md"))
    numbers = [int(path.name[:2]) for path in chapters if re.match(r"^\d{2}-", path.name)]
    if numbers != list(range(36)):
        errors.append(f"chapter numbering is not consecutive 00-35: {numbers}")
    if len(chapters) != 36:
        errors.append(f"expected 36 chapter files, found {len(chapters)}")

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
        expected = list(enumerate(REQUIRED_SECTIONS, start=1))
        if found != expected:
            errors.append(f"{relative}: required sections are missing or out of order: {found}")

    toc = (ROOT / "README.md").read_text(encoding="utf-8")
    toc_links = [target.split("#", 1)[0] for target in LINK_PATTERN.findall(toc)]
    chapter_counts = Counter(target for target in toc_links if target.startswith("chapters/"))
    for path in chapters:
        target = f"chapters/{path.name}"
        if chapter_counts[target] != 1:
            errors.append(f"README must link {target} exactly once; found {chapter_counts[target]}")

    all_markdown = markdown_files()
    heading_cache = {path: headings(path) for path in all_markdown}
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
        if in_fence:
            errors.append(f"{relative}: unclosed fenced code block")

        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                if target.startswith("#") and target[1:] not in heading_cache[path]:
                    errors.append(f"{relative}: missing local anchor {target}")
                continue
            if Path(target.split("#", 1)[0]).is_absolute():
                errors.append(f"{relative}: absolute local path is prohibited: {target}")
                continue
            file_part, _, anchor = target.partition("#")
            resolved = (path.parent / unquote(file_part)).resolve() if file_part else path
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{relative}: link escapes handbook root: {target}")
                continue
            if not resolved.is_file():
                errors.append(f"{relative}: missing link target {target}")
            elif anchor and anchor not in heading_cache.get(resolved, set()):
                errors.append(f"{relative}: missing anchor in {target}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL: {len(errors)} handbook validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: handbook publication contract is satisfied")
    print(f"Markdown files checked: {len(markdown_files())}")
    print("Chapter files checked: 36")
    print("Chapter sequence: 00-35")
    print("Required chapter sections: 10")
    return 0


if __name__ == "__main__":
    sys.exit(main())

