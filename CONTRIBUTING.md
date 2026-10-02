# Contributing

## Skill contract

Each skill lives at `skills/<skill-name>/SKILL.md` and starts with frontmatter containing exactly `name` and `description`.

Keep names lowercase and hyphenated. The directory name and frontmatter `name` must match.

## Authoring guidelines

- Optimize the description for triggering, not marketing.
- Keep the body procedural and compact.
- Put long-lived shared context in `references/`.
- Prefer explicit inputs, stop conditions, and outputs.
- State safety boundaries next to the step where they matter.
- Do not duplicate architecture across multiple skills.
- Avoid secrets, real credentials, production tokens, and private test data in examples.
- Make success/failure observable so another agent can verify the result.

## Before opening a PR

Run `python scripts/validate_skills.py`.

For security skills, verify that examples default to local/QA and that cleanup never deletes audit evidence.
