---
name: skill-scout
description: "Discover, evaluate, and manage AI skills from community sources. Use when scouting for new skills, vetting incoming skills, checking skill inventory, or loading vetted skills for a session."
---

# Skill Scout

Continuous skill acquisition pipeline for AI assistants: discover → evaluate → adopt → load.

Skills are markdown instruction files named SKILL.md that extend an AI assistant's capabilities. This skill provides a systematic framework for finding them in community repositories, vetting them for quality and security, and managing a local library.

## Directory Layout

Create this structure in your workspace:

```
skill-library/
  incoming/   — Pulled from sources, awaiting review
  vetted/     — Reviewed and approved, organized by domain:
    finance/         — Investment, trading, due diligence
    dev/             — Development tools, debugging, architecture
    science/         — Research methodology, writing, peer review
    data/            — Analysis, visualization, databases
    process/         — Workflows, estimation, incident response
    communication/   — Writing, stakeholder comms, documentation
    testing/         — TDD, verification, evaluation
  rejected/   — Declined with documented reasons
  logs/       — Scout run history and decisions
  skill-scout/ — This skill (meta-skill)
```

Domain subdirectories are optional — you can start flat and reorganize later. The inventory script handles both layouts.

## Pre-flight Checks

**Run these BEFORE any Scout or Vet workflow:**

### 1. Environment Awareness Snapshot
Before scouting or vetting, scan your current environment for existing capabilities:
- **Platform built-in skills:** Check what your AI platform provides out of the box (e.g., Cowork's `.skills/skills/`, Claude Code's built-in skills)
- **Installed plugins:** List any active plugins and their bundled skills
- **Your vetted library:** Run `scripts/inventory.py` to see what you've already adopted
- Note capabilities across ALL layers — any new candidate must NOT duplicate what you already have

### 2. Cull Pass Check (if maintaining a library long-term)
Check when you last reviewed your vetted skills for relevance. If more than 90 days, consider culling before adding new skills. Dead weight accumulates.

## Workflows

### Load (Session Bootstrap)

Load vetted skills relevant to the current task.

1. Run `python3 <path-to-skill-scout>/scripts/inventory.py <skill-library-path>` to list available skills (use the full path to inventory.py if running from outside the skill-scout directory)
2. Read YAML frontmatter from each skill in `vetted/` to get names and descriptions
3. Identify which skills are relevant to the current task:
   - Match skill descriptions against the task domain (e.g., data analysis, security review, writing)
   - When multiple skills match, prioritize by specificity — a narrow match beats a broad one
   - When uncertain, list candidates and ask the user which to load
4. For selected skills, read the full SKILL.md body into context
5. Report which skills were loaded and why

**Principle:** Skills share the context window. Load only what's relevant. Three to five skills per session is typical; more than seven is likely too many.

### Scout (Discovery)

Search sources for new skills. Maintain a source registry in `references/sources.md`.

1. Run Pre-flight Checks (environment awareness snapshot + cull pass check)
2. For each tracked source, fetch the current skill listing (README, catalog, or directory listing)
3. Compare against your full pipeline — check `vetted/`, `incoming/`, AND `rejected/` to avoid re-pulling
4. **Redundancy scan** for each candidate:
   a. Check against ALL vetted skills (scan all domain subdirectories in `vetted/`)
   b. Check against platform built-in skills
   c. Check against active plugin capabilities
   d. If >70% purpose overlap with any existing skill or plugin, flag as redundant — do NOT pull into incoming
   e. Log redundant candidates in the scout report with reason for skipping
5. **Usefulness review** — for EVERY candidate that passes step 4 (including partial overlaps):
   a. Identify the 1-3 closest existing skills (vetted, built-in, or plugin) by purpose
   b. Compare: Does the candidate do something the existing skills don't? Is it higher quality? More current? Better structured?
   c. If the candidate is strictly better than an existing vetted skill, recommend **replacing** the old one (move old to rejected/ with reason "superseded by [new]")
   d. If the candidate adds genuine new capability not covered anywhere, proceed to pull into incoming
   e. If the candidate is roughly equivalent to existing coverage, **skip it** — log as "not an improvement over [existing]" in the scout report
   f. Apply this standard: "Would loading this skill meaningfully improve the AI's output on tasks in its domain?" If the answer isn't clearly yes, skip it.
