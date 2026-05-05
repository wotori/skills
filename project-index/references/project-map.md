# Local Project Map

Snapshot date: 2026-05-05.

Root folders:

- `/Users/wotori/git/ekza` - Ekza, Omoba, Solana, Stellar, Bevy, and related experiments.
- `/Users/wotori/git/wotori` - Wotori Studio products and landing pages.
- `/Users/wotori/git/skills` - source folders for local Codex skills.

## High-Signal Projects

| User wording | Path | What it is | Usual checks |
| --- | --- | --- | --- |
| Omoba, O-MOBA, "омоба" | `/Users/wotori/git/ekza/omoba-bevy` | Authoritative-server MOBA prototype: Rust UDP server, Bevy client, shared skills crate. | `cargo build --workspace`; `cargo test --workspace`; `cargo fmt --all -- --check`; `python3 scripts/verify_task_02_multiplayer_session_flow.py`; `make verify-task-12` |
| Ekza Bevy, "экза bevy" | `/Users/wotori/git/ekza/ekza-bevy` | Old Bevy 0.6.1 NFText visualization prototype. | `cargo build`; `cargo test` |
| Ekza core | `/Users/wotori/git/ekza/core` | React/Vite/R3F/Rapier/Socket.IO client runtime for social 3D worlds, Solana profile/avatar integration. | `npm run ts:check`; `npm run build`; `npm run dev` |
| Wotori/Ekza/Omoba landing pages | `/Users/wotori/git/wotori/landing-v2` | Turborepo/pnpm monorepo for Wotori Studio, Ekza Space, O-MOBA, and dev hub Next.js apps. | `make type-check`; `make build`; `make dev`; app-specific `make dev-wotori`, `make dev-ekza`, `make dev-omoba` |
| Classical archive, OpusPrism | `/Users/wotori/git/wotori/classical-archive-mvp` | Classical music catalog prototype: FastAPI/Postgres/MinIO backend, Next.js frontend, Docker Compose. | `docker compose up --build`; backend pytest/Ruff/Black from `backend`; frontend `npm run dev` from `frontend` |
| Ekza Stellar UI | `/Users/wotori/git/ekza/ekza-stellar` | React 18 + Parcel + TypeScript frontend for Solana-backed project/asset/universe/release workflows. | `yarn valid`; `yarn build`; `yarn dev` |
| Solana Stellar | `/Users/wotori/git/ekza/solana-stellar` | Anchor protocol for collaborative asset universes on Solana. | `anchor test`; `yarn lint` |
| Solana Avatars | `/Users/wotori/git/ekza/solana-avatars` | Anchor/avatar NFT identity programs and app/sdk folders. | `anchor test` if configured; `yarn lint`; check README/Makefile first |
| Solana Donations | `/Users/wotori/git/ekza/solana-donations` | Anchor protocol for Solana project donations and donor stats. | `make build`; `make test`; `yarn build`; avoid deploy without approval |
| Solana Ekza Space | `/Users/wotori/git/ekza/solana-ekza-space` | Anchor program for finite numbered Spaces as Metaplex NFTs. | `anchor test`; `yarn build`; `yarn lint` |
| Solana Users | `/Users/wotori/git/ekza/solana-users` | Anchor user profile/social graph smart contracts. | `make build`; `make test`; `yarn lint` |
| Ekza Radio | `/Users/wotori/git/ekza/ekza-radio` | Rust workspace with news-service and news-translator, OpenAI/ElevenLabs/Tavily driven media generation. | `cargo test --workspace`; `make test`; service commands in README |

## Ekza Folder

### `/Users/wotori/git/ekza/EkzaBot`

Python-style bot repository with `src/` and `.venv/`. Inspect local files before choosing commands.

### `/Users/wotori/git/ekza/NFText`

Next.js dApp for text/image/3D NFT minting, IPFS/Pinata, CW20/CW721/marketplace flows, and Archway/CosmWasm-era NFText concepts.

Important files:

- `package.json` name: `nftext`
- scripts include `dev`, `build`, `start`
- `README.md` documents required `.env` values and smart contracts

### `/Users/wotori/git/ekza/bubblegum`

Node/TypeScript CLI playground for Solana compressed NFT minting with Bubblegum v2.

Important files:

- `package.json` name: `solana-minter`
- `Makefile` targets: `check-ts`, `get-address`, `get-balance`, `npm-create-tree`, `npm-mint-cnft`, `npm-inspect-tree`
- Scripts live in `scripts/`

### `/Users/wotori/git/ekza/cc0-assets-nft`

CC0 3D asset collection for NFT/platform use. Main content is under `models/`. Treat as asset library rather than app code.

