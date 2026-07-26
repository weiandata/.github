"""Deterministic rendering for repository-local WAEF-owned adapter blocks."""

from __future__ import annotations

import re


START_MARKER = "<!-- WAEF:START -->"
END_MARKER = "<!-- WAEF:END -->"
GENERATED_MARKER_RE = re.compile(
    r"^<!-- Generated from WAEF [0-9]+\.[0-9]+; do not edit this block directly\. -->$",
    re.MULTILINE,
)
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def render_compliance_workflow(commit: str) -> str:
    """Render the only accepted repository-local WAEF workflow caller."""

    if not COMMIT_RE.fullmatch(commit):
        raise ValueError("workflow commit must be a full lowercase 40-character SHA")
    return (
        "name: WAEF Compliance\n"
        "on: [pull_request, push]\n"
        "permissions:\n"
        "  contents: read\n"
        "jobs:\n"
        "  compliance:\n"
        f"    uses: weiandata/WAEF/.github/workflows/compliance.yml@{commit}\n"
        "    with:\n"
        f"      waef_commit: {commit}\n"
        "      lock_path: .waef/waef.lock.yml\n"
        "    secrets:\n"
        "      WAEF_APP_ID: ${{ secrets.WAEF_APP_ID }}\n"
        "      WAEF_APP_PRIVATE_KEY: ${{ secrets.WAEF_APP_PRIVATE_KEY }}\n"
    )


def render_public_compliance_workflow(repository: str, commit: str) -> str:
    """Render the exact repository-bound bridge for a public repository."""

    if not REPOSITORY_RE.fullmatch(repository):
        raise ValueError("repository must be a valid GitHub repository name")
    if not COMMIT_RE.fullmatch(commit):
        raise ValueError("workflow commit must be a full lowercase 40-character SHA")
    return (
        "name: WAEF Compliance\n"
        "on: [pull_request, push]\n"
        "permissions:\n"
        "  contents: read\n"
        "jobs:\n"
        "  compliance:\n"
        "    name: WAEF Compliance\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 15\n"
        "    steps:\n"
        "      - name: Check out consumer repository\n"
        "        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10\n"
        "        with:\n"
        "          persist-credentials: false\n"
        "\n"
        "      - name: Restrict public organization bridge\n"
        "        env:\n"
        "          CALLER_REPOSITORY: ${{ github.repository }}\n"
        "        run: |\n"
        "          set -euo pipefail\n"
        f'          test "${{CALLER_REPOSITORY}}" = "weiandata/{repository}"\n'
        "\n"
        "      - name: Create private WAEF read token\n"
        "        id: waef-token\n"
        "        uses: actions/create-github-app-token@f8d387b68d61c58ab83c6c016672934102569859\n"
        "        with:\n"
        "          app-id: ${{ secrets.WAEF_APP_ID }}\n"
        "          private-key: ${{ secrets.WAEF_APP_PRIVATE_KEY }}\n"
        "          owner: weiandata\n"
        "          repositories: WAEF\n"
        "\n"
        "      - name: Check out exact private WAEF source\n"
        "        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10\n"
        "        with:\n"
        "          repository: weiandata/WAEF\n"
        f"          ref: {commit}\n"
        "          token: ${{ steps.waef-token.outputs.token }}\n"
        "          path: .waef/cache\n"
        "          persist-credentials: false\n"
        "          fetch-depth: 0\n"
        "\n"
        "      - name: Verify exact private WAEF source\n"
        "        env:\n"
        "          WAEF_LOCK_PATH: .waef/waef.lock.yml\n"
        '        run: python3 .waef/cache/scripts/verify_framework_checkout.py --lock "$GITHUB_WORKSPACE/$WAEF_LOCK_PATH" --checkout .waef/cache\n'
        "\n"
        "      - name: Install pinned validator requirements\n"
        "        run: python3 -m pip install --disable-pip-version-check --requirement .waef/cache/requirements.txt\n"
        "\n"
        "      - name: Validate consumer repository\n"
        "        env:\n"
        "          WAEF_LOCK_PATH: .waef/waef.lock.yml\n"
        '        run: python3 .waef/cache/scripts/validate_repository.py "$GITHUB_WORKSPACE" --event "$GITHUB_EVENT_PATH" --lock-path "$WAEF_LOCK_PATH"\n'
    )


def _bounds(text: str) -> tuple[int, int]:
    if text.count(START_MARKER) != 1 or text.count(END_MARKER) != 1:
        raise ValueError("adapter must contain exactly one WAEF marker pair")
    start = text.index(START_MARKER)
    end = text.index(END_MARKER)
    if start >= end:
        raise ValueError("WAEF start marker must precede end marker")
    return start, end + len(END_MARKER)


def render_waef_block(body: str, version: str) -> str:
    if not VERSION_RE.fullmatch(version):
        raise ValueError("WAEF version must use MAJOR.MINOR")
    if START_MARKER in body or END_MARKER in body:
        raise ValueError("WAEF block body must not contain governance markers")
    normalized = body.strip("\n")
    return (
        f"{START_MARKER}\n"
        f"<!-- Generated from WAEF {version}; do not edit this block directly. -->\n"
        f"{normalized}\n"
        f"{END_MARKER}"
    )


def replace_waef_block(text: str, body: str, version: str) -> str:
    """Replace one WAEF-owned block while preserving all project-owned bytes."""

    start, end = _bounds(text)
    return text[:start] + render_waef_block(body, version) + text[end:]


def update_generated_version(text: str, version: str) -> str:
    """Update only the generated-version marker inside a valid WAEF block."""

    start, end = _bounds(text)
    block = text[start:end]
    markers = GENERATED_MARKER_RE.findall(block)
    if len(markers) != 1:
        raise ValueError("WAEF block must contain exactly one generated-version marker")
    body = GENERATED_MARKER_RE.sub("", block, count=1)
    body = body.removeprefix(START_MARKER).removesuffix(END_MARKER).strip("\n")
    return replace_waef_block(text, body, version)
