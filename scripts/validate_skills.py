#!/usr/bin/env python3
"""Validate Codex skill structure without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(?P<meta>.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str, path: Path, errors: list[str]) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"{path}: missing frontmatter")
        return {}

    values: dict[str, str] = {}
    for raw in match.group("meta").splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            errors.append(f"{path}: invalid frontmatter line: {raw!r}")
            continue
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> int:
    errors: list[str] = []

    if not SKILLS.is_dir():
        errors.append("skills/: directory is missing")
        skill_dirs: list[Path] = []
    else:
        skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
        if not skill_dirs:
            errors.append("skills/: no skills found")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
            continue

        text = skill_file.read_text(encoding="utf-8")
        rel = skill_file.relative_to(ROOT)
        meta = parse_frontmatter(text, rel, errors)
        name = meta.get("name", "")
        description = meta.get("description", "")

        if name != skill_dir.name:
            errors.append(f"{rel}: name must match directory ({skill_dir.name})")
        if name and not NAME_RE.fullmatch(name):
            errors.append(f"{rel}: name must be lowercase hyphen-case")
        if not 20 <= len(description) <= 600:
            errors.append(f"{rel}: description must be 20..600 characters")
        if len(text.split()) > 5000:
            errors.append(f"{rel}: exceeds 5000 words; move detail to references/")
        if "\t" in text:
            errors.append(f"{rel}: tabs are not allowed")

        unknown = set(meta) - {"name", "description"}
        if unknown:
            errors.append(f"{rel}: unsupported frontmatter keys: {sorted(unknown)}")

    for required in ("README.md", "CONTRIBUTING.md", "SECURITY.md"):
        if not (ROOT / required).is_file():
            errors.append(f"{required} is missing")

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} skill(s) successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
