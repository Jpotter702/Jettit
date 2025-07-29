"""
Reddit data collection service.
This module integrates with RedditHarbor for data collection and stores results in PostgreSQL.
"""

import uuid
import time
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from database import get_db
from models import SearchJob, Submission, Comment

class RedditCollectorService:
    """
    Service for collecting Reddit data using RedditHarbor.
    Integrates with RedditHarbor library and stores results in PostgreSQL database.
    """
    
    def __init__(self):
        self.active_jobs: Dict[str, Dict[str, Any]] = {}
        # Initialize RedditHarbor credentials
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "RedditHarborUI/1.0")
    
    async def start_collection_job(
        self,
        subreddit: str,
        sort_type: str = "hot",
        post_limit: int = 100,
        include_comments: bool = True,
        anonymize_users: bool = True
    ) -> Dict[str, Any]:
        """
        Start a new Reddit data collection job.
        
        Args:
            subreddit: Name of the subreddit to collect data from
            sort_type: Sort type ('hot', 'new', 'top')
            post_limit: Maximum number of posts to collect
            include_comments: Whether to include comments
            anonymize_users: Whether to anonymize user data
            
        Returns:
            Dictionary containing job information
        """
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Create job record
        job_info = {
            "job_id": job_id,
            "subreddit": subreddit,
            "sort_type": sort_type,
            "post_limit": post_limit,
            "include_comments": include_comments,
            "anonymize_users": anonymize_users,
            "status": "queued",
            "progress": 0,
            "total_posts": 0,
            "collected_posts": 0,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "error_message": None
        }
        
        # Store job in database
        await self._store_job_in_db(job_info)
        
        # Start RedditHarbor collection in background
        try:
            await self._start_reddit_collection(job_id, job_info)
        except Exception as e:
            # Update job status to failed
            await self._update_job_status(job_id, "failed", error_message=str(e))
            return {
                "job_id": job_id,
                "status": "failed",
                "message": f"Collection failed: {str(e)}"
            }
        
        return {
            "job_id": job_id,
            "status": "queued",
            "message": f"Collection job created for r/{subreddit}"
        }
    
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a collection job from the database.
        
        Args:
            job_id: The job ID to check
            
        Returns:
            Job status information or None if job not found
        """
        db = next(get_db())
        try:
            search_job = db.query(SearchJob).filter(SearchJob.job_id == job_id).first()
            if not search_job:
                return None
            
            return {
                "job_id": search_job.job_id,
                "subreddit": search_job.subreddit,
                "sort_type": search_job.sort_type,
                "post_limit": search_job.post_limit,
                "include_comments": search_job.include_comments,
                "anonymize_users": search_job.anonymize_users,
                "status": search_job.status,
                "progress": search_job.progress,
                "total_posts": search_job.total_posts,
                "collected_posts": search_job.collected_posts,
                "created_at": search_job.created_at,
                "updated_at": search_job.updated_at,
                "error_message": search_job.error_message
            }
        finally:
            db.close()
    
    async def _store_job_in_db(self, job_info: Dict[str, Any]) -> None:
        """
        Store job information in the database.
        """
        db = next(get_db())
        try:
            search_job = SearchJob(
                job_id=job_info["job_id"],
                subreddit=job_info["subreddit"],
                sort_type=job_info["sort_type"],
                post_limit=job_info["post_limit"],
                include_comments=job_info["include_comments"],
                anonymize_users=job_info["anonymize_users"],
                status=job_info["status"],
                progress=job_info["progress"],
                total_posts=job_info["total_posts"],
                collected_posts=job_info["collected_posts"],
                error_message=job_info["error_message"]
            )
            db.add(search_job)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    async def _update_job_status(self, job_id: str, status: str, progress: int = None, 
                                total_posts: int = None, collected_posts: int = None, 
                                error_message: str = None) -> None:
        """
        Update job status in the database.
        """
        db = next(get_db())
        try:
            search_job = db.query(SearchJob).filter(SearchJob.job_id == job_id).first()
            if search_job:
                search_job.status = status
                if progress is not None:
                    search_job.progress = progress
                if total_posts is not None:
                    search_job.total_posts = total_posts
                if collected_posts is not None:
                    search_job.collected_posts = collected_posts
                if error_message is not None:
                    search_job.error_message = error_message
                search_job.updated_at = datetime.now()
                db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    async def _start_reddit_collection(self, job_id: str, job_info: Dict[str, Any]) -> None:
        """
        Start Reddit data collection using RedditHarbor.
        """
        try:
            # Import RedditHarbor
            from redditharbor import collect
            
            # Update job status to running
            await self._update_job_status(job_id, "running", progress=0)
            
            # Initialize RedditHarbor collector
            collector = collect.RedditCollector(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent=self.reddit_user_agent
            )
            
            # Start collection
            results = await collector.collect_subreddit_submissions(
                subreddit=job_info["subreddit"],
                sort=job_info["sort_type"],
                limit=job_info["post_limit"],
                include_comments=job_info["include_comments"],
                anonymize_users=job_info["anonymize_users"]
            )
            
            # Store results in database
            await self._store_results(job_id, results)
            
            # Update job status to completed
            await self._update_job_status(
                job_id, 
                "completed", 
                progress=100,
                total_posts=len(results.get("submissions", [])),
                collected_posts=len(results.get("submissions", []))
            )
            
        except Exception as e:
            # Update job status to failed
            await self._update_job_status(job_id, "failed", error_message=str(e))
            raise e
    
    async def _store_results(self, job_id: str, results: Dict[str, Any]) -> None:
        """
        Store RedditHarbor results in the database.
        """
        db = next(get_db())
        try:
            # Get the search job
            search_job = db.query(SearchJob).filter(SearchJob.job_id == job_id).first()
            if not search_job:
                raise ValueError(f"Search job {job_id} not found")
            
            submissions = results.get("submissions", [])
            for submission_data in submissions:
                # Create submission record
                submission = Submission(
                    search_job_id=search_job.id,
                    reddit_id=submission_data.get("id"),
                    title=submission_data.get("title"),
                    selftext=submission_data.get("selftext"),
                    url=submission_data.get("url"),
                    score=submission_data.get("score", 0),
                    upvote_ratio=submission_data.get("upvote_ratio", 0.0),
                    num_comments=submission_data.get("num_comments", 0),
                    author=submission_data.get("author") if not submission_data.get("anonymized") else None,
                    subreddit=submission_data.get("subreddit"),
                    created_utc=datetime.fromtimestamp(submission_data.get("created_utc", 0))
                )
                db.add(submission)
                db.flush()  # Get the submission ID
                
                # Store comments if included
                if submission_data.get("comments"):
                    for comment_data in submission_data["comments"]:
                        comment = Comment(
                            submission_id=submission.id,
                            reddit_id=comment_data.get("id"),
                            body=comment_data.get("body"),
                            score=comment_data.get("score", 0),
                            author=comment_data.get("author") if not comment_data.get("anonymized") else None,
                            created_utc=datetime.fromtimestamp(comment_data.get("created_utc", 0))
                        )
                        db.add(comment)
            
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    async def get_collected_data(
        self,
        job_id: Optional[str] = None,
        subreddit: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Retrieve collected Reddit data from the database.
        
        Args:
            job_id: Specific job ID to get data for
            subreddit: Filter by subreddit
            limit: Number of records to return
            offset: Number of records to skip
            
        Returns:
            Dictionary containing data and metadata
        """
        db = next(get_db())
        try:
            query = db.query(Submission)
            
            if job_id:
                # Get submissions for specific job
                search_job = db.query(SearchJob).filter(SearchJob.job_id == job_id).first()
                if search_job:
                    query = query.filter(Submission.search_job_id == search_job.id)
                else:
                    return {
                        "data": [],
                        "total": 0,
                        "limit": limit,
                        "offset": offset,
                        "job_id": job_id,
                        "subreddit": subreddit
                    }
            
            if subreddit:
                query = query.filter(Submission.subreddit == subreddit)
            
            total = query.count()
            submissions = query.offset(offset).limit(limit).all()
            
            # Convert to dictionary format
            data = []
            for submission in submissions:
                submission_dict = {
                    "id": submission.reddit_id,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "url": submission.url,
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "author": submission.author,
                    "subreddit": submission.subreddit,
                    "created_utc": submission.created_utc.isoformat() if submission.created_utc else None,
                    "collected_at": submission.collected_at.isoformat() if submission.collected_at else None
                }
                data.append(submission_dict)
            
            return {
                "data": data,
                "total": total,
                "limit": limit,
                "offset": offset,
                "job_id": job_id,
                "subreddit": subreddit
            }
        finally:
            db.close()
    
    async def list_jobs(
        self,
        status: Optional[str] = None,
        subreddit: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List all collection jobs with optional filtering.
        
        Args:
            status: Filter by job status
            subreddit: Filter by subreddit
            limit: Number of jobs to return
            offset: Number of jobs to skip
            
        Returns:
            Dictionary containing jobs and metadata
        """
        db = next(get_db())
        try:
            query = db.query(SearchJob)
            
            if status:
                query = query.filter(SearchJob.status == status)
            if subreddit:
                query = query.filter(SearchJob.subreddit == subreddit)
            
            total = query.count()
            jobs = query.order_by(SearchJob.created_at.desc()).offset(offset).limit(limit).all()
            
            # Convert to dictionary format
            data = []
            for job in jobs:
                job_dict = {
                    "job_id": job.job_id,
                    "subreddit": job.subreddit,
                    "sort_type": job.sort_type,
                    "post_limit": job.post_limit,
                    "include_comments": job.include_comments,
                    "anonymize_users": job.anonymize_users,
                    "status": job.status,
                    "progress": job.progress,
                    "total_posts": job.total_posts,
                    "collected_posts": job.collected_posts,
                    "created_at": job.created_at.isoformat() if job.created_at else None,
                    "updated_at": job.updated_at.isoformat() if job.updated_at else None,
                    "error_message": job.error_message
                }
                data.append(job_dict)
            
            return {
                "jobs": data,
                "total": total,
                "limit": limit,
                "offset": offset,
                "status": status,
                "subreddit": subreddit
            }
        finally:
            db.close()
    
    async def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """
        Cancel a running collection job.
        
        Args:
            job_id: The job ID to cancel
            
        Returns:
            Dictionary containing cancellation result
        """
        db = next(get_db())
        try:
            search_job = db.query(SearchJob).filter(SearchJob.job_id == job_id).first()
            if not search_job:
                raise ValueError(f"Job {job_id} not found")
            
            if search_job.status not in ["queued", "running"]:
                raise ValueError(f"Cannot cancel job with status: {search_job.status}")
            
            # Update job status to cancelled
            search_job.status = "cancelled"
            search_job.updated_at = datetime.now()
            db.commit()
            
            return {
                "job_id": job_id,
                "status": "cancelled",
                "message": f"Job {job_id} has been cancelled"
            }
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    async def get_job_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about collection jobs.
        
        Returns:
            Dictionary containing job statistics
        """
        db = next(get_db())
        try:
            # Count jobs by status
            total_jobs = db.query(SearchJob).count()
            queued_jobs = db.query(SearchJob).filter(SearchJob.status == "queued").count()
            running_jobs = db.query(SearchJob).filter(SearchJob.status == "running").count()
            completed_jobs = db.query(SearchJob).filter(SearchJob.status == "completed").count()
            failed_jobs = db.query(SearchJob).filter(SearchJob.status == "failed").count()
            cancelled_jobs = db.query(SearchJob).filter(SearchJob.status == "cancelled").count()
            
            # Count total submissions and comments
            total_submissions = db.query(Submission).count()
            total_comments = db.query(Comment).count()
            
            # Get top subreddits
            from sqlalchemy import func
            top_subreddits = db.query(
                SearchJob.subreddit,
                func.count(SearchJob.id).label('job_count')
            ).group_by(SearchJob.subreddit).order_by(func.count(SearchJob.id).desc()).limit(10).all()
            
            return {
                "jobs": {
                    "total": total_jobs,
                    "queued": queued_jobs,
                    "running": running_jobs,
                    "completed": completed_jobs,
                    "failed": failed_jobs,
                    "cancelled": cancelled_jobs
                },
                "data": {
                    "total_submissions": total_submissions,
                    "total_comments": total_comments
                },
                "top_subreddits": [
                    {"subreddit": subreddit, "job_count": count}
                    for subreddit, count in top_subreddits
                ]
            }
        finally:
            db.close()
    
    async def export_data(
        self,
        job_id: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Export collected data in specified format.
        
        Args:
            job_id: The job ID to export data for
            format: Export format ('json', 'csv', 'jsonl')
            
        Returns:
            Dictionary containing export information
        """
        # TODO: Replace with actual export logic
        # Example of what this will look like:
        # data = await self.get_collected_data(job_id=job_id)
        # 
        # if format == "csv":
        #     return self._export_to_csv(data["data"])
        # elif format == "json":
        #     return self._export_to_json(data["data"])
        # elif format == "jsonl":
        #     return self._export_to_jsonl(data["data"])
        # else:
        #     raise ValueError(f"Unsupported format: {format}")
        
        # For now, return placeholder
        return {
            "message": f"Export for job {job_id} in {format} format",
            "format": format,
            "job_id": job_id,
            "data": []  # This would contain the actual exported data
        }

# Global instance
reddit_collector = RedditCollectorService() 