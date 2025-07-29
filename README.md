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