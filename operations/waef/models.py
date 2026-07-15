"""Validated data models for WAEF organization automation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


APPROVED_REPOSITORIES = frozenset(
    {
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
)
ROOT_FIELDS = frozenset({"schema_version", "organization", "repositories"})
REPOSITORY_FIELDS = frozenset(
    {"name", "owner", "lifecycle", "profiles", "expected_waef_check", "migration_wave"}
)


class InventoryError(ValueError):
    """Raised when the reviewed repository inventory is invalid."""


@dataclass(frozen=True, slots=True)
class RepositoryRecord:
    name: str
    owner: str
    lifecycle: str
    profiles: tuple[str, ...]
    expected_waef_check: str
    migration_wave: int


@dataclass(frozen=True, slots=True)
class AuditFinding:
    repository: str
    rule_id: str
    path: str
    message: str
    severity: str = "error"

    @property
    def fingerprint(self) -> str:
        identity = f"{self.repository}\0{self.rule_id}\0{self.path}".encode("utf-8")
        return hashlib.sha256(identity).hexdigest()[:20]


def _require_string(record: dict, field: str, repository: str) -> str:
    value = record[field]
    if not isinstance(value, str) or not value.strip():
        raise InventoryError(f"repository {repository!r} field {field!r} must be a non-empty string")
    return value


def _parse_record(raw: object, index: int) -> RepositoryRecord:
    if not isinstance(raw, dict):
        raise InventoryError(f"repository entry {index} must be an object")
    fields = set(raw)
    unknown = fields - REPOSITORY_FIELDS
    missing = REPOSITORY_FIELDS - fields
    if unknown:
        raise InventoryError(f"repository entry {index} has unknown fields: {sorted(unknown)}")
    if missing:
        raise InventoryError(f"repository entry {index} has missing fields: {sorted(missing)}")

    name = _require_string(raw, "name", f"entry {index}")
    owner = _require_string(raw, "owner", name)
    lifecycle = _require_string(raw, "lifecycle", name)
    expected_check = _require_string(raw, "expected_waef_check", name)
    profiles = raw["profiles"]
    wave = raw["migration_wave"]

    if lifecycle not in {"active", "planned"}:
        raise InventoryError(f"repository {name!r} has invalid lifecycle {lifecycle!r}")
    if not isinstance(profiles, list) or not profiles or not all(
        isinstance(profile, str) and profile.strip() for profile in profiles
    ):
        raise InventoryError(f"repository {name!r} profiles must be a non-empty string list")
    if len(profiles) != len(set(profiles)):
        raise InventoryError(f"repository {name!r} has duplicate profiles")
    if not isinstance(wave, int) or isinstance(wave, bool) or wave not in {1, 2, 3}:
        raise InventoryError(f"repository {name!r} migration_wave must be 1, 2, or 3")

    return RepositoryRecord(
        name=name,
        owner=owner,
        lifecycle=lifecycle,
        profiles=tuple(profiles),
        expected_waef_check=expected_check,
        migration_wave=wave,
    )


def load_inventory(path: str | Path) -> list[RepositoryRecord]:
    """Load the reviewed inventory and reject any schema or repository drift."""

    source = Path(path)
    try:
        document = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InventoryError(f"cannot load inventory {source}: {error}") from error
    if not isinstance(document, dict):
        raise InventoryError("inventory root must be an object")

    fields = set(document)
    unknown = fields - ROOT_FIELDS
    missing = ROOT_FIELDS - fields
    if unknown:
        raise InventoryError(f"inventory has unknown fields: {sorted(unknown)}")
    if missing:
        raise InventoryError(f"inventory has missing fields: {sorted(missing)}")
    if document["schema_version"] != 1:
        raise InventoryError("inventory schema_version must be 1")
    if document["organization"] != "weiandata":
        raise InventoryError("inventory organization must be 'weiandata'")
    if not isinstance(document["repositories"], list):
        raise InventoryError("inventory repositories must be a list")

    records = [_parse_record(raw, index) for index, raw in enumerate(document["repositories"])]
    names = [record.name for record in records]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise InventoryError(f"duplicate repository entries: {duplicates}")
    if set(names) != APPROVED_REPOSITORIES:
        missing_names = sorted(APPROVED_REPOSITORIES - set(names))
        unknown_names = sorted(set(names) - APPROVED_REPOSITORIES)
        raise InventoryError(
            "inventory does not match the approved repository set; "
            f"missing={missing_names}, unknown={unknown_names}"
        )
    return records
