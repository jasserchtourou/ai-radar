# AI Radar — Step-by-Step TODO

Stack: FastAPI (async) · SQLAlchemy 2.x ORM (async, asyncpg) · Alembic · PostgreSQL · pytest · Ruff · mypy · Docker

Decisions: statuses = ARCHIVED (keep for later) / DECLINED; PENDING inferred (no row) ·
a note archives the item · email buttons Open/Archive/Decline · "never resend" enforced by DB ·
bigint identity IDs · deployment platform decided in Milestone 10.

Rule: finish a step, run its check, then tick it. One step = one small commit.

---

## Milestone 1 — Project setup

- [x] 1.1 `git init`, `.gitignore` (Python, `.env`, `.venv`, `__pycache__`)
- [x] 1.2 `backend/pyproject.toml` with deps: fastapi, uvicorn, sqlalchemy[asyncio], asyncpg, alembic, pydantic-settings, httpx; dev: pytest, pytest-asyncio, ruff, mypy
- [x] 1.3 Folder skeleton: `app/{api,core,db,models,schemas,services,ingestion,jobs}`, `tests/{unit,integration,api}`
- [x] 1.4 `app/core/config.py` — `Settings` via pydantic-settings; `.env.example`
- [ ] 1.5 `app/main.py` — app factory + `GET /health`
      ✔ check: `uvicorn app.main:app` → `/health` returns `{"status":"ok"}`
- [ ] 1.6 `docker-compose.yml` (postgres + api) and `Dockerfile`
      ✔ check: `docker compose up` → health works, `psql` connects
- [ ] 1.7 `app/db/session.py` — `create_async_engine`, `async_sessionmaker`, `get_db` dependency
- [ ] 1.8 `app/db/base.py` — `DeclarativeBase` + naming convention for constraints (important for Alembic)
- [ ] 1.9 `GET /ready` — runs `SELECT 1` through the async session
- [ ] 1.10 Alembic init with async template (`alembic init -t async`), wire `target_metadata`
      ✔ check: `alembic revision -m "empty"` + `alembic upgrade head` works
- [ ] 1.11 pytest setup: test DB, async fixtures, per-test transaction rollback
      ✔ check: a test for `/health` and `/ready` passes
- [ ] 1.12 Ruff + mypy config, run clean
- [ ] 1.13 GitHub Actions CI: ruff, mypy, pytest against a Postgres service container

## Milestone 2 — Database schema (ORM models + migrations)

- [ ] 2.1 Mixin for `created_at` / `updated_at` (timestamptz)
- [ ] 2.2 Model `User` (+ `lower(email)` unique index)
- [ ] 2.3 Model `Session`
- [ ] 2.4 Model `Source` (type CHECK, quality CHECK)
- [ ] 2.5 Model `IngestionRun`
- [ ] 2.6 Model `Discovery` (3 unique rules incl. partial index, `search_vector` generated column + GIN)
- [ ] 2.7 Models `Tag` + `DiscoveryTag` (+ reverse index)
- [ ] 2.8 Model `UserDiscovery` (composite PK, status CHECK, library index)
- [ ] 2.9 Models `Digest` + `DigestItem` (unique period, sent_at CHECK, composite FK)
- [ ] 2.10 Generate migration → **read it line by line** → fix what autogenerate missed (triggers, generated column)
- [ ] 2.11 `updated_at` trigger in migration
- [ ] 2.12 DB tests: each constraint rejects bad data (duplicate URL, bad status, resend same item…)
- [ ] 2.13 Seed script: user (CLI, hashed password) + initial sources
- [ ] 2.14 `docs/database.md` + ADRs 001–002

## Milestone 3 — Basic API + auth

- [ ] 3.1 Error format + exception handlers (404/409/422/500, no stack traces)
- [ ] 3.2 Password hashing (argon2) + login/logout endpoints, HttpOnly session cookie
- [ ] 3.3 `current_user` dependency
- [ ] 3.4 Pagination schema (`limit`/`offset`, max limit)
- [ ] 3.5 `GET /api/v1/sources`, `GET /api/v1/tags`
- [ ] 3.6 `GET /api/v1/discoveries` (+ filters: source, tag, date, search) and `GET /{id}`
- [ ] 3.7 API tests (auth required, pagination, filters)
- [ ] 3.8 ADR 003 — authentication

## Milestone 4 — Ingestion

- [ ] 4.1 `RawItem` / `NormalizedItem` schemas + `SourceAdapter` Protocol
- [ ] 4.2 URL normalization + unit tests
- [ ] 4.3 RSS adapter (httpx + feedparser), tests with fixture XML
- [ ] 4.4 GitHub adapter (search API, token, rate-limit handling), mocked tests
- [ ] 4.5 Retry/backoff/timeout helper
- [ ] 4.6 Rule-based tagging + categorization
- [ ] 4.7 Insert with `ON CONFLICT DO NOTHING RETURNING` → counts
- [ ] 4.8 Ingestion service: sources in parallel, failures isolated, `ingestion_runs` recorded, structured logs
- [ ] 4.9 Integration test: fetch → normalize → dedup → save (run twice → 0 new)
- [ ] 4.10 ADR 005 — deduplication

## Milestone 5 — Ranking

- [ ] 5.1 Score components (recency, source quality, relevance, github signal, novelty) as pure functions
- [ ] 5.2 Configurable weights + `score_version`
- [ ] 5.3 Scoring job for unscored discoveries, breakdown stored
- [ ] 5.4 Unit tests for each component + total

## Milestone 6 — User feedback

- [ ] 6.1 State machine (allowed transitions) + unit tests
- [ ] 6.2 `POST /discoveries/{id}/archive|decline` + `DELETE /discoveries/{id}/status` (undo) — idempotent upsert
- [ ] 6.3 Notes endpoint (auto-archive)
- [ ] 6.4 `GET /library` (archived, with search) + `GET /library/declined`
- [ ] 6.5 Inbox query (sent but not acted on)
- [ ] 6.6 API tests

## Milestone 7 — Digest

- [ ] 7.1 Candidate selection + personalization (tag/source save rates)
- [ ] 7.2 Digest creation in one transaction (unique period)
- [ ] 7.3 "Why it matters" template text
- [ ] 7.4 Email HTML template
- [ ] 7.5 Signed action tokens + confirmation page (GET never mutates)
- [ ] 7.6 Resend client with idempotency key; claim → send → record
- [ ] 7.7 Tests: double run = one email; crash after send = no duplicate
- [ ] 7.8 `GET /api/v1/digests`, `/digests/{id}`

## Milestone 8 — Scheduling

- [ ] 8.1 `python -m app.jobs daily` CLI
- [ ] 8.2 `POST /internal/jobs/daily` protected by secret
- [ ] 8.3 "Is digest due?" logic + resume unsent digests
- [ ] 8.4 Concurrency test (two runs at once)
- [ ] 8.5 ADR 004 — scheduling

## Milestone 9 — Frontend (Next.js + TS + Tailwind)

- [ ] 9.1 Setup + `/api` rewrite proxy to backend
- [ ] 9.2 Login, inbox, discovery detail, library, search, digests pages

## Milestone 10 — Deployment

- [ ] 10.1 Neon DB (pooled URL, `statement_cache_size=0`), run migrations
- [ ] 10.2 Backend container deploy
- [ ] 10.3 Frontend on Vercel
- [ ] 10.4 Resend domain + cron trigger
- [ ] 10.5 End-to-end production check + `docs/deployment.md`
