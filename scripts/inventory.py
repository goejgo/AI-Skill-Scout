#!/usr/bin/env python3
"""
Skill inventory scanner.

Reports skills across four directories: system-installed, vetted, incoming,
and rejected. Parses YAML frontmatter from SKILL.md files and flags skills
that contain executable scripts.

Usage:
    python3 inventory.py <skill-library-path> [--system-skills <path>]

Arguments:
    skill-library-path    Root of the skill library (contains vetted/, incoming/, rejected/)
    --system-skills       Optional path to system-installed skills directory

Examples:
    python3 inventory.py ./skill-library
    python3 inventory.py ./skill-library --system-skills ~/.skills/skills
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime


def read_frontmatter(skill_path: Path) -> dict:
    """Extract name and description from SKILL.md YAML frontmatter.

    Handles multi-line descriptions by joining continuation lines.
    Returns a dict with 'name' and 'description' keys.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"name": skill_path.name, "description": "(no SKILL.md)"}

    try:
        content = skill_md.read_text(errors="replace")
    except OSError:
        return {"name": skill_path.name, "description": "(unreadable)"}

    if not content.startswith("---"):
        return {"name": skill_path.name, "description": "(no frontmatter)"}

    try:
        end = content.index("---", 3)
        block = content[3:end].strip()
    except ValueError:
        return {"name": skill_path.name, "description": "(malformed frontmatter)"}

    fm = {}
    current_key = None
    current_val = ""

    for line in block.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # Check if this is a new key: value pair
        if ":" in stripped and not stripped.startswith("-"):
            colon_pos = stripped.index(":")
            candidate_key = stripped[:colon_pos].strip().lower()
            candidate_val = stripped[colon_pos + 1:].strip().strip('"').strip("'")

            # Save previous key if we had one
            if current_key and current_key in ("name", "description"):
                fm[current_key] = current_val.strip()

            current_key = candidate_key
            current_val = candidate_val
        elif current_key:
            # Continuation line for multi-line value
            current_val += " " + stripped.strip('"').strip("'")

    # Save final key
    if current_key and current_key in ("name", "description"):
        fm[current_key] = current_val.strip()

    if not fm:
        return {"name": skill_path.name, "description": "(empty frontmatter)"}
    if "name" not in fm:
        fm["name"] = skill_path.name
    return fm


def has_executable_content(skill_path: Path) -> bool:
    """Check if a skill directory contains executable files or command-bearing configs.

    For config files (.json, .yaml, .yml), looks for key patterns that suggest
    code execution rather than simple substring matches. This avoids false
    positives from words like "runner" or "description" containing "run".
    """
    executable_extensions = {".py", ".sh", ".js", ".ts", ".bash", ".zsh", ".rb", ".pl"}

    # Patterns that indicate execution when used as keys in config files.
    # Each pattern is anchored to look like a key (preceded by quote or line start).
    config_key_patterns = re.compile(
        r'(?:^|\s|"|\')'           # key boundary: start of line, whitespace, or quote
        r'(?:command|exec|spawn|eval|script|run|hook)'
        r'(?:\s*[:=]|"|\')',       # value boundary: colon, equals, or closing quote
        re.IGNORECASE | re.MULTILINE
    )

    for item in skill_path.rglob("*"):
        if not item.is_file():
            continue

        if item.suffix.lower() in executable_extensions:
            return True

        if item.suffix.lower() in (".json", ".yaml", ".yml"):
            try:
                text = item.read_text(errors="replace")
                if config_key_patterns.search(text):
                    return True
            except OSError:
                continue

    return False


def scan_dir(dir_path: Path) -> list:
    """Scan directory for skill subdirectories. Return list of skill info dicts."""
    results = []
    if not dir_path.exists():
        return results

    try:
        entries = sorted(dir_path.iterdir())
    except OSError:
        return results

    for item in entries:
        if not item.is_dir() or item.name.startswith("."):
            continue

        fm = read_frontmatter(item)
        executable = has_executable_content(item)

        desc = fm.get("description", "(none)")
        if len(desc) > 100:
            desc = desc[:97] + "..."

        results.append({
            "dir": item.name,
            "name": fm.get("name", item.name),
            "description": desc,
            "has_executable": executable,
        })

    return results


def print_section(title: str, skills: list) -> None:
    """Print a section of the inventory report."""
    print(f"\n## {title} ({len(skills)})")
    if not skills:
        print("  (none)")
        return
    for s in skills:
        flag = " [EXECUTABLE]" if s["has_executable"] else ""
        print(f"  {s['name']}{flag}")
        print(f"    {s['description']}")


def main():
    # Parse arguments
    args = sys.argv[1:]
    system_skills_path = None
    library_path = None

    i = 0
    while i < len(args):
        if args[i] == "--system-skills" and i + 1 < len(args):
            system_skills_path = Path(args[i + 1])
            i += 2
        elif args[i].startswith("--"):
            print(f"Unknown option: {args[i]}", file=sys.stderr)
            sys.exit(1)
        elif library_path is None:
            library_path = Path(args[i])
            i += 1
        else:
            print(f"Unexpected argument: {args[i]}", file=sys.stderr)
            sys.exit(1)

    if library_path is None:
        print(__doc__.strip())
        sys.exit(1)

    if not library_path.exists():
        print(f"Error: {library_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"=== Skill Inventory — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    # System-installed skills (optional)
    if system_skills_path and system_skills_path.exists():
        print_section("Installed (System)", scan_dir(system_skills_path))

    # Pipeline directories
    vetted = scan_dir(library_path / "vetted")
    incoming = scan_dir(library_path / "incoming")
    rejected = scan_dir(library_path / "rejected")

    print_section("Vetted (Ready to Load)", vetted)
    print_section("Incoming (Awaiting Review)", incoming)
    print_section("Rejected", rejected)

    # Summary
    print(f"\n## Pipeline: {len(vetted)} vetted, {len(incoming)} incoming, {len(rejected)} rejected")

    # Warnings
    executable_vetted = [s for s in vetted if s["has_executable"]]
    if executable_vetted:
        print(f"\n⚠ {len(executable_vetted)} vetted skill(s) contain executable content:")
        for s in executable_vetted:
            print(f"  - {s['name']}")


if __name__ == "__main__":
    main()
