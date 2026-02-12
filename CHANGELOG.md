# Changelog

All notable changes to AI Skill Scout are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [0.3.0] — 2026-02-11

### Added
- Prompt injection detection in `inventory.py` — scans SKILL.md and AGENT.md for override instructions, privilege escalation, data exfiltration patterns, base64 obfuscation, and zero-width Unicode
- Code block stripping to avoid false positives on security documentation
- Retroactive Re-Scanning section in `vetting.md` — when to re-scan, how, and what to do with findings

### Changed
- Scanner now reports `[SUSPICIOUS]` flags alongside `[EXECUTABLE]` flags

## [0.2.0] — 2026-02-11

### Added
- `CONTRIBUTING.md` with contribution guidelines and priorities
- Complementary Security Tools section in `sources.md` (Caterpillar, MCP-Scan, Cisco skill-scanner, Nova-Proximity)
- Ecosystem Context section in `sources.md` (SkillsMP, Agent Skills Hub, Superpowers, Claude Code Skill Factory)

### Changed
- `README.md` rewritten with Snyk ToxicSkills stats (36% vulnerability rate, 1,400+ malicious payloads) and landscape positioning
- Related Projects section added to README categorizing complementary tools

## [0.1.0] — 2026-02-10

### Added
- Initial release
- Vetting checklist (`references/vetting.md`) with 5-dimension scoring, quick-reject criteria, mandatory file audit, and human gate for executable content
- Source registry (`references/sources.md`) with trust tier system
- Inventory scanner (`scripts/inventory.py`) with YAML frontmatter parsing, executable content detection (regex-based boundary matching), and pipeline reporting
- Example skills: sample-vetted and sample-rejected with documented scoring
- MIT License
