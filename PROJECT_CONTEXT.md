# AI Radar — Backend Engineering Project

## 1. Project Purpose

I want to build a personal platform called **AI Radar**.

The purpose is simple:

Every 3 days, the system should discover the most interesting NEW developments in AI and send me a short email digest containing approximately 5 high-value discoveries.

The email should be extremely concise.

Example:

---

### OpenClaw introduces X

Short 1–2 sentence explanation of what changed and why it might matter.

[Read more]

---

When I click an item, I should be able to open my web application and see the complete information:

* title
* short summary
* source
* original URL
* GitHub repository if available
* documentation if available
* publication date
* discovery date
* category
* tags
* why it may matter
* related projects
* personal notes

I should then be able to:

* Save
* Archive
* Decline
* Re-open later
* Search my saved/archived discoveries
* Add personal notes

The frontend is NOT my main learning objective.

Claude should build a functional and clean frontend, but the primary engineering focus of this project is:

> **Backend engineering + databases + APIs + data ingestion + architecture + reliability + deployment.**

---

# 2. VERY IMPORTANT — Learning Objective

I am an AI Engineer / aspiring strong Backend Engineer.

I already have experience with Python, FastAPI, Django, APIs, AI/LLM systems, RAG and related technologies.

However, I want to become much stronger at **real backend engineering**.

Therefore, this project must NOT be built as a quick prototype where everything is abstracted away.

I want to understand:

* how a production backend is structured
* how databases are designed
* relational modeling
* SQL
* PostgreSQL
* indexes
* constraints
* transactions
* migrations
* REST API design
* authentication
* authorization
* background jobs
* scheduling
* queues if appropriate
* retries
* idempotency
* caching
* pagination
* filtering
* validation
* error handling
* logging
* testing
* integration testing
* external APIs
* rate limiting
* security
* deployment
* observability
* configuration management
* Docker
* CI/CD

The goal is NOT just to finish the application.

The goal is:

> **Finish the application while becoming significantly better at backend engineering.**

---

# 3. How Claude Should Work With Me

Claude should behave as:

1. Senior Backend Engineer
2. Technical mentor
3. Code reviewer
4. Architecture reviewer
5. Pair programmer

Do NOT blindly implement everything without explanation.

For important architectural decisions:

1. Explain the problem.
2. Explain the possible approaches.
3. Explain which approach we are choosing.
4. Explain why.
5. Then implement it.

For example, if we need to store discovery status, explain:

* enum vs string
* database constraint
* state transitions
* indexing implications
* why we choose one approach

Then implement it.

---

# 4. Learning Mode

For important backend concepts, explain them briefly before implementation.

Use this format when appropriate:

### Concept

What are we solving?

### Options

What are the common approaches?

### Decision

What are we using?

### Why?

Why is this appropriate for this project?

### Implementation

Show/build the implementation.

### What I should understand

List the 2–5 things I should remember.

Do not over-explain trivial syntax.

I want practical engineering knowledge, not a Python beginner course.

---

# 5. Technology Stack

## Backend

Python 3.12+

FastAPI

Pydantic v2

SQLAlchemy 2.x

Alembic

PostgreSQL

pytest

httpx

Ruff

mypy where useful

Docker

Docker Compose for local development

---

# 6. Frontend

The frontend is secondary.

Use:

Next.js

TypeScript

Tailwind CSS

A simple clean dashboard.

The frontend should consume the FastAPI backend through REST APIs.

Do not spend excessive development time polishing animations or visual details.

Prioritize backend correctness.

---

# 7. Deployment Goal

The final system should be deployable without owning a VPS.

Preferred architecture:

Frontend:
Vercel

Backend:
A platform compatible with FastAPI/container deployment.

Database:
Managed PostgreSQL such as Supabase/Neon/etc.

Email:
Resend or another suitable email provider.

Scheduling:
A cloud scheduler / cron mechanism.

Important:

Do NOT design the backend around a permanent local process.

The system must work correctly when deployed in a serverless/cloud environment.

Background jobs must therefore be designed appropriately.

---

# 8. No Paid AI API Initially

VERY IMPORTANT:

The initial version must NOT require OpenAI, Anthropic, Gemini, or another paid AI API.

I want to build the first version without an LLM.

The system should use deterministic algorithms and external data sources.

Later, AI summarization can be added as an optional extension.

This is intentional.

I want to learn backend engineering first.

---

# 9. Core System

The system should perform this pipeline:

