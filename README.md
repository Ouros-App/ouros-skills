# Ouros Skills

> Reusable, low-context skills for Codex and agent harnesses used by the Ouros project.

[![CI/CD](https://github.com/Ouros-App/ouros-skills/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Ouros-App/ouros-skills/actions/workflows/ci-cd.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What this repository is

`ouros-skills` contains focused skills that teach agents **how to work safely and consistently** on Ouros workflows without stuffing every session with a giant system prompt.

The repository favors progressive disclosure:

1. skill metadata stays tiny and trigger-focused;
2. `SKILL.md` contains only the execution workflow;
3. shared architecture/policy lives in `references/` and is loaded only when needed.

## Security audit suite

| Skill | Purpose |
| --- | --- |
| [`ouros-security-audit`](skills/ouros-security-audit/SKILL.md) | Coordinates a full, evidence-driven security audit and delegates work by attack surface. |
| [`safe-runtime-testing`](skills/safe-runtime-testing/SKILL.md) | Runs non-destructive QA/local probes with fixtures, rollback and cleanup verification. |
| [`ouros-ai-security`](skills/ouros-ai-security/SKILL.md) | Reviews MIDAS, MCP, tool authorization, prompt injection boundaries and cross-user isolation. |
| [`finding-verifier`](skills/finding-verifier/SKILL.md) | Reproduces findings independently, rejects false positives and produces regression-ready evidence. |

Shared project boundaries live in [`references/ouros-security-model.md`](references/ouros-security-model.md).

## Install

The audit skills use a shared reference, so install the repository structure as a unit instead of copying only the skill directories.

### Codex user skills

```bash
git clone https://github.com/Ouros-App/ouros-skills.git
mkdir -p ~/.codex/ouros-skills
cp -R ouros-skills/skills ouros-skills/references ~/.codex/ouros-skills/
ln -sfn ~/.codex/ouros-skills/skills ~/.codex/skills/ouros
```

The relative paths used by the skills remain valid because `skills/` and `references/` stay side by side.

### Repository-local skills

Copy both directories together:

```text
your-repo/
└── .codex/
    └── ouros-skills/
        ├── skills/
        └── references/
```

Then expose the skill directories from that bundle to your harness. Do not copy a single `SKILL.md` without its shared references.

## Recommended autonomous topology

```text
Security Lead
  └─ ouros-security-audit
       ├─ Runtime Tester -> safe-runtime-testing
       ├─ AI/MCP Tester -> ouros-ai-security
       └─ Verifier      -> finding-verifier
```

The lead discovers and prioritizes. Runtime testing is gated. Verification is independent. A finding is never confirmed merely because another agent claimed it exists.

## Design rules

- One skill, one responsibility.
- Prefer short decision rules over encyclopedic checklists.
- Read shared references only when relevant.
- Never make production the default test target.
- Preserve audit logs. Cleanup removes test-created state; it does not hide evidence.
- Require reproducible evidence and a concrete affected boundary for findings.
- Destructive, persistence, availability, and third-party tests require separate explicit authorization.

## Repository layout

```text
.
├── skills/
│   ├── finding-verifier/
│   ├── ouros-ai-security/
│   ├── ouros-security-audit/
│   └── safe-runtime-testing/
├── references/
│   └── ouros-security-model.md
├── scripts/
│   └── validate_skills.py
└── .github/workflows/
    └── ci-cd.yml
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Every skill must pass `python scripts/validate_skills.py`.

Security issues should follow [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