6. For each genuinely new, non-redundant skill that passes usefulness review:
   - Create `incoming/<skill-name>/SKILL.md`
   - Add YAML frontmatter: `name`, `description`, `source` (URL), `trust_tier` (1-3)
   - Preserve any bundled resources the skill depends on
7. Log the run in `logs/scout-YYYY-MM-DD.md`: sources checked, findings, decisions, redundancies skipped, usefulness comparisons
8. Report findings to the user — what's new, what looks promising, what needs vetting, what was skipped (redundant or not an improvement)

**Source management:** Add new sources to `references/sources.md` as you discover them. Remove sources that consistently produce low-quality or abandoned content. Date every entry.

### Vet (Evaluate & Decide)

Evaluate skills in `incoming/` against the checklist in `references/vetting.md`.

1. **Mandatory file audit first.** Run `find <skill-directory> -type f` and account for every file. This is not optional — bundled files are the attack surface.
2. Read the full SKILL.md content
3. **Redundancy & usefulness re-check:** Confirm the skill doesn't overlap with current vetted skills or plugins (may have changed since scouting). Apply the usefulness standard: "Would loading this skill meaningfully improve the AI's output on tasks in its domain?" If not, reject early.
4. As you review, flag any non-markdown files for inspection:
   - Scripts (`.py`, `.sh`, `.js`, `.ts`) → read every line, understand what each does
   - Config files (`.json`, `.yaml`) → check for fields like `"command":`, `"exec":`, `"eval":` that indicate code execution
   - Binary files → reject unless clearly an asset (image, font) with a legitimate purpose
5. Score against the 5-dimension checklist: Structure, Value, Quality, Security, Adaptability (1-5 each, 25 total)
6. Decision:
   - **Score ≥ 20** → Adopt as-is. Copy to appropriate domain subdirectory in `vetted/`, remove from `incoming/`
   - **Score 15-19** → Adopt with modifications. Document changes in `MODIFICATIONS.md`, copy to `vetted/<domain>/`
   - **Score < 15** → Reject. Create `REJECTION.md` with scores and reasons, move to `rejected/`
7. **Human gate:** Skills containing ANY executable code cannot be auto-adopted. Flag them in the vetting report with full file listing and wait for human approval.

### Update (Check for Changes)

Periodically check if adopted skills have been updated upstream.

1. For each skill in `vetted/` that has a `source` field in its frontmatter, fetch the current version from the source URL
2. Compare content against the local copy — look for meaningful changes, not just whitespace
3. If updated:
   - Pull the new version to `incoming/<skill-name>/` (overwriting the previous incoming copy if one exists)
   - Re-vet against the checklist, paying special attention to newly added files or code
   - If it passes, replace the version in `vetted/` and log the update
   - If it fails or introduces executable content, flag for human review
4. Log all update checks in `logs/update-YYYY-MM-DD.md`

## Trust Tiers

| Tier | Source Type | Vetting Level |
|------|-----------|---------------|
| 1 | Platform vendor official repos | Structure check only. Adopt unless environment-incompatible. |
| 2 | High-reputation curated collections (10k+ stars, active maintenance) | Full 25-point checklist. Likely needs modifications for your environment. |
| 3 | Individual repos, social media shares, unknown origin | Deep vet. All files read line-by-line. Assume untrusted until proven otherwise. |

**Star counts and popularity are social proof, not security audits.** A compromised maintainer can push malicious updates to a trusted repo. Trending or viral skills warrant more scrutiny, not less.

## Rules

1. Never execute scripts from unvetted skills
2. Prefer methodology skills (plain markdown) over executable skills — they're safer and more portable
3. Skills with executable code require human approval before adoption
4. Log every scout run and every vetting decision — the audit trail matters
5. When modifying community skills, document every change in `MODIFICATIONS.md`
6. One skill, one purpose — if a community skill tries to do too much, split it or reject it
7. Re-vet adopted skills if their upstream source reports a security incident
8. Place adopted skills in the correct domain subdirectory, not at `vetted/` root
9. Always run pre-flight checks before scouting