```text
External Sources
       ↓
Ingestion
       ↓
Normalization
       ↓
Deduplication
       ↓
Enrichment
       ↓
Scoring
       ↓
Selection
       ↓
Database
       ↓
Email Digest
       ↓
User Feedback
       ↓
Personalized Ranking
```

---

# 10. Sources

Initial sources should include:

## RSS / Websites

Use RSS feeds whenever possible.

Possible categories:

* AI research
* AI engineering
* AI agents
* LLMs
* developer tools
* open-source AI
* infrastructure

Do not scrape websites unnecessarily when RSS/API access exists.

---

## GitHub

Use the GitHub API.

Look for:

* new repositories
* significant releases
* rapidly developing projects
* repositories relevant to AI engineering
* agent frameworks
* LLM infrastructure
* developer tools

Examples of technologies/categories:

* LangGraph
* MCP
* OpenClaw
* Hermes
* OpenHands
* coding agents
* inference frameworks
* vector databases
* evaluation frameworks
* agent infrastructure

These are examples, not a hardcoded list.

---

# 11. Source Abstraction

Do NOT hardcode all ingestion logic into one giant function.

Create an abstraction such as:

```python
class SourceAdapter(Protocol):
    async def fetch(self) -> list[RawItem]:
        ...
```

Possible implementations:

```text
RSSSource
GitHubSource
```

Later:

```text
ArxivSource
HackerNewsSource
ProductHuntSource
...
```

The system should be extensible.

---

# 12. Data Pipeline

Every external item should pass through a predictable pipeline.

## Step 1 — Fetch

Retrieve raw external data.

## Step 2 — Normalize

Convert different source formats into a common internal structure.

Example:

```python
NormalizedItem(
    title=...,
    description=...,
    url=...,
    source=...,
    published_at=...,
    github_url=...,
)
```

## Step 3 — Deduplicate

Do not insert duplicate discoveries.

Possible deduplication signals:

* canonical URL
* normalized URL
* external source ID
* GitHub repository ID
* content hash where appropriate

The database must enforce uniqueness where possible.

Do NOT rely only on Python checks.

---

# 13. Database Design

Use PostgreSQL.

Start by designing the relational model before writing endpoints.

Potential entities:

```text
User

Source

Discovery

Tag

DiscoveryTag

UserDiscovery

Digest

DigestItem

UserPreference
```

Do not blindly copy this schema.

Analyze whether every entity is necessary.

---

# 14. Suggested Initial Schema

## users

```text
id
email
password_hash / auth identifier
created_at
updated_at
```

---

## sources

```text
id
name
type
url
active
created_at
updated_at
```

Examples:

```text
GitHub
RSS
ArXiv
```

---

## discoveries

```text
id
source_id
external_id
title
description
canonical_url
github_url
published_at
discovered_at
score
metadata
created_at
updated_at
```

Important:

`external_id` should allow source-specific identification.

Consider a composite uniqueness constraint:

```text
(source_id, external_id)
```

if appropriate.

---

# 15. User Discovery State

Do NOT put user-specific state directly inside `discoveries`.

A discovery is global.

The fact that I personally saved or declined it belongs to the relationship between the user and discovery.

Therefore use something like:

```text
user_discoveries

id
user_id
discovery_id
status
created_at
updated_at
archived_at
```

Status:

```text
PENDING
SAVED
ARCHIVED
DECLINED
```

Think carefully about whether `PENDING` should actually be persisted or inferred.

Discuss this before implementing.

---

# 16. Tags

Use normalized many-to-many relationships.

```text
tags

id
name
```

```text
discovery_tags

discovery_id
tag_id
```

Potential tags:

```text
agents
llm
mcp
coding-agents
open-source
inference
rag
vector-db
research
developer-tools
```

---

# 17. Digests

A digest represents one generated email.

```text
digests

id
user_id
generated_at
sent_at
status
```

Possible status:

```text
GENERATED
SENT
FAILED
```

Then:

```text
digest_items

id
digest_id
discovery_id
position
```

This allows us to know exactly what was sent to the user.

This is important for auditability and debugging.

---

# 18. Database Principles

Use:

* foreign keys
* unique constraints
* check constraints where useful
* indexes
* timestamps
* transactions
* appropriate nullable/non-nullable fields

Do not create indexes everywhere.

For every important index, understand:

* which query uses it
* why it helps
* what write cost it introduces

Use `EXPLAIN` when useful.

---

# 19. API Design

Use REST.

Example:

