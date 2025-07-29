from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import SearchJob
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: Optional[int] = None
    total_posts: Optional[int] = None
    collected_posts: Optional[int] = None
    error_message: Optional[str] = None

@router.get("/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Get the status of a collection job
    """
    search_job = db.query(SearchJob).filter(SearchJob.job_id == job_id).first()
    
    if not search_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=search_job.job_id,
        status=search_job.status,
        progress=search_job.progress,
        total_posts=search_job.total_posts,
        collected_posts=search_job.collected_posts,
        error_message=search_job.error_message
    )
```

```python:backend/routes/data.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Submission, Comment
from typing import Optional

router = APIRouter()

@router.get("/")
async def get_collected_data(
    subreddit: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Retrieve collected Reddit data with pagination
    """
    # TODO: Implement actual data retrieval with filters
    return {
        "data": [],
        "total": 0,
        "limit": limit,
        "offset": offset,
        "subreddit": subreddit
    }
```

## Frontend Setup (React + TypeScript)

Now let's create the React frontend structure:

```json:frontend/package.json
{
  "name": "redditharbor-ui",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.48.2",
    "axios": "^1.6.2",
    "react-router-dom": "^6.20.1",
    "@types/node": "^20.10.4"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
```

```typescript:frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

```typescript:frontend/src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

```typescript:frontend/src/App.tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Results from './pages/Results'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>RedditHarbor UI</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results/:jobId" element={<Results />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
```

```typescript:frontend/src/pages/Home.tsx
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { collectSubredditData } from '../services/api'
import './Home.css'

interface CollectionForm {
  subreddit: string
  sortType: 'hot' | 'new' | 'top'
  postLimit: number
  includeComments: boolean
  anonymizeUsers: boolean
}

const Home: React.FC = () => {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<CollectionForm>({
    defaultValues: {
      subreddit: '',
      sortType: 'hot',
      postLimit: 100,
      includeComments: true,
      anonymizeUsers: true
    }
  })

  const onSubmit = async (data: CollectionForm) => {
    setIsLoading(true)
    setError(null)
    
    try {
      const response = await collectSubredditData({
        subreddit: data.subreddit,
        sort_type: data.sortType,
        post_limit: data.postLimit,
        include_comments: data.includeComments,
        anonymize_users: data.anonymizeUsers
      })
      
      // Navigate to results page
      navigate(`/results/${response.job_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="home">
      <div className="container">
        <h2>Collect Reddit Data</h2>
        <p>Enter a subreddit name to start collecting data</p>
        
        <form onSubmit={handleSubmit(onSubmit)} className="collection-form">
          <div className="form-group">
            <label htmlFor="subreddit">Subreddit Name</label>
            <input
              id="subreddit"
              type="text"
              placeholder="e.g., programming, askreddit"
              {...register('subreddit', { 
                required: 'Subreddit name is required',
                pattern: {
                  value: /^[a-zA-Z0-9_]+$/,
                  message: 'Invalid subreddit name format'
                }
              })}
            />
            {errors.subreddit && (
              <span className="error">{errors.subreddit.message}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="sortType">Sort Type</label>
            <select id="sortType" {...register('sortType')}>
              <option value="hot">Hot</option>
              <option value="new">New</option>
              <option value="top">Top</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="postLimit">Post Limit</label>
            <input
              id="postLimit"
              type="number"
              min="1"
              max="1000"
              {...register('postLimit', { 
                valueAsNumber: true,
                min: { value: 1, message: 'Minimum 1 post' },
                max: { value: 1000, message: 'Maximum 1000 posts' }
              })}
            />
            {errors.postLimit && (
              <span className="error">{errors.postLimit.message}</span>
            )}
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                {...register('includeComments')}
              />
              Include Comments
            </label>
          </div>

          <div className="form-group checkbox">
            <label>
              <input
                type="checkbox"
                {...register('anonymizeUsers')}
              />
              Anonymize Users
            </label>
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="submit-btn"
          >
            {isLoading ? 'Starting Collection...' : 'Start Collection'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}

export default Home
```

```typescript:frontend/src/pages/Results.tsx
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getJobStatus, getCollectedData } from '../services/api'
import ResultsTable from '../components/ResultsTable'
import ExportButtons from '../components/ExportButtons'
import './Results.css'

interface JobStatus {
  job_id: string
  status: string
  progress?: number
  total_posts?: number
  collected_posts?: number
  error_message?: string
}

const Results: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>()
  const [jobStatus, setJobStatus] = useState<JobStatus | null>(null)
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!jobId) return

    const fetchStatus = async () => {
      try {
        const status = await getJobStatus(jobId)
        setJobStatus(status)
        
        if (status.status === 'completed') {
          const resultData = await getCollectedData()
          setData(resultData.data || [])
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch status')
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
    
    // Poll for status updates if job is still running
    if (jobStatus?.status === 'running' || jobStatus?.status === 'queued') {
      const interval = setInterval(fetchStatus, 5000)
      return () => clearInterval(interval)
    }
  }, [jobId, jobStatus?.status])

  if (loading) {
    return (
      <div className="results">
        <div className="container">
          <div className="loading">Loading...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="results">
        <div className="container">
          <div className="error-message">{error}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="results">
      <div className="container">
        <h2>Collection Results</h2>
        
        {jobStatus && (
          <div className="job-status">
            <h3>Job Status: {jobStatus.status}</h3>
            {jobStatus.progress !== undefined && (
              <div className="progress">
                <div 
                  className="progress-bar" 
                  style={{ width: `${jobStatus.progress}%` }}
                ></div>
                <span>{jobStatus.progress}%</span>
              </div>
            )}
            {jobStatus.total_posts && (
              <p>Collected {jobStatus.collected_posts} of {jobStatus.total_posts} posts</p>
            )}
            {jobStatus.error_message && (
              <div className="error-message">{jobStatus.error_message}</div>
            )}
          </div>
        )}

        {jobStatus?.status === 'completed' && data.length > 0 && (
          <>
            <ExportButtons jobId={jobId!} />
            <ResultsTable data={data} />
          </>
        )}

        {jobStatus?.status === 'completed' && data.length === 0 && (
          <div className="no-data">
            <p>No data was collected for this job.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Results
```

```typescript:frontend/src/components/ResultsTable.tsx
import React, { useState } from 'react'
import './ResultsTable.css'

interface Submission {
  id: string
  title: string
  score: number
  upvote_ratio: number
  num_comments: number
  author?: string
  subreddit: string
  created_utc: string
  url?: string
}

interface ResultsTableProps {
  data: Submission[]
}

const ResultsTable: React.FC<ResultsTableProps> = ({ data }) => {
  const [sortBy, setSortBy] = useState<keyof Submission>('score')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [filterKeyword, setFilterKeyword] = useState('')
  const [minScore, setMinScore] = useState('')

  const handleSort = (column: keyof Submission) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(column)
      setSortOrder('desc')
    }
  }

  const filteredAndSortedData = data
    .filter(item => {
      const matchesKeyword = filterKeyword === '' || 
        item.title.toLowerCase().includes(filterKeyword.toLowerCase())
      const matchesScore = minScore === '' || item.score >= parseInt(minScore)
      return matchesKeyword && matchesScore
    })
    .sort((a, b) => {
      const aVal = a[sortBy]
      const bVal = b[sortBy]
      
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        return sortOrder === 'asc' 
          ? aVal.localeCompare(bVal)
          : bVal.localeCompare(aVal)
      }
      
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortOrder === 'asc' ? aVal - bVal : bVal - aVal
      }
      
      return 0
    })

  return (
    <div className="results-table">
      <div className="filters">
        <div className="filter-group">
          <label>Search:</label>
          <input
            type="text"
            placeholder="Filter by title..."
            value={filterKeyword}
            onChange={(e) => setFilterKeyword(e.target.value)}
          />
        </div>
        <div className="filter-group">
          <label>Min Score:</label>
          <input
            type="number"
            placeholder="0"
            value={minScore}
            onChange={(e) => setMinScore(e.target.value)}
          />
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th onClick={() => handleSort('title')}>
              Title {sortBy === 'title' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('score')}>
              Score {sortBy === 'score' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('upvote_ratio')}>
              Upvote Ratio {sortBy === 'upvote_ratio' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('num_comments')}>
              Comments {sortBy === 'num_comments' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('author')}>
              Author {sortBy === 'author' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('created_utc')}>
              Created {sortBy === 'created_utc' && (sortOrder === 'asc' ? '↑' : '↓')}
            </th>
          </tr>
        </thead>
        <tbody>
          {filteredAndSortedData.map((item) => (
            <tr key={item.id}>
              <td>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.title}
                </a>
              </td>
              <td>{item.score}</td>
              <td>{(item.upvote_ratio * 100).toFixed(1)}%</td>
              <td>{item.num_comments}</td>
              <td>{item.author || 'Anonymous'}</td>
              <td>{new Date(item.created_utc).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {filteredAndSortedData.length === 0 && (
        <div className="no-results">
          No results match your filters.
        </div>
      )}
    </div>
  )
}

export default ResultsTable
```

```typescript:frontend/src/components/ExportButtons.tsx
import React, { useState } from 'react'
import { exportData } from '../services/api'
import './ExportButtons.css'

interface ExportButtonsProps {
  jobId: string
}

const ExportButtons: React.FC<ExportButtonsProps> = ({ jobId }) => {
  const [exporting, setExporting] = useState<string | null>(null)

  const handleExport = async (format: 'csv' | 'json' | 'jsonl') => {
    setExporting(format)
    try {
      const response = await exportData(jobId, format)
      
      // Create download link
      const blob = new Blob([JSON.stringify(response)], {
        type: 'application/json'
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `reddit-data-${jobId}.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    } finally {
      setExporting(null)
    }
  }

  return (
    <div className="export-buttons">
      <h3>Export Data</h3>
      <div className="button-group">
        <button
          onClick={() => handleExport('csv')}
          disabled={exporting !== null}
          className="export-btn csv"
        >
          {exporting === 'csv' ? 'Exporting...' : 'Export as CSV'}
        </button>
        <button
          onClick={() => handleExport('json')}
          disabled={exporting !== null}
          className="export-btn json"
        >
          {exporting === 'json' ? 'Exporting...' : 'Export as JSON'}
        </button>
        <button
          onClick={() => handleExport('jsonl')}
          disabled={exporting !== null}
          className="export-btn jsonl"
        >
          {exporting === 'jsonl' ? 'Exporting...' : 'Export as JSONL'}
        </button>
      </div>
    </div>
  )
}

export default ExportButtons
```

```typescript:frontend/src/services/api.ts
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface CollectionRequest {
  subreddit: string
  sort_type: string
  post_limit: number
  include_comments: boolean
  anonymize_users: boolean
}

export interface CollectionResponse {
  job_id: string
  status: string
  message: string
}

export interface JobStatus {
  job_id: string
  status: string
  progress?: number
  total_posts?: number
  collected_posts?: number
  error_message?: string
}

export const collectSubredditData = async (request: CollectionRequest): Promise<CollectionResponse> => {
  const response = await api.post('/collect', request)
  return response.data
}

export const getJobStatus = async (jobId: string): Promise<JobStatus> => {
  const response = await api.get(`/status/${jobId}`)
  return response.data
}

export const getCollectedData = async (params?: {
  subreddit?: string
  limit?: number
  offset?: number
}): Promise<{ data: any[], total: number, limit: number, offset: number }> => {
  const response = await api.get('/data', { params })
  return response.data
}

export const exportData = async (jobId: string, format: string): Promise<any> => {
  const response = await api.get(`/export/${jobId}`, {
    params: { format },
    responseType: 'blob'
  })
  return response.data
}
```

## Configuration Files

```env:.env.example
# Backend Configuration
DATABASE_URL=postgresql://user:password@localhost/redditharbor
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=RedditHarborUI/1.0

# Supabase Configuration (if using Supabase)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

```dockerfile:Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile:Dockerfile.frontend
FROM node:18-alpine

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

```yaml:docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/redditharbor
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=redditharbor
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```markdown:README.md
# RedditHarbor UI

A user-friendly web interface for collecting and analyzing Reddit data using the RedditHarbor library.

## Features

- 🎯 **Easy Data Collection**: Simple form to collect Reddit data from any subreddit
- 📊 **Interactive Results**: View collected data with filtering and sorting
- 📁 **Multiple Export Formats**: Download data as CSV, JSON, or JSONL
- 🔒 **Privacy-Focused**: Optional user anonymization
- ⚡ **Real-time Status**: Track collection progress in real-time

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL (or use Docker)

### Development Setup

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd redditharbor-ui
   
   # Install backend dependencies
   cd backend
   pip install -r requirements.txt
   
   # Install frontend dependencies
   cd ../frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Reddit API credentials and database URL
   ```

3. **Start the development servers:**
   ```bash
   # Terminal 1: Start backend
   cd backend
   uvicorn main:app --reload --port 8000
   
   # Terminal 2: Start frontend
   cd frontend
   npm run dev
   ```

4. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Docker Setup

```bash
docker-compose up --build
```

## Usage

1. **Enter a subreddit name** in the form
2. **Configure collection settings** (sort type, post limit, etc.)
3. **Start collection** and monitor progress
4. **View results** with filtering and sorting options
5. **Export data** in your preferred format

## API Endpoints

- `POST /collect` - Start a new collection job
- `GET /status/{job_id}` - Get job status
- `GET /data` - Retrieve collected data
- `GET /export/{job_id}` - Export data

## Development

### Project Structure

```
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI app entry point
│   ├── models.py           # Database models
│   ├── database.py         # Database configuration
│   ├── routes/             # API routes
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── services/       # API services
│   │   └── App.tsx         # Main app component
│   └── package.json        # Node dependencies
└── docs/                   # Documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
```

## CSS Files for Styling

```css:frontend/src/App.css
.App {
  text-align: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}

.App-header h1 {
  margin: 0;
  font-size: 2rem;
}

main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
```

```css:frontend/src/index.css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
```

```css:frontend/src/pages/Home.css
.home {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.container {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.collection-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

.form-group.checkbox input {
  width: auto;
}

.error {
  color: #d32f2f;
  font-size: 14px;
}

.submit-btn {
  background-color: #1976d2;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #1565c0;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 12px;
  border-radius: 4px;
  margin-top: 20px;
}
```

```css:frontend/src/pages/Results.css
.results {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.container {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.job-status {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.progress {
  margin: 10px 0;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 20px;
  background-color: #4caf50;
  transition: width 0.3s ease;
}

.progress span {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #333;
  font-weight: 600;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
  padding: 12px;
  border-radius: 4px;
  margin: 20px 0;
}
```

```css:frontend/src/components/ResultsTable.css
.results-table {
  margin-top: 20px;
}

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: 600;
  font-size: 14px;
}

.filter-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

th {
  background-color: #f5f5f5;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
}

th:hover {
  background-color: #e0e0e0;
}

td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

td a {
  color: #1976d2;
  text-decoration: none;
}

td a:hover {
  text-decoration: underline;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}
```

```css:frontend/src/components/ExportButtons.css
.export-buttons {
  margin: 20px 0;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.export-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.export-btn.csv {
  background-color: #4caf50;
  color: white;
}

.export-btn.csv:hover:not(:disabled) {
  background-color: #45a049;
}

.export-btn.json {
  background-color: #2196f3;
  color: white;
}

.export-btn.json:hover:not(:disabled) {
  background- 