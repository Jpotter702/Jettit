---
title: Prompts
tags: [requirements, prompts, github, reddit, projects]

---

Absolutely. Below is a breakdown of each task into **developer-friendly prompts**, compatible with **Cursor** and other code-aware tools (like GitHub Copilot, CodeWhisperer, or Cody). These prompts are designed to be pasted directly into your IDE to help implement the feature with AI support.

---

## 🧩 **Phase 1: Project Setup & Core Integration**

### 📦 Backend: FastAPI

```python
# Create a FastAPI app with a route `/collect` that accepts a subreddit name, sort type, and post limit as JSON.
# This route should call a placeholder function for now that will later wrap RedditHarbor logic.
```

```python
# Add CORS middleware to FastAPI to allow requests from localhost:3000 (React dev server).
```

### 🧪 Frontend: React

```tsx
// Create a React form with inputs for:
// - subreddit name (text)
// - sort type (select: hot, new, top)
// - post limit (number)
// - submit button to trigger collection
// Use React Hook Form for validation.
```

```tsx
// Use Axios or Fetch to POST the form data to `/collect` endpoint on the FastAPI backend.
// Show a loading indicator while the request is in progress.
```

---

## 🧩 **Phase 2: Data Collection & Storage**

### 🧠 Backend

```python
# Implement a function that calls RedditHarbor's collect.subreddit_submission with parameters from the `/collect` POST request.
# Store the results in PostgreSQL or Supabase.
```

```python
# Design SQLAlchemy models or Supabase schema for:
# - Submissions
# - Comments
# - Users (optional)
```

```python
# Add a `/status` endpoint to return the progress or completion of a collection job.
# Return JSON with a status field (e.g., "running", "completed", "error").
```

---

## 🧩 **Phase 3: Display & Search Results**

### 🎨 Frontend

```tsx
// Create a data display component that shows submissions in a table format:
// Columns: title, score, upvote ratio, subreddit, created_at.
// Add a loading spinner while fetching.
```

```tsx
// Add filters above the table:
// - search keyword
// - minimum score
// - sort by score or date
// Implement filtering client-side for now.
```

```tsx
// Add pagination or infinite scroll to the results table.
```

---

## 🧩 **Phase 4: Export & User Management**

### 🧠 Backend

```python
# Add a route `/export` that takes a dataset ID or parameters and returns a file in CSV or JSON format.
# Use StreamingResponse in FastAPI for efficient download.
```

### 🎨 Frontend

```tsx
// Add "Export as CSV/JSON" buttons to the results table.
// When clicked, call `/export` and trigger a file download.
```

```tsx
// Optional: Add login form using Supabase Auth or Auth0.
// After login, store user session and use it to filter saved searches.
```

---

## 🧩 **Phase 5: Finalization & Deployment**

### 🔧 DevOps

```dockerfile
# Write a Dockerfile for the FastAPI backend with environment variable support.
```

```json
// Create a Vercel/Fly.io configuration for deploying the React frontend.
// Make sure to route `/api/*` requests to the FastAPI backend.
```

```yaml
# Add GitHub Actions CI/CD pipeline:
# - Lint and test backend
# - Build frontend
# - Deploy to Fly.io or Vercel
```

---

Would you like these packaged into a `.cursor` workspace or as a project template folder?
