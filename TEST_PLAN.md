# Jettit - Comprehensive Test Plan

## Overview
This test plan validates the complete Jettit application functionality across all phases, with focus on Phase 5 deployment and integration testing.

## Test Environment Setup

### Prerequisites
- Docker and Docker Compose installed
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 15+

### Environment Variables Required
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/redditharbor
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=RedditHarborUI/1.0
VITE_API_URL=http://localhost:8000
```

## Test Phases

### Phase 1: Unit Tests

#### Backend API Tests (`backend/`)
- [ ] **Database Connection**: Test PostgreSQL connection and models
- [ ] **API Endpoints**: Test all FastAPI routes
- [ ] **Reddit Integration**: Test RedditHarbor service integration
- [ ] **Data Models**: Validate SQLAlchemy models and relationships
- [ ] **Authentication**: Test user registration and login endpoints

#### Frontend Component Tests (`frontend/`)
- [ ] **Component Rendering**: Test all React components
- [ ] **Form Validation**: Test input validation and error handling
- [ ] **API Integration**: Test service layer and API calls
- [ ] **State Management**: Test component state and props
- [ ] **Routing**: Test React Router navigation

### Phase 2: Integration Tests

#### API Integration
- [ ] **Collection Workflow**: Test complete data collection flow
- [ ] **Job Status Tracking**: Test job creation, status updates, and completion
- [ ] **Data Export**: Test CSV, JSON, and JSONL export functionality
- [ ] **Error Handling**: Test error scenarios and edge cases
- [ ] **Performance**: Test with large datasets and concurrent requests

#### Database Integration
- [ ] **CRUD Operations**: Test all database operations
- [ ] **Data Integrity**: Test constraints and relationships
- [ ] **Migrations**: Test database schema changes
- [ ] **Indexing**: Verify performance indexes work correctly

### Phase 3: End-to-End Tests

#### User Workflows
- [ ] **User Registration**: Complete user signup flow
- [ ] **Data Collection**: Submit collection job and track progress
- [ ] **Results Viewing**: View and filter collected data
- [ ] **Data Export**: Download data in different formats
- [ ] **Job Management**: List, view, and cancel jobs

#### Cross-Browser Testing
- [ ] **Chrome**: Test primary functionality
- [ ] **Firefox**: Test compatibility
- [ ] **Safari**: Test WebKit compatibility
- [ ] **Mobile**: Test responsive design

### Phase 4: Deployment Tests

#### Docker Testing
- [ ] **Backend Container**: Test backend Docker image
- [ ] **Frontend Container**: Test frontend Docker image
- [ ] **Docker Compose**: Test full stack deployment
- [ ] **Health Checks**: Verify container health endpoints
- [ ] **Environment Variables**: Test configuration injection

#### Production Deployment
- [ ] **Build Process**: Test production builds
- [ ] **Static Assets**: Test asset serving and caching
- [ ] **API Proxy**: Test frontend-to-backend routing
- [ ] **Security Headers**: Verify security configurations
- [ ] **SSL/TLS**: Test HTTPS functionality

### Phase 5: Performance & Security Tests

#### Performance Testing
- [ ] **Load Testing**: Test with multiple concurrent users
- [ ] **Database Performance**: Test query performance with large datasets
- [ ] **Memory Usage**: Monitor memory consumption
- [ ] **Response Times**: Measure API response times
- [ ] **Frontend Performance**: Test bundle size and load times

#### Security Testing
- [ ] **Input Validation**: Test XSS and injection protection
- [ ] **Authentication**: Test session management
- [ ] **CORS Configuration**: Verify cross-origin policies
- [ ] **Environment Variables**: Test secret handling
- [ ] **Security Headers**: Verify HTTP security headers

## Test Execution Commands

### Backend Tests
```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov flake8 httpx

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Run unit tests with coverage
pytest test_phase2.py -v --cov=. --cov-report=html

# Run integration tests
python test_phase2.py
```

### Frontend Tests
```bash
cd frontend

# Install dependencies
npm install

# Run linting
npm run lint

# Build for production
npm run build

# Start development server
npm run dev
```

### Docker Tests
```bash
# Build and start all services
docker-compose up --build

# Test individual services
docker-compose up backend
docker-compose up frontend
docker-compose up db

# Check container health
docker ps
docker-compose logs backend
docker-compose logs frontend
```

### End-to-End Tests
```bash
# Start full application
docker-compose up -d

# Run manual testing scenarios
# 1. Visit http://localhost:3000
# 2. Submit a data collection job
# 3. Monitor job progress
# 4. View and export results
# 5. Test user registration/login
```

## Test Data

### Sample Test Cases
1. **Small Subreddit**: r/test (limited posts)
2. **Medium Subreddit**: r/programming (moderate activity)
3. **Large Subreddit**: r/AskReddit (high volume - use small limits)

### Test Scenarios
- **Valid Inputs**: Standard subreddit names, reasonable limits
- **Edge Cases**: Empty subreddits, very large limits, special characters
- **Error Cases**: Invalid subreddits, API failures, database errors

## Success Criteria

### Functional Requirements
- [ ] All API endpoints respond correctly
- [ ] Data collection completes successfully
- [ ] Export functionality works for all formats
- [ ] User interface is responsive and functional
- [ ] Error handling provides meaningful feedback

### Non-Functional Requirements
- [ ] Application starts within 30 seconds
- [ ] API responses under 2 seconds for normal operations
- [ ] Frontend loads within 3 seconds
- [ ] Handles 10 concurrent collection jobs
- [ ] Database supports 1000+ submissions per job

### Deployment Requirements
- [ ] Docker containers build successfully
- [ ] Application runs in production environment
- [ ] Environment variables configure correctly
- [ ] Health checks pass consistently
- [ ] Logs provide adequate debugging information

## Test Results Documentation

Create test result files:
- `test-results-backend.md`
- `test-results-frontend.md`
- `test-results-integration.md`
- `test-results-deployment.md`

Each should include:
- Test execution date/time
- Environment details
- Pass/fail status for each test
- Performance metrics
- Issues found and resolution status
- Screenshots for UI tests

## Maintenance

### Regular Testing Schedule
- **Daily**: Unit tests in CI/CD pipeline
- **Weekly**: Integration tests and performance checks
- **Monthly**: Full end-to-end testing and security review
- **Release**: Complete test suite execution

### Test Data Cleanup
- Remove test database records after each test run
- Clean up exported files from test runs
- Reset test user accounts periodically