```text
GET    /api/v1/discoveries
GET    /api/v1/discoveries/{id}

POST   /api/v1/discoveries/{id}/save
POST   /api/v1/discoveries/{id}/decline
POST   /api/v1/discoveries/{id}/archive

GET    /api/v1/library
GET    /api/v1/library/saved
GET    /api/v1/library/archived

GET    /api/v1/tags
GET    /api/v1/sources

GET    /api/v1/digests
GET    /api/v1/digests/{id}
```

Use proper HTTP semantics.

Do not create endpoints such as:

```text
POST /doEverything
```

---

# 20. API Versioning

Start with:

```text
/api/v1/
```

Even though this is a personal project.

I want to learn proper API organization.

---

# 21. Pagination

Collection endpoints must not return unlimited records.

Implement pagination.

Consider:

```text
limit
offset
```

initially.

Later consider cursor pagination if there is a real reason.

Explain the tradeoff.

---

# 22. Filtering

The discoveries endpoint should eventually support:

```text
status
source
tag
date
search
```

Example:

```text
GET /api/v1/discoveries?status=pending&tag=agents
```

Keep filtering logic maintainable.

---

# 23. Authentication

The application should support a real authenticated user.

Since this is initially a personal application, keep the authentication architecture simple.

Do not build enterprise authentication unnecessarily.

But still understand:

* password hashing
* sessions/JWT
* authentication
* authorization
* secure cookies
* CSRF considerations
* secrets

Choose an appropriate approach and explain it.

---

# 24. Ranking System

Do NOT use an LLM initially.

Build a deterministic scoring system.

Possible factors:

```text
recency
source_quality
technical_relevance
github_activity
novelty
category relevance
```

Example conceptual formula:

```text
score =
    0.25 * relevance
  + 0.20 * novelty
  + 0.20 * source_quality
  + 0.15 * recency
  + 0.20 * github_signal
```

Do NOT blindly use these weights.

The exact formula should be discussed and implemented in a configurable way.

The score should be explainable.

For example:

```json
{
  "total": 87,
  "relevance": 92,
  "novelty": 84,
  "source_quality": 90,
  "github_signal": 81
}
```

This makes debugging much easier.

---

# 25. Personalization

User feedback should eventually influence ranking.

If I repeatedly:

```text
SAVE → agents
SAVE → MCP
SAVE → coding agents

DECLINE → generic AI business news
DECLINE → generic AI image tools
```

the system should learn my preferences.

Do NOT start with machine learning.

Initially use simple statistics:

```text
tag save rate
tag decline rate
source save rate
category save rate
```

Then adjust ranking.

Later an ML model could be introduced.

---

# 26. Email Digest

The email should contain approximately 5 items.

Each item:

```text
TITLE

2 short lines explaining what happened.

Why it matters:
one concise sentence.

[OPEN]
[DECLINE]
```

The email should be visually clean.

Do not send long articles by email.

The purpose of the email is:

> **Give me enough information to decide whether I want to investigate.**

---

# 27. Email Actions

The buttons should eventually allow:

```text
Open
Save
Decline
```

Be careful with security.

Do not create unauthenticated destructive endpoints.

Use signed tokens or authenticated routes where appropriate.

Explain the security model.

---

# 28. Scheduling

The desired behavior is:

> Every 3 days generate a new AI Radar digest.

The deployment environment may not support an exact every-3-days scheduler directly.

Therefore investigate practical approaches.

Possibilities:

1. daily cron + database decides whether a digest is due
2. external scheduler
3. cron running daily with a `last_digest_at` check

For example:

```text
if now - last_digest_at >= 3 days:
    generate_digest()
```

This should be **idempotent**.

If the job executes twice, it must not send two identical emails.

---

# 29. Idempotency

This is an important backend-learning objective.

Every scheduled job should be safe to retry.

Example:

```text
Job starts
↓
Fetch data
↓
Insert new discoveries
↓
Check whether digest already exists for this period
↓
Generate digest
↓
Send email
↓
Record successful delivery
```

Think carefully about failure scenarios.

Example:

```text
Email sent successfully
↓
Database update fails
↓
Job retries
↓
Could send duplicate email
```

Design around this.

Explain possible solutions such as:

* idempotency keys
* delivery records
* unique constraints
* transactional outbox
* provider message IDs

Choose an appropriate level of complexity for this project.

---

# 30. Background Jobs

Do not run long ingestion work directly inside normal HTTP requests.

Separate:

```text
HTTP API
```

from:

```text
scheduled ingestion
digest generation
email sending
```

For V1, keep infrastructure simple.

A scheduled endpoint can trigger the work.

If a real queue is needed later, evaluate:

* Redis
* Celery
* Dramatiq
* RQ
* cloud queue

