---
name: project-index
description: Local repository map for Wotori, Ekza, Omoba, Solana, Stellar, Bevy, landing pages, and studio infrastructure under /Users/wotori/git. Use when Codex needs to locate one of the user's local projects, identify the correct repository before editing, choose likely build/test/dev commands, or understand how git/ekza and git/wotori are organized without asking the user to repeat paths.
---

# Project Index

Use this skill before changing or diagnosing projects under:

- `/Users/wotori/git/ekza`
- `/Users/wotori/git/wotori`
- `/Users/wotori/git/skills`

Read `references/project-map.md` when you need the project list, stack, common commands, or repository notes.

## Workflow

1. Match the user's wording to the project map. Russian spellings and shorthand are common: "омоба" usually means `omoba-bevy`, "экза" may mean `ekza-bevy`, `core`, `ekza-stellar`, or a landing page depending on context.
2. Prefer the specific repository's own `README.md`, `AGENTS.md`, `Makefile`, `Cargo.toml`, `package.json`, `Anchor.toml`, and task docs after selecting a candidate.
3. Check `git status --short --branch` before edits. Many folders are independent git repositories, not one monorepo.
4. Ignore generated/vendor directories while searching unless the task explicitly targets them: `node_modules`, `target`, `dist`, `build`, `.next`, `.turbo`, `.parcel-cache`, `.anchor`, `.venv`, `.git`.
5. Run the smallest relevant verification command from the map or from local repo docs. Do not assume a command works across all projects.

## Safety Notes

- Do not modify secrets, `.env` values, wallet files, deployment settings, or production infrastructure without explicit user approval.
- For Solana/Anchor projects, avoid `deploy`, validator resets, wallet changes, and test-ledger deletion unless the user asks.
- For repo-index maintenance, update `references/project-map.md` when new local projects appear or commands change.