### `/Users/wotori/git/ekza/core`

Ekza Core web client foundation for social 3D worlds.

Stack and layout:

- React, Vite, React Three Fiber, Rapier, Socket.IO, Solana wallet/profile integration.
- `src/components/ekza.tsx` app shell.
- `src/features/profile/useUserProfile.ts` profile/avatar loading.
- `src/features/realtime/useRealtimeSession.ts` Socket.IO sessions.
- `src/features/chat/useWorldChat.ts` chat state.
- `sdk/` Anchor client wrapper for Solana user profile program.
- `supabase/` and `api/` exist; inspect before backend changes.

Commands:

- `npm run dev`
- `npm run ts:check`
- `npm run build`
- `npm run preview`
- `make ts-check`

### `/Users/wotori/git/ekza/cw-stellar`

CosmWasm/Archway workspace with `contracts/*`.

Commands from local docs:

- `archway build --optimize`
- `archway store`
- `archway instantiate`
- `archway metadata`

### `/Users/wotori/git/ekza/ekza-bevy`

Old Bevy visualization prototype for NFText.

Important files:

- `Cargo.toml` package: `ekza-bevy-engine`
- Bevy dependency: `0.6.1`
- `src/`, `assets/`, `index.html`

Commands:

- `cargo build`
- `cargo run`
- README also documents wasm build with `wasm32-unknown-unknown` and `wasm-bindgen`

Known note from 2026-05-05: on macOS SDK 26.2 with Rust 1.93.1, `cargo build` failed in `coreaudio-sys v0.2.9` bindgen/proc-macro2 while processing `MacTypes.h`. Reverify before assuming this still fails.

### `/Users/wotori/git/ekza/ekza-bot`

Rust 2024 package `ekza-bot`. Inspect `Cargo.toml` and `src/` before running.

### `/Users/wotori/git/ekza/ekza-radio`

Rust workspace:

- `crates/news-common`
- `crates/news-service`
- `crates/news-translator`

Purpose:

- Collect news, write scripts, translate, generate MP3, store artifacts.
- Requires `.env` for `TAVILY_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`.

Commands:

- `cargo test --workspace`
- `make test`
- `RUST_LOG=info cargo run -p news-service`
- `cargo run -p news-translator -- ./config/translator.toml`

### `/Users/wotori/git/ekza/ekza-rust-server`

Rust server package `ekza-rust-server`.

Makefile targets:

- `build`, `run`, `dev`, `check`, `test`, `fmt`, `lint`
- distribution/deployment targets exist: `linux-release`, `dist-bin`, `docker-image`, `docker-run`, `docker-up`, `docker-save`, `deploy`

Avoid deploy/docker production paths without approval.

### `/Users/wotori/git/ekza/ekza-server`

Archived Node server.

README says code moved to the Ekza repo. Treat as legacy unless the user names it directly.

### `/Users/wotori/git/ekza/ekza-server-rust`

Rust package named `server`.

Makefile targets:

- `check`, `fmt`, `clippy`, `server`, `bridge`, `bot`, `kill`, `restart`

### `/Users/wotori/git/ekza/ekza-space-ui`

Vite UI package `ekza-space-ui`.

Commands:

- `npm run dev`
- `npm run build`
- `make build-anchor-ts`

### `/Users/wotori/git/ekza/ekza-stellar`

React + Parcel frontend for Ekza Stellar Solana asset/universe workflow.

Stack:

- React 18, React Router, TypeScript, Parcel.
- Solana Web3, Anchor, wallet adapter.
- Tailwind, Three.js, React Three Fiber.

Source boundaries:

- `src/blockchain` owns frontend blockchain provider and `useBlockchain`.
- `src/contracts/solana` has Solana-specific client/Anchor helpers/IDL.
- `src/contracts/entities` has project and asset contract surface.
- `src/contracts/universes` has universe contract surface.
- `src/pages` route-level screens.
- `src/components` reusable UI.
- `src/config/constants.ts` shared constants.

Commands:

- `yarn dev`
- `yarn build`
- `yarn valid`
- `yarn start`

### `/Users/wotori/git/ekza/landing`

Ekza landing pages, Parcel-style outputs and Makefile for variants.

Makefile targets:

- `dev-w`, `dev-e`, `dev-both`
- `open-w`, `open-e`, `open-both`

### `/Users/wotori/git/ekza/omoba-bevy`

Authoritative-server MOBA prototype.

Stack:

- Rust workspace, edition 2024.
- Workspace members: `client`, `server`, `skills`.
- Bevy client, Rust UDP authoritative server.

Important docs:

