from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import os
import csv
import json
import io
from datetime import datetime
from dotenv import load_dotenv
from services.reddit_collector import reddit_collector

# Load environment variables
load_dotenv()

app = FastAPI(
    title="RedditHarbor UI API",
    description="Backend API for RedditHarbor data collection interface",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class CollectionRequest(BaseModel):
    subreddit: str
    sort_type: str = "hot"  # hot, new, top
    post_limit: int = 100
    include_comments: bool = True
    anonymize_users: bool = True

class CollectionResponse(BaseModel):
    job_id: str
    status: str
    message: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: Optional[int] = None
    total_posts: Optional[int] = None
    collected_posts: Optional[int] = None
    error_message: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str

@app.get("/")
async def root():
    return {"message": "RedditHarbor UI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "redditharbor-ui-api"}

@app.post("/collect", response_model=CollectionResponse)
async def collect_subreddit_data(request: CollectionRequest):
    """
    Initiate Reddit data collection for a subreddit
    """
    try:
        # Call the placeholder service that will later wrap RedditHarbor logic
        result = await reddit_collector.start_collection_job(
            subreddit=request.subreddit,
            sort_type=request.sort_type,
            post_limit=request.post_limit,
            include_comments=request.include_comments,
            anonymize_users=request.anonymize_users
        )
        
        return CollectionResponse(
            job_id=result["job_id"],
            status=result["status"],
            message=result["message"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """
    Get the status of a collection job
    """
    try:
        # Call the placeholder service for job status
        job_info = await reddit_collector.get_job_status(job_id)
        
        if not job_info:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return JobStatus(
            job_id=job_info["job_id"],
            status=job_info["status"],
            progress=job_info.get("progress"),
            total_posts=job_info.get("total_posts"),
            collected_posts=job_info.get("collected_posts"),
            error_message=job_info.get("error_message")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data")
async def get_collected_data(
    job_id: Optional[str] = None,
    subreddit: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Retrieve collected Reddit data
    """
    try:
        # Call the placeholder service for data retrieval
        result = await reddit_collector.get_collected_data(
            job_id=job_id,
            subreddit=subreddit,
            limit=limit,
            offset=offset
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs")
async def list_jobs(
    status: Optional[str] = None,
    subreddit: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """
    List all collection jobs with optional filtering
    """
    try:
        result = await reddit_collector.list_jobs(
            status=status,
            subreddit=subreddit,
            limit=limit,
            offset=offset
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """
    Cancel a running collection job
    """
    try:
        result = await reddit_collector.cancel_job(job_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_statistics():
    """
    Get collection job statistics
    """
    try:
        result = await reddit_collector.get_job_statistics()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserRegister):
    """
    Register a new user
    """
    try:
        # TODO: Implement actual user registration with password hashing
        # For now, return a placeholder response
        return UserResponse(
            id=1,
            username=user_data.username,
            email=user_data.email,
            created_at=str(datetime.now())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/login")
async def login_user(user_data: UserLogin):
    """
    Login user and return session token
    """
    try:
        # TODO: Implement actual user authentication
        # For now, return a placeholder response
        return {
            "access_token": "placeholder_token",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "username": "user",
                "email": user_data.email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user():
    """
    Get current user information
    """
    try:
        # TODO: Implement actual user session validation
        # For now, return a placeholder response
        return UserResponse(
            id=1,
            username="user",
            email="user@example.com",
            created_at=str(datetime.now())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/{job_id}")
async def export_data(job_id: str, format: str = "json"):
    """
    Export collected data in specified format using StreamingResponse
    """
    try:
        # Get the data for export
        data_result = await reddit_collector.get_collected_data(job_id=job_id)
        data = data_result.get("data", [])
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found for export")
        
        if format.lower() == "csv":
            return await _export_csv(data, job_id)
        elif format.lower() == "json":
            return await _export_json(data, job_id)
        elif format.lower() == "jsonl":
            return await _export_jsonl(data, job_id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'csv', 'json', or 'jsonl'")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def _export_csv(data: list, job_id: str):
    """Export data as CSV using StreamingResponse"""
    
    def generate_csv():
        if not data:
            return
        
        # Create CSV writer
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        headers = ['id', 'title', 'score', 'upvote_ratio', 'num_comments', 'author', 'subreddit', 'created_utc', 'url']
        writer.writerow(headers)
        yield output.getvalue()
        output.seek(0)
        output.truncate()
        
        # Write data rows
        for item in data:
            row = [
                item.get('id', ''),
                item.get('title', ''),
                item.get('score', 0),
                f"{item.get('upvote_ratio', 0) * 100:.1f}%",
                item.get('num_comments', 0),
                item.get('author', 'Anonymous'),
                item.get('subreddit', ''),
                item.get('created_utc', ''),
                item.get('url', '')
            ]
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate()
    
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=reddit-data-{job_id}.csv"
        }
    )

async def _export_json(data: list, job_id: str):
    """Export data as JSON using StreamingResponse"""
    
    def generate_json():
        yield json.dumps({
            "job_id": job_id,
            "export_date": str(datetime.now()),
            "total_records": len(data),
            "data": data
        }, indent=2, default=str)
    
    return StreamingResponse(
        generate_json(),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=reddit-data-{job_id}.json"
        }
    )

async def _export_jsonl(data: list, job_id: str):
    """Export data as JSONL (JSON Lines) using StreamingResponse"""
    
    def generate_jsonl():
        for item in data:
            yield json.dumps(item, default=str) + "\n"
    
    return StreamingResponse(
        generate_jsonl(),
        media_type="application/jsonl",
        headers={
            "Content-Disposition": f"attachment; filename=reddit-data-{job_id}.jsonl"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 