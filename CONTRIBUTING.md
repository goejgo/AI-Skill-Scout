# Contributing

Thanks for your interest in improving skill-scout. This project benefits from people who work with AI skills daily and see the gaps firsthand.

## What We Need

**Security improvements** are the highest priority. The vetting checklist in `references/vetting.md` is the core of this project. If you've encountered an attack pattern, evasion technique, or supply chain risk that the checklist doesn't cover, that's the most valuable contribution you can make.

**New skill sources** for `references/sources.md` — if you've found a repository or community that produces quality skills, add it with the appropriate trust tier and any notes about what to watch for.

**Vetting checklist refinements** — if a scoring dimension is too vague, a threshold is wrong, or a step is missing, propose a change. Real-world experience with the checklist matters more than theory.

**Inventory script improvements** — `scripts/inventory.py` is intentionally simple. Bug fixes, better detection patterns, and edge case handling are welcome. Feature creep is not — the script should stay readable and auditable.

## How to Contribute

1. **Open an issue first** for anything non-trivial. Describe the problem or gap before proposing a solution.
2. **Fork and branch.** One change per pull request.
3. **Explain your reasoning.** The "why" matters more than the "what" — especially for security changes.

## What We Won't Accept

- Skills themselves. This is a framework for evaluating skills, not a skill library.
- Executable code beyond `inventory.py` without strong justification. The project's security posture depends on being mostly markdown.
- Automated integrations that phone home, collect telemetry, or require API keys.
- Changes that make the framework specific to one platform. skill-scout should stay portable.

## Code of Conduct

Be direct, be constructive, be honest. If you think something is wrong, say so with evidence. Skip the pleasantries and get to the point — that's how this project was built.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