- `README.md`
- `RUNBOOK.md`
- `docs/playtest-script.md`
- `docs/bug-report-template.md`
- `docs/mvp-scope-and-limitations.md`
- `tasks/MVP-CHECKLIST.md`
- `AGENTS.md` has proof-loop instructions for substantial implementation work.

Commands:

- `cargo build --workspace`
- `cargo test --workspace`
- `cargo fmt --all -- --check`
- `cargo clippy --workspace --all-targets -- -D warnings` may expose many client warnings; do not treat as equivalent to build failure.
- `make server`
- `make game`
- `make start`
- `make stop`
- `make verify-task-12`
- `python3 scripts/verify_task_02_multiplayer_session_flow.py`

Known note from 2026-05-05: `cargo build --workspace`, `cargo test --workspace`, fmt check, `verify_task_02_multiplayer_session_flow.py`, and `make verify-task-12` passed. Strict clippy failed on existing warnings such as `too_many_arguments`, `type_complexity`, `collapsible_if`, and `unnecessary_map_or`.

### `/Users/wotori/git/ekza/omoba-bevy-archive`

Archived earlier Omoba Bevy crate named `omoba`. Prefer active `omoba-bevy` unless the user explicitly asks for the archive.

## Solana / Anchor Contracts Index

Use this table when the user asks about "contracts", "programs", Solana, Anchor, IDLs, SDK generation, or deployment/test commands.

| Repository | Program crates | Program IDs from `Anchor.toml` | Default cluster | Notes |
| --- | --- | --- | --- | --- |
| `/Users/wotori/git/ekza/solana-avatars` | `programs/avatars`, `programs/minter` | localnet/devnet `solana_avatars = 56kfTdE1xmCkZ2eDuikD7S5Mr15nmdzQENDWfmdMVtt`; `minter = 29KLLArkfCfRGPgTh4k4qzXvR2JkkXfRnnNZTKn54TKz` | devnet | Avatar identity and avatar NFT minting. Has `app/`, `sdk/`, `scripts/`, `tests/`. |
| `/Users/wotori/git/ekza/solana-donations` | `programs/solana-donations` | localnet `solana_donations = 7XhmW42LmPuk2gcHjjsDwGiTurWDrUFP9yff9AK4mkB4` | localnet | Donation protocol: projects, donors, top-10 stats, project treasury flow. |
| `/Users/wotori/git/ekza/solana-ekza-space` | `programs/ekza-space` | localnet `solana_ekza_space = Bms233NNbKb5FAcsjCmmCAU98oCuBXwLrLXNE5sBRdbb` | localnet | Finite numbered Spaces as Metaplex NFTs plus PDA settings. |
| `/Users/wotori/git/ekza/solana-stellar` | `programs/solana-stellar` | localnet `solana_stellar = 3rVXfq7LLSLqbDzvZuSrQoMytwczLj2Q8Hue62rxPZAA` | localnet | Collaborative asset universes: assets, lineage, releases, contributor shares. |
| `/Users/wotori/git/ekza/solana-users` | `programs/users`, `programs/avatars` | devnet `users = Dpn8XGzXTGErx71SDLxuzVCDwJDKF79sE42r9qoY5Wpf`; devnet `avatars = DN2ho2mgKdvsYjnxMZNcpQabJwcGeYTYwAyX2CdkHnd9`; localnet `users = Dpn8XGzXTGErx71SDLxuzVCDwJDKF79sE42r9qoY5Wpf` | devnet | User profile/social graph contracts. Be careful: provider defaults to devnet. |

Safe checks for Anchor repositories:

- Start with `git status --short --branch`, `Anchor.toml`, `Cargo.toml`, `package.json`, and README.
- Prefer `anchor test`, `yarn lint`, `make build`, or repo-specific `make test`.
- Do not run `anchor deploy`, `make deploy`, wallet mutation, validator reset, or test-ledger deletion without explicit user approval.

### `/Users/wotori/git/ekza/solana-avatars`

Anchor/Solana avatar NFT identity project with `app/`, `programs/`, `sdk/`, `scripts/`, `tests/`, and `migrations/`.

README describes:

- `avatar` program: stores user data and links to avatar NFTs.
- `minter` program: publishing and minting NFT-based avatars.

Commands:

- Check `Makefile`, `Anchor.toml`, and README before running.
- `yarn lint` exists.

### `/Users/wotori/git/ekza/solana-donations`

Anchor protocol for Solana donations.

Program ID:

- `7XhmW42LmPuk2gcHjjsDwGiTurWDrUFP9yff9AK4mkB4`

Concepts:

