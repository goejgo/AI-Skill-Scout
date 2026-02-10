# skill-scout

A skill for discovering, evaluating, and managing AI skills from community sources.

## The Problem

The open skills ecosystem is growing fast. Community-contributed skills are proliferating across GitHub repositories, curated lists, and social media. But there's no standard process for evaluating what's worth adopting, and no framework for doing it safely.

Skills are loaded into your AI assistant's context window. A malicious skill can inject prompts, exfiltrate data through crafted instructions, or bundle scripts that execute with the same permissions as the user running the assistant. Installing a skill is an act of trust — and the ecosystem currently provides no tools for making that trust decision systematically.

## What This Skill Does

**skill-scout** gives your AI assistant a repeatable pipeline for skill acquisition:

1. **Scout** — Search tracked GitHub repositories for new skills, pull candidates into an incoming queue
2. **Vet** — Score each skill on a 25-point checklist covering structure, value, quality, security, and adaptability. Skills with executable code are flagged for human review.
3. **Adopt or Reject** — Move skills to a vetted library or reject with documented reasoning
4. **Load** — At the start of a session, identify which vetted skills are relevant and load them into context
5. **Update** — Periodically check if adopted skills have been updated upstream and re-vet changes

## Security Model

The vetting checklist (`references/vetting.md`) implements defense-in-depth:

- **Mandatory file audit** before scoring — every file in the skill directory is inventoried and inspected, not just SKILL.md
- **Quick reject criteria** for obfuscated code, base64 content, prompt injection patterns, and credential access
- **Human gate** for executable content — skills with scripts, hooks, or command-bearing config files cannot be auto-adopted
- **Supply chain awareness** — popularity is not security; trending skills get more scrutiny, not less
- **Trust tiers** — platform vendor skills get lighter review, unknown sources get deep vetting

## Installation

### As a Claude Code / Cowork skill

Copy the `skill-scout/` directory into your skills folder:

```bash
cp -r skill-scout/ ~/.claude/skills/skill-scout/
```

Or in Cowork mode, place it in your mounted workspace's `.skills/skills/` directory.

### As a standalone framework

The vetting checklist and inventory script work independently. You don't need to install the full skill to use them:

- `references/vetting.md` — Use as a review checklist for any skill you're considering
- `scripts/inventory.py` — Run against any directory of skills to get a status report

## Usage

Tell your AI assistant:

- **"Scout for new skills"** — Searches tracked sources, pulls candidates into incoming/
- **"Vet incoming skills"** — Scores candidates, adopts or rejects with documentation
- **"Load skills for this task"** — Identifies and loads relevant vetted skills
- **"Run skill inventory"** — Reports current state of the pipeline
- **"Check for skill updates"** — Compares adopted skills against upstream versions

## Directory Structure

```
skill-scout/
  SKILL.md              — The meta-skill (instructions for the AI)
  scripts/
    inventory.py        — Skill inventory scanner
  references/
    vetting.md          — 25-point vetting checklist with security framework
    sources.md          — Source registry template with community examples
```

Your skill library (created on first use):

```
skill-library/
  incoming/             — Candidates pulled from sources, awaiting review
  vetted/               — Reviewed and approved, ready to load
  rejected/             — Declined with documented reasons
  logs/                 — Scout run history and vetting decisions
```

## Inventory Script

```bash
# Basic usage
python3 scripts/inventory.py ./skill-library

# With system-installed skills
python3 scripts/inventory.py ./skill-library --system-skills ~/.claude/skills
```

Reports all skills across the pipeline, parses YAML frontmatter, and flags skills containing executable content.

## Compatibility

skill-scout uses the SKILL.md format [documented by Anthropic](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills). The format is plain markdown with YAML frontmatter — portable to any tool that supports markdown-based skill or instruction files.

## Contributing

If you find a useful skill source or have improvements to the vetting checklist, contributions are welcome. The security framework in particular benefits from more eyes — if you spot a gap, please open an issue.

## License

MIT