Do NOT add Redis/Celery simply because they are popular.

Add infrastructure only when the architecture benefits from it.

---

# 31. Error Handling

Implement consistent API errors.

Use appropriate HTTP status codes.

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
429 Too Many Requests
500 Internal Server Error
```

Do not expose internal stack traces to users.

Log detailed errors server-side.

---

# 32. Logging

Use structured logging where appropriate.

Logs should make it possible to understand:

```text
when a job started
what source failed
how many items were fetched
how many were new
how many were duplicates
how many were ranked
which digest was generated
whether email succeeded
```

Example:

```text
INFO ingestion_started source=github
INFO ingestion_completed source=github fetched=42 new=7 duplicates=35
INFO digest_generated digest_id=123 items=5
INFO email_sent digest_id=123
```

---

# 33. Testing

Testing is a major part of this project.

Use pytest.

At minimum:

## Unit tests

Test:

* URL normalization
* deduplication
* scoring
* ranking
* tag extraction
* state transitions

## API tests

Test:

* authentication
* CRUD
* save
* decline
* archive
* filtering
* pagination

## Database tests

Test:

* constraints
* relationships
* transactions

## Integration tests

Test:

```text
fetch → normalize → deduplicate → save
```

and eventually:

```text
ingest → rank → generate digest
```

Mock external APIs.

Do not depend on GitHub being available for every test.

---

# 34. External API Reliability

GitHub/RSS sources can fail.

Implement:

* timeouts
* retries
* exponential backoff where appropriate
* rate-limit handling
* logging
* graceful degradation

One broken source should not kill the entire ingestion pipeline.

Example:

```text
RSS 1 → success
RSS 2 → success
GitHub → rate limited
RSS 3 → success

Result:
process available data
log GitHub failure
continue
```

---

# 35. Configuration

Use environment variables.

Example:

```text
DATABASE_URL=
GITHUB_TOKEN=
RESEND_API_KEY=
APP_BASE_URL=
SECRET_KEY=
```

Never commit secrets.

Provide:

```text
.env.example
```

---

# 36. Docker

Use Docker for local development.

The backend should be reproducible.

Example:

```text
docker-compose.yml

services:
    api
    postgres
```

Do not containerize unnecessary things.

---

# 37. Migrations

Use Alembic.

Never manually modify the production database schema.

Workflow:

```text
modify SQLAlchemy model
        ↓
generate migration
        ↓
review migration
        ↓
run migration
```

I want to understand what Alembic actually does.

Do not hide migrations from me.

---

# 38. Repository Structure

Prefer a clean structure such as:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── workers/
│   └── utils/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── alembic/
├── alembic.ini
├── Dockerfile
├── pyproject.toml
└── README.md
```

Do not create unnecessary layers.

If a repository/service abstraction is introduced, explain why.

---

# 39. Architecture Principle

Avoid both extremes:

### Bad:

Everything inside routes.

```python
@router.get(...)
async def endpoint():
    # 300 lines
```

### Also bad:

50 abstraction layers for a small application.

I want:

> **Simple architecture with clear responsibilities.**

---

# 40. Security

At minimum consider:

* password hashing
* secure secrets
* authentication
* authorization
* SQL injection prevention
* XSS
* CSRF where applicable
* SSRF when fetching external URLs
* rate limiting
* input validation
* URL validation
* email token security

External URLs are particularly important.

Do not blindly fetch arbitrary user-provided URLs from the backend.

---

# 41. Observability

Eventually add:

* health endpoint
* readiness endpoint if appropriate
* structured logs
* error tracking
* basic metrics

Example:

```text
GET /health
```

should verify the application is alive.

A database readiness check can be separate.

---

# 42. Documentation

The README should explain:

* project purpose
* architecture
* setup
* environment variables
* database setup
* migrations
* running locally
* testing
* Docker
* deployment
* API documentation
* architecture decisions

Also create:

```text
docs/
    architecture.md
    database.md
    ingestion.md
    deployment.md
```

---

# 43. Architecture Decision Records

For important decisions create ADRs.

Example:

```text
docs/adr/

001-postgresql.md
002-sqlalchemy.md
003-authentication.md
004-scheduling.md
005-deduplication.md
```

Each ADR:

```text
Context
Decision
Alternatives
Consequences
```

This will help me learn system design.

---

# 44. Development Method

Do NOT build the entire project in one giant step.

Use milestones.

## Milestone 1

Project setup.

Deliver:

* FastAPI
* PostgreSQL
* Docker
* SQLAlchemy
* Alembic
* pytest
* Ruff
* basic CI