- Project owner creates projects.
- Donors send SOL to project treasury.
- Protocol tracks donor stats and top 10.
- Protocol fee on donation is 0; creation fee is controlled by config.

Commands:

- `make build`
- `make build-all`
- `make test`
- `yarn build`
- `yarn lint`

Avoid `make deploy`, `make build-deploy`, validator resets, and wallet changes without explicit approval.

### `/Users/wotori/git/ekza/solana-ekza-space`

Anchor program for finite numbered "Spaces", each represented by a Metaplex NFT plus PDA settings.

Program:

- name: `solana_ekza_space`
- localnet ID: `Bms233NNbKb5FAcsjCmmCAU98oCuBXwLrLXNE5sBRdbb`

Commands:

- `anchor test`
- `yarn build`
- `yarn lint`

### `/Users/wotori/git/ekza/solana-stellar`

Anchor protocol for collaborative asset universes on Solana.

Concepts:

- Universe, Asset, Lineage, Release, Release Vault, Contributor Share.
- Intended downstream consumer: `solana-avatars`.

Command:

- `anchor test`
- `yarn lint`

### `/Users/wotori/git/ekza/solana-users`

Anchor user profile/social graph smart contracts.

Programs:

- devnet `avatars`: `DN2ho2mgKdvsYjnxMZNcpQabJwcGeYTYwAyX2CdkHnd9`
- devnet/localnet `users`: `Dpn8XGzXTGErx71SDLxuzVCDwJDKF79sE42r9qoY5Wpf`

Provider defaults to devnet in `Anchor.toml`; be careful before running commands that mutate chain state.

Commands:

- `make build`
- `make test`
- `yarn lint`

## Wotori Folder

### `/Users/wotori/git/wotori/classical-archive-mvp`

OpusPrism.app, a full prototype for a classical music catalog.

Stack:

- Backend: Python 3.11, FastAPI, SQLAlchemy 2.0 async, Alembic, PostgreSQL, MinIO, pytest, Ruff, Black.
- Frontend: Next.js 14 App Router, TypeScript, Tailwind, React Hook Form, React Dropzone, SWR, framer-motion.
- Infra: Docker Compose with Postgres, MinIO, backend, frontend, minio-mc.

Layout:

- `backend/`
- `frontend/`
- `mobile/`
- `docker-compose.yml`
- `.env.example`

Commands:

- Full stack: `docker compose up --build`
- Backend local: create venv, `pip install -e .`, `alembic upgrade head`, `uvicorn app.main:app --reload`
- Frontend local: `cd frontend && npm install && npm run dev`

Ports from README:

- `http://localhost:3000` frontend/admin
- `http://localhost:8000` FastAPI
- `http://localhost:9101` MinIO Console
- `http://localhost` nginx same-origin entrypoint

### `/Users/wotori/git/wotori/landing-v2`

Turborepo/pnpm monorepo for Wotori Studio public-facing pages.

Apps:

- `apps/wotori` - Wotori Studio landing page.
- `apps/ekza` - Ekza Space landing page.
- `apps/omoba` - O-MOBA landing page.
- `apps/dev-hub` - local dev hub with links.

Packages:

- `packages/ui` - shared shadcn/ui component library.
- `packages/locales` - translations and i18n utilities.
- `packages/config` - shared TypeScript, ESLint, Tailwind config.
- `packages/analytics` - analytics package.

Commands:

- `pnpm install`
- `pnpm dev`
- `pnpm build`
- `pnpm lint`
- `make dev`
- `make dev-wotori` on port 3000
- `make dev-ekza` on port 3001
- `make dev-omoba` on port 3002
- `make dev-hub` on port 3999
- `make type-check`
- `make validate`

## Skills Folder

### `/Users/wotori/git/skills/lossless-to-mp3`

Codex skill for converting lossless audio albums/tracks to MP3.

It has:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/convert_lossless_to_mp3.sh`
- `scripts/cue_to_mp3.py`

### `/Users/wotori/git/skills/project-index`

This skill. Update this map when project paths, commands, or notable repo state changes.

## Search Hints

Use these search commands from `/Users/wotori`:

```sh
find git/ekza git/wotori -maxdepth 2 -name .git -type d | sed 's#/.git$##' | sort
find git/ekza git/wotori -maxdepth 2 \( -name package.json -o -name Cargo.toml -o -name README.md -o -name Makefile -o -name Anchor.toml \) | sort
```

Use these repository-local checks before edits:

```sh
git status --short --branch
rg --files -g 'AGENTS.md' -g 'README*' -g 'Makefile' -g 'Cargo.toml' -g 'package.json' -g 'Anchor.toml'
```
