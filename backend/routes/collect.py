from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import SearchJob
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

router = APIRouter()

class CollectionRequest(BaseModel):
    subreddit: str
    sort_type: str = "hot"
    post_limit: int = 100
    include_comments: bool = True
    anonymize_users: bool = True

class CollectionResponse(BaseModel):
    job_id: str
    status: str
    message: str

@router.post("/", response_model=CollectionResponse)
async def create_collection_job(
    request: CollectionRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new Reddit data collection job
    """
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Create search job record
        search_job = SearchJob(
            job_id=job_id,
            subreddit=request.subreddit,
            sort_type=request.sort_type,
            post_limit=request.post_limit,
            include_comments=request.include_comments,
            anonymize_users=request.anonymize_users,
            status="queued"
        )
        
        db.add(search_job)
        db.commit()
        db.refresh(search_job)
        
        # TODO: Trigger background task for actual collection
        
        return CollectionResponse(
            job_id=job_id,
            status="queued",
            message=f"Collection job created for r/{request.subreddit}"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 