# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (FastAPI)
```bash
# Start backend development server
cd backend
uvicorn main:app --reload --port 8000

# Run backend tests
cd backend
python test_phase2.py

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Initialize database
cd backend
python init_db.py
```

### Frontend (React + Vite)
```bash
# Start frontend development server
cd frontend
npm run dev

# Build frontend for production
cd frontend
npm run build

# Run frontend linting
cd frontend
npm run lint

# Install frontend dependencies
cd frontend
npm install
```

### Docker Development
```bash
# Start all services with Docker Compose
docker-compose up --build

# Start specific service
docker-compose up backend
docker-compose up frontend
docker-compose up db
```

## Architecture Overview

This is a Reddit data collection and analysis application called "Jettit" (formerly RedditHarbor UI). It consists of:

### Backend (`/backend`)
- **FastAPI application** (`main.py`) - Main API server with CORS enabled
- **Database models** (`models.py`) - SQLAlchemy ORM models for Users, SearchJobs, Submissions, Comments
- **Database configuration** (`database.py`) - PostgreSQL connection via SQLAlchemy
- **Reddit collector service** (`services/reddit_collector.py`) - Integrates with RedditHarbor library for data collection
- **API routes** (`routes/`) - Organized endpoints for collection, data retrieval, and status

### Frontend (`/frontend`)
- **React application** built with Vite and TypeScript
- **Component structure**:
  - `pages/` - Main page components (Home, Results, Auth)
  - `components/` - Reusable UI components (DataSummary, ExportButtons, ResultsTable, etc.)
  - `services/api.ts` - API client for backend communication
- **Styling** - Individual CSS files per component
- **Routing** - React Router for navigation

### Database Schema
- **Users** - User account management
- **SearchJobs** - Collection job tracking with status, progress, and metadata
- **Submissions** - Reddit posts with metadata (score, comments, etc.)
- **Comments** - Reddit comments linked to submissions
- Database indexes on frequently queried fields (status, dates, scores)

## Key Integration Points

### RedditHarbor Integration
The backend integrates with the `redditharbor` Python library for Reddit data collection. The `RedditCollectorService` class handles:
- Job management and status tracking
- Asynchronous data collection
- Database storage of collected data
- Export functionality

### Environment Variables
Required environment variables (typically in `.env` file):
- `DATABASE_URL` - PostgreSQL connection string
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API client secret
- `REDDIT_USER_AGENT` - Reddit API user agent

### API Endpoints
- `POST /collect` - Start data collection job
- `GET /status/{job_id}` - Get job status and progress
- `GET /data` - Retrieve collected data with filtering
- `GET /export/{job_id}` - Export data in CSV/JSON/JSONL formats
- `GET /jobs` - List collection jobs
- `GET /stats` - Get collection statistics
- Authentication endpoints for user management

## Development Workflow

1. **Database Setup**: Ensure PostgreSQL is running (via Docker or local installation)
2. **Backend First**: Start the FastAPI server on port 8000
3. **Frontend Development**: Start Vite dev server on port 3000 with API proxy
4. **Testing**: Use `test_phase2.py` to test Reddit integration and data flow

## Important Notes

- The application requires Reddit API credentials for data collection
- Database migrations are handled through SQLAlchemy and Alembic
- Frontend uses Vite's proxy to route `/api` requests to the backend
- All user data can be anonymized during collection
- Export formats support streaming responses for large datasets
- Job status tracking allows for long-running collection processes