# Skill Source Registry

Track where you find skills, how much you trust them, and when you last checked.

## How to Use This File

Add sources as you discover them. Remove sources that go stale or consistently produce low-quality content. Update the `Last checked` date after every scout run.

Each source gets a trust tier:

| Tier | Meaning | Vetting Required |
|------|---------|-----------------|
| 1 | Platform vendor official | Structure check only |
| 2 | High-reputation, actively maintained (10k+ stars) | Full 25-point checklist |
| 3 | Individual, unknown, or social media sourced | Deep vet, all files line-by-line |

## Example Sources

Below are community repositories known to contain AI skills as of early 2026. Verify current status before relying on any of them — repositories change, get archived, or change maintainers.

### Tier 1: Platform Official

**anthropics/skills**
- URL: https://github.com/anthropics/skills
- Category: Foundational — document creation, design, development
- Trust: Tier 1
- Last checked: —

**anthropics/claude-plugins-official**
- URL: https://github.com/anthropics/claude-plugins-official
- Category: Official plugins (skills + MCPs + commands)
- Trust: Tier 1
- Last checked: —

### Tier 2: Community Curated

**affaan-m/everything-claude-code**
- URL: https://github.com/affaan-m/everything-claude-code
- Category: Development — agents, TDD, code review, security, verification
- Trust: Tier 2
- Notes: Includes Node.js hooks — review executable content before adopting
- Last checked: —

**sickn33/antigravity-awesome-skills**
- URL: https://github.com/sickn33/antigravity-awesome-skills
- Category: Broad — 700+ skills covering architecture, security, data, operations
- Trust: Tier 2
- Notes: Mostly markdown (low execution risk). Large catalog — use CATALOG.md for navigation
- Last checked: —

**ComposioHQ/awesome-claude-skills**
- URL: https://github.com/ComposioHQ/awesome-claude-skills
- Category: Automation, SaaS integrations, development tools
- Trust: Tier 2
- Notes: Curated directory — links to individual repos. Good for discovery.
- Last checked: —

**K-Dense-AI/claude-scientific-skills**
- URL: https://github.com/K-Dense-AI/claude-scientific-skills
- Category: Scientific — bioinformatics, genomics, drug discovery, materials science
- Trust: Tier 2
- Notes: MIT licensed. Narrow domain — activate when scientific tasks arise.
- Last checked: —

### Complementary Security Tools

These are not skill sources — they're scanners you can run alongside skill-scout's vetting checklist for deeper security analysis.

**Caterpillar (Alice)**
- URL: https://caterpillar.alice.io/
- What it does: Static skill scanner — inspects skill logic and configs for injection paths, unsafe tool access, and obfuscated behaviors
- Works with: Claude Skills, Cursor Rules, MCP configs
- When to use: During the file audit step on any Tier 3 source, or when a skill feels too good to be true

**MCP-Scan (Invariant Labs)**
- URL: https://github.com/invariantlabs-ai/mcp-scan
- What it does: Scans for prompt injection, tool poisoning, and toxic data flows across MCP servers and agent skills
- When to use: When a skill interacts with MCP servers or fetches external content

**Skill Scanner (Cisco AI Defense)**
- URL: https://github.com/cisco-ai-defense/skill-scanner
- What it does: Pattern-based detection (YARA rules) plus LLM-as-judge analysis for malicious code, prompt injection, and data exfiltration
- When to use: For deep automated analysis when manual file review isn't practical

**Nova-Proximity (Nova Hunting)**
- URL: https://github.com/Nova-Hunting/nova-proximity
- What it does: MCP and agent skills security scanner with NOVA detection rules
- When to use: When evaluating MCP-heavy skill packages

### Ecosystem Context

Skill marketplaces and curated lists for discovery (not vetted by this project — apply your own checklist):

- **SkillsMP** — https://skillsmp.com/ — Marketplace hosting 160k+ skills. Filters by minimum 2 stars but does not do security vetting.
- **Agent Skills Hub** — https://agentskillshub.dev/ — Security-first registry with automated code analysis. Worth cross-referencing.
- **awesome-agent-skills** — https://github.com/heilcheng/awesome-agent-skills — Community-curated list across Claude, Copilot, Cursor, Codex.
- **Superpowers** — https://github.com/obra/superpowers — Methodology + skills framework with 20+ battle-tested skills.
- **Claude Code Skill Factory** — https://github.com/alirezarezvani/claude-code-skill-factory — Toolkit for building production-ready skills.

### Tier 3: Watch List

Add individual repos and social media finds here. Template:

```
**[repo-name] ([author])**
- URL: [url]
- Category: [what it covers]
- Trust: Tier 3
- Notes: [why it's on the watch list, any concerns]
- Added: [YYYY-MM-DD]
- Last checked: —
```
