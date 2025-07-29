---
title: Scaffold Rule
tags: [reddit, github, scaffold, projects]

---

Great choice. Below is a suggested **`.cursor/rules.json`** file tailored to your RedditHarbor UI project, guiding Cursor to structure the codebase with best practices for **FastAPI + React**, and aligning with your development plan:

```json
{
  "$schema": "https://raw.githubusercontent.com/getcursor/cursor-rules/main/schema.json",
  "rules": [
    {
      "pattern": "backend/main.py",
      "description": "Defines the FastAPI app, routes, and includes the RedditHarbor integration points.",
      "tags": ["backend", "fastapi", "api"]
    },
    {
      "pattern": "backend/routes/collect.py",
      "description": "Handles subreddit collection requests using RedditHarbor. Accepts subreddit, sort, limit.",
      "tags": ["api", "reddit", "harbor"]
    },
    {
      "pattern": "backend/models.py",
      "description": "Contains SQLAlchemy or Supabase ORM models for Submissions, Comments, Users.",
      "tags": ["db", "models"]
    },
    {
      "pattern": "backend/database.py",
      "description": "Initializes database connection and session management.",
      "tags": ["db", "init"]
    },
    {
      "pattern": "frontend/src/pages/Home.tsx",
      "description": "Home page for input form (subreddit, sort, limit) and triggers collection.",
      "tags": ["frontend", "form", "collection"]
    },
    {
      "pattern": "frontend/src/components/ResultsTable.tsx",
      "description": "Displays collected Reddit data with filters and pagination.",
      "tags": ["ui", "results", "table"]
    },
    {
      "pattern": "frontend/src/components/ExportButtons.tsx",
      "description": "Download data as CSV or JSON from backend export route.",
      "tags": ["export", "frontend", "ui"]
    },
    {
      "pattern": "frontend/src/services/api.ts",
      "description": "API utility to communicate with backend routes using Axios.",
      "tags": ["api", "axios"]
    },
    {
      "pattern": "docker-compose.yml",
      "description": "Sets up local development stack for backend, frontend, and database.",
      "tags": ["docker", "devops"]
    },
    {
      "pattern": "README.md",
      "description": "Explains how to install, run, and contribute to the RedditHarbor UI project.",
      "tags": ["docs", "usage", "project"]
    }
  ]
}
```

You can drop this file into a `.cursor` directory at the root of your repo. It will help structure your workspace and guide Cursor's suggestions intelligently.

Would you like a sample `docker-compose.yml` to match this structure as well?
