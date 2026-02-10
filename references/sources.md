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

### Tier 3: Watch List

Add individual repos and social media finds here. Template:

```
**[repo-name] ([author])**
- URL: [url]
- Category: [what it covers]
- Trust: Tier 3
- Notes: [why it's on the watch list, any concerns]
- Added: [date]
- Last checked: —
```
