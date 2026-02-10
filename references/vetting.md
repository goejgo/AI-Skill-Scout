# Skill Vetting Checklist

A security-aware evaluation framework for AI skills sourced from community repositories.

## Quick Reject

Any of these → immediate reject, no scoring needed:

- No SKILL.md file
- Malicious or obfuscated code in any file
- Scripts that access credentials, environment variables, or sensitive paths
- Scripts that make network calls to unknown endpoints
- Base64-encoded content, minified code, or encoded strings in any file
- Files that reference external URLs for script loading or data exfiltration
- Prompt injection patterns: instructions disguised as data, role overrides, "ignore previous instructions"
- Description is vague or misleading about what the skill actually does

## Mandatory File Audit

**Before scoring begins**, run a full file audit on every file in the skill directory. This step is not optional — bundled files are the primary attack surface.

### Step 1: Inventory all files

```bash
find <skill-directory> -type f
```

Every file must be accounted for. Reviewing only SKILL.md is insufficient.

### Step 2: Flag non-markdown files

Any file that is not `.md` or `.txt` requires manual inspection:

- `.py`, `.sh`, `.js`, `.ts` → read every line, understand what it does
- `.json` → check for `command`, `exec`, `spawn`, `eval`, `require`, `import` fields
- `.yaml` / `.yml` → check for `run`, `script`, `command`, `hook` fields
- Binary files → reject unless clearly an asset (image, font) with a legitimate purpose

### Step 3: Check for hidden content in markdown

Even `.md` files can carry payloads:

- Embedded HTML with `<script>` tags or event handlers (`onclick`, `onload`)
- HTML comments containing encoded instructions
- Invisible Unicode characters or zero-width joiners
- Markdown links pointing to unexpected destinations
- Fenced code blocks that look like documentation but contain executable instructions

### Step 4: Human gate for executable content

**Skills containing ANY executable code — scripts, hooks, JSON with command fields — cannot be auto-adopted.** They must be:

1. Flagged in the vetting report with a complete file listing
2. Presented to a human reviewer with the code visible
3. Adopted only after explicit human approval

This is the critical control. Automated vetting handles quality assessment; human review handles security decisions for executable content.

## Scoring Checklist

Score each dimension 1–5.

- **20–25:** Adopt as-is. Copy to `vetted/`, remove from `incoming/`.
- **15–19:** Adopt with modifications. Document changes in `MODIFICATIONS.md`, then copy to `vetted/`.
- **Below 15:** Reject. Create `REJECTION.md` with scores and reasoning, move to `rejected/`.

### 1. Structure (1–5)

- Has YAML frontmatter with `name` and `description`
- Description is specific enough to trigger correctly (not vague or overly broad)
- Progressive disclosure: lean SKILL.md body, supporting detail in `references/`
- Resources organized logically (`scripts/`, `references/`, `assets/`)
- No extraneous files (stale READMEs, CHANGELOGs, unrelated configs)

### 2. Value (1–5)

- Adds a capability the AI assistant doesn't already have
- No significant overlap with already-adopted skills
- Knowledge is non-obvious — goes beyond generic advice anyone could give
- Saves real time or measurably improves quality on actual tasks
- Relevant to your defined scope (configure this per your needs)

### 3. Quality (1–5)

- Instructions are clear and actionable, not vague or aspirational
- Uses imperative or infinitive form ("Verify the input" not "You should consider verifying")
- Includes examples where they would help clarify the approach
- Gives the AI appropriate freedom — neither over-prescriptive nor under-specified
- Token-efficient: no padding, no redundant phrasing, no filler

### 4. Security (1–5)

- **5** = Pure markdown, no executable content of any kind
- **4** = Contains config files (JSON/YAML) with no command execution fields
- **3** = Contains scripts with clear, readable purpose and no external calls
- **2** = Contains scripts with external dependencies or network access (requires human gate)
- **1** = Contains obfuscated code, encoded strings, or unclear execution paths → reject

Additional security checks regardless of score:

- No network calls or filesystem access outside the skill library directory (the directory containing `vetted/`, `incoming/`, `rejected/`)
- No credential handling or environment variable access
- No `eval()`, `exec()`, `Function()`, `child_process`, `subprocess`, or dynamic code execution
- No fetching remote scripts or loading external modules at runtime
- Dependencies, if any, must be standard, well-known, and pinned to versions

### 5. Adaptability (1–5)

- Works in your runtime environment (Cowork VM, Claude Code CLI, Cursor, etc.)
- No hard-coded paths or platform-specific assumptions
- Modifiable without breaking core functionality
- Compatible with other skills (no naming conflicts, no contradictory instructions)
- Useful across multiple task types (not hyper-niche to one rare scenario)

## Supply Chain Risk

Star counts and repository popularity are social proof, not security audits.

- A compromised maintainer account can push malicious updates to a previously trusted repo
- High-star repos are higher-value targets for supply chain attacks, not lower-risk ones
- Skills distributed via social media (Twitter/X, Discord, Reddit) bypass any repo-level review
- "Trending" or "viral" skills warrant more scrutiny, not less
- If an upstream source reports a security incident, quarantine all skills from that source and re-vet before continued use

## Adopt With Modifications

When modifying community skills before adoption:

1. Strip executable scripts unless they provide critical value AND pass human security review
2. Rewrite vague descriptions to include clear trigger patterns
3. Cut bloat — apply the "does the AI actually need this paragraph?" test
4. Convert platform-specific instructions to your environment's equivalents
5. Document every change in `MODIFICATIONS.md` inside the skill directory

## Rejection Documentation

Create `REJECTION.md` inside the rejected skill's directory:

```markdown
# Rejected: [skill-name]
- **Source:** [URL]
- **Date:** YYYY-MM-DD
- **Scores:** Structure: X | Value: X | Quality: X | Security: X | Adaptability: X | Total: XX/25
- **File Audit:** [list all files found, flag any non-markdown]
- **Reason:** [1-2 sentences]
- **Revisit?** Yes / No — if yes, note what would need to change upstream
```
