---
title: Cursor Rules
tags: [development, github, projects, reddit, api, ai]

---

Certainly! Here’s a refined set of **Cursor project rules**, crafted for the RedditHarbor UI project. It leverages **domain-specific knowledge** about RedditHarbor and ensures **consistent development protocols** across the full-stack codebase.

### ⚙️ Structure of `.cursor/rules/` Directory

* `.cursor/rules/architecture.mdc` — overarching architectural conventions
* `.cursor/rules/backend_fastapi.mdc` — backend-specific guidance
* `.cursor/rules/frontend_react.mdc` — frontend-specific React rules
* `.cursor/rules/dev_protocol.mdc` — team-wide processes and consistency guidelines

---

### 1. `architecture.mdc`

```md
---
description: Overall architecture & high-level domain knowledge of RedditHarbor
globs: []
---
# RedditHarbor UI Architecture Guidelines

- We use **FastAPI** as the backend to wrap core functionality from the **RedditHarbor** library, enabling data collection, anonymization, storage, and updates via REST endpoints.
- Frontend is built with **React / TypeScript**, interacting with FastAPI endpoints to initiate jobs and retrieve data.
- Data flows: **Frontend form ⟶ API call ⟶ RedditHarbor logic ⟶ DB storage (PostgreSQL or Supabase) ⟶ frontend data display/export**.
- Be mindful of **RedditHarbor’s privacy-first design**: allow toggling anonymization of user profiles.
- Design logical separation: API routes for `/collect`, `/status`, `/data`, `/export`, mapping to corresponding modules.

```

---

### 2. `backend_fastapi.mdc`

```md
---
description: FastAPI backend rules for RedditHarbor integration
globs: backend/**/*.py
---
# Backend (FastAPI + RedditHarbor) Guidelines

- Define modular routes in `backend/routes/`, e.g. `collect.py`, `status.py`, `export.py`.
- Use **dependency injection** for database sessions (e.g. via `Depends`).
- Interface with RedditHarbor library cleanly—wrap calls within service functions.
- Use **SQLAlchemy** or Supabase ORM for models: `Submission`, `Comment`, `User`, `SearchJob`.
- Each search job endpoint should return a job ID and status; progress is tracked in `SearchJob`.
- Use **async endpoints** where possible; long-running jobs should use FastAPI BackgroundTasks or Celery.
- For exports, use FastAPI’s `StreamingResponse` with proper MIME and file headers.
- Sanitize inputs: subreddit names, date ranges, limits.
- Respect Reddit API rate limits and error handling from RedditHarbor.
- Include unit-tests using `pytest` for core logic, model creation, error cases.

```

---

### 3. `frontend_react.mdc`

```md
---
description: React + TypeScript frontend conventions
globs: frontend/src/**/*.tsx
---
# Frontend (React + TS) Guidelines

- Use **functional components with hooks** exclusively. No class components.
- Organize code: Components in `src/components/`, pages in `src/pages/`, services in `src/services/`.
- Use **Axios** or `fetch` in `api.ts` to hit backend endpoints: `/collect`, `/status`, `/data`, `/export`.
- Naming conventions: kebab-case folders, PascalCase component names, camelCase props/state.
- Forms: use `react-hook-form` or Formik for collection input. Validate required fields.
- Provide loading state visuals for collecting jobs and data fetching.
- Results display using a table or card layout: include filters (keyword, score, upvote ratio).
- Support pagination or infinite scroll with virtualization if large datasets.
- Export buttons should trigger downloads via anchor blob or link.
- Keep styling modular (CSS Modules, Tailwind, or equivalent).

```

---

### 4. `dev_protocol.mdc`

```md
---
description: Long‑term development protocol, naming, branching, commit style
globs: []
---
# Development Protocol & Team Style Guide

## 🧑‍💻 Branching & Commits

- Use feature branches: `feature/<short-description>` or `bugfix/<...>`.
- Follow commit message style: `<type>: <short summary>`—types: `feat`, `fix`, `docs`, `refactor`, `test`.

## 🧪 Testing

- Aim for high coverage: at least 80% for backend and services.
- Include tests for edge cases: rate limits, empty subreddit, invalid input, anonymized data toggles.
- Run backend tests with `pytest`, frontend with `Jest` or React Testing Library.

## 📜 Code Reviews

- Pull requests should reference issue/ticket.
- Require at least one approving review.
- Check that rules are respected: modularity, naming, docstrings, test coverage.

## 📁 File & Folder Conventions

- Backend: `backend/`, with subfolders: `models`, `routes`, `services`, `database`, `tests`.
- Frontend: `frontend/src/`, with `pages`, `components`, `services`, `styles`, `tests`.
- Centralise configuration: environment variables in `.env`, secrets not committed.

## 🧠 Documentation & Inline Context

- Update `README.md` whenever new feature or API behavior changes.
- Add docstrings in Python functions to explain intent and domain-specific logic (e.g. anonymization).
- Provide sample config: `example.env`, example `.cursor/rules` for reference.

## 📆 Redundancy & Refactoring

- Schedule a codebase audit every 4 weeks to remove dead code, improve pattern consistency.
- Refactor service modules when expansion happens (e.g. keyword‑based collection, temporal metrics).

```

---

### ✅ Next Steps

* Drop these `.mdc` files into your repo under `.cursor/rules/`.
* Ensure Cursor is configured to auto-attach these rule files per pattern.
* Developers will now have domain-aware, consistent guidance during coding, inline edits, and chat interactions.

You can also **set up an MCP server** later tied to your project management tool (e.g., Jira or Notion) to pull in ticket context—Cursor rules will work hand-in-hand with that.([playbooks.com][1], [dev.to][2], [medium.com][3], [launchdarkly.com][4], [docs.cursor.com][5], [docs.cursor.com][6])

Let me know if you'd like example `.cursor/rules` or to connect a protocol to automate updates or issue generation!

[1]: https://playbooks.com/rules?utm_source=chatgpt.com "Cursor rules for AI that actually work - Playbooks"
[2]: https://dev.to/dpaluy/mastering-cursor-rules-a-developers-guide-to-smart-ai-integration-1k65?utm_source=chatgpt.com "Mastering Cursor Rules: A Developer's Guide to Smart AI Integration"
[3]: https://medium.com/%40grzywaczewski.jakub/cursor-ai-rules-d097c902253b?utm_source=chatgpt.com "(Cursor) AI rules! - by Jakub Grzywaczewski - Medium"
[4]: https://launchdarkly.com/docs/tutorials/cursor-tips-and-tricks?utm_source=chatgpt.com "4 hacks to turbocharge your Cursor productivity - LaunchDarkly"
[5]: https://docs.cursor.com/context/rules?utm_source=chatgpt.com "Rules - Cursor"
[6]: https://docs.cursor.com/guides/working-with-context?utm_source=chatgpt.com "Working with Context - Cursor Docs"