---

## Milestone 2

Database design.

Deliver:

* schema
* relationships
* constraints
* indexes
* migrations

Before implementation, explain the ER model.

---

## Milestone 3

Basic API.

Deliver:

* health
* users
* discoveries
* sources
* tags

---

## Milestone 4

Ingestion.

Deliver:

* RSS adapter
* GitHub adapter
* normalization
* deduplication

---

## Milestone 5

Ranking.

Deliver:

* deterministic scoring
* explainable score
* top 5 selection

---

## Milestone 6

User feedback.

Deliver:

* save
* decline
* archive
* notes
* library

---

## Milestone 7

Digest.

Deliver:

* digest generation
* email template
* delivery
* idempotency

---

## Milestone 8

Scheduling.

Deliver:

* scheduled ingestion
* scheduled digest
* safe retries

---

## Milestone 9

Frontend.

Claude can handle most of this.

Keep it simple.

---

## Milestone 10

Deployment.

Deploy:

```text
Frontend → Vercel
Backend → cloud platform
Database → managed PostgreSQL
Email → Resend
```

Then test the complete production flow.

---

# 45. Definition of Done

The project is complete when:

```text
Every ~3 days
      ↓
Sources are fetched
      ↓
New AI developments discovered
      ↓
Duplicates removed
      ↓
Items scored
      ↓
Top 5 selected
      ↓
Digest stored
      ↓
Email sent
      ↓
I receive email
      ↓
I click an item
      ↓
Web application opens
      ↓
I can save / decline / archive
      ↓
My feedback is stored
      ↓
Future ranking uses that feedback
```

And importantly:

```text
If something fails
      ↓
The system logs it
      ↓
Retries safely
      ↓
Doesn't duplicate data
      ↓
Doesn't send duplicate emails
```

---

# 46. Future AI Version

Only AFTER the non-AI version works.

Potential additions:

### LLM summarization

Generate:

```text
What happened?
Why does it matter?
Who should care?
```

### Semantic deduplication

Detect two articles about the same underlying event.

### Semantic ranking

Use embeddings to compare discoveries with my interests.

### Personal AI assistant

Ask:

> "Show me everything I saved about agent memory."

> "What did I save about MCP last month?"

> "Which AI projects have I wanted to try but never explored?"

But these are V2/V3.

Do not introduce them into V1.

---

# 47. Important Engineering Rule

When there is a choice between:

```text
quick implementation
```

and

```text
implementation that teaches an important backend concept
```

prefer the educationally valuable approach, as long as it is still reasonable for a production-style application.

However, do not introduce unnecessary complexity just to make the project look sophisticated.

---

# 48. How Claude Should Respond During Development

At the beginning of each milestone, tell me:

```text
What we are building
Why we need it
What I will learn
```

Before important implementation:

```text
Architecture decision
```

After implementation:

```text
What changed
Why it works
What I should inspect
How to test it
```

When I make a mistake:

Do not silently fix everything.

Explain the mistake and why it matters.

When there are multiple valid approaches:

Explain the tradeoffs.

---

# 49. Coding Style

Prefer:

* type hints
* async where appropriate
* small functions
* clear names
* explicit dependencies
* dependency injection where useful
* testable services
* Pydantic schemas
* SQLAlchemy 2.x style
* modern Python

Avoid:

* unnecessary magic
* global mutable state
* giant functions
* giant classes
* premature abstractions
* unnecessary design patterns
* copy-pasted code

---

# 50. Final Goal

This project should accomplish TWO things.

### Product goal

Create a personal AI Radar that keeps me informed about important new AI developments.

### Career goal

Make me substantially stronger at:

```text
Python
FastAPI
PostgreSQL
SQL
SQLAlchemy
Alembic
REST APIs
Backend architecture
Data modeling
External APIs
Background processing
Reliability
Testing
Security
Docker
Cloud deployment
System design
```

The second goal is at least as important as the first.

---

# 51. Start Here

Do NOT immediately generate the entire application.

First:

1. Analyze this specification.
2. Identify missing or contradictory requirements.
3. Propose the V1 architecture.
4. Propose the database ER model.
5. Explain the main tables and relationships.
6. Explain the backend request/data flow.
7. Explain the scheduled ingestion/digest flow.
8. Identify the main technical risks.
9. Propose the milestone plan.
10. Wait for my confirmation before starting implementation.

The first thing I want to deeply understand is:

> **How should the PostgreSQL database be designed for this application, and why?**

Start with the database architecture and teach me the reasoning behind it.
