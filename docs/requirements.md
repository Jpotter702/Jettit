---
title: Requirements
tags: [requirements, github, reddit, projects]

---

Here is a structured list of requirements to build a user-friendly interface around RedditHarbor, assuming a **React + FastAPI** architecture:

---

## ✅ **Functional Requirements**

### 🧩 **Frontend (React)**

1. **Search UI**

   * Input for subreddit name(s)
   * Filters: date range, sorting type (hot, new, top), keyword match
   * Options to limit number of posts/comments

2. **Results Display**

   * Table or card view of collected submissions and comments
   * Filters for upvote ratio, score, keyword highlight
   * Pagination or infinite scroll

3. **Export Options**

   * Download data as CSV, JSON, or JSONL

4. **Status Feedback**

   * Loading indicators
   * Error messages
   * Success notifications

5. **User Account (optional)**

   * Basic login/session management
   * Preferences for saved searches or API credentials

---

### 🔧 **Backend (FastAPI)**

1. **RedditHarbor Integration**

   * Endpoints to trigger data collection (e.g., `POST /collect`)
   * Endpoints to fetch stored data (e.g., `GET /data`)
   * Endpoint to list and manage stored datasets

2. **Data Handling**

   * Store collected data in PostgreSQL or Supabase
   * Option to queue long-running collection jobs (via Celery or BackgroundTasks)

3. **Security**

   * Input validation
   * Rate-limiting on API calls
   * Credential storage (for Reddit and Supabase)

4. **Export Services**

   * Generate downloadable files on request

---

### 🗃️ **Database Requirements**

1. Tables for:

   * Submissions
   * Comments
   * Users
   * Search jobs (to track request metadata and progress)

---

## 🧪 **Non-Functional Requirements**

* **Responsive design** (desktop/tablet/mobile)
* **Scalability** for high volume subreddit queries
* **Deployability** via Docker or similar
* **Documentation** for end users and devs
* **Testing** (unit tests for API, e2e tests for frontend)

---

Let me know if you want this translated into a project scaffold, user stories, or GitHub issues.
