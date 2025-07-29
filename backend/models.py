from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    search_jobs = relationship("SearchJob", back_populates="user")

class SearchJob(Base):
    __tablename__ = "search_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    subreddit = Column(String, index=True)
    sort_type = Column(String)  # hot, new, top
    post_limit = Column(Integer)
    include_comments = Column(Boolean, default=True)
    anonymize_users = Column(Boolean, default=True)
    status = Column(String)  # queued, running, completed, failed
    progress = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)
    collected_posts = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="search_jobs")
    submissions = relationship("Submission", back_populates="search_job")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    search_job_id = Column(Integer, ForeignKey("search_jobs.id"))
    reddit_id = Column(String, unique=True, index=True)
    title = Column(Text)
    selftext = Column(Text, nullable=True)
    url = Column(String, nullable=True)
    score = Column(Integer)
    upvote_ratio = Column(Float)
    num_comments = Column(Integer)
    author = Column(String, nullable=True)  # null if anonymized
    subreddit = Column(String)
    created_utc = Column(DateTime(timezone=True))
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    search_job = relationship("SearchJob", back_populates="submissions")
    comments = relationship("Comment", back_populates="submission")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    reddit_id = Column(String, unique=True, index=True)
    body = Column(Text)
    score = Column(Integer)
    author = Column(String, nullable=True)  # null if anonymized
    created_utc = Column(DateTime(timezone=True))
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    submission = relationship("Submission", back_populates="comments")

# Database indexes for better performance
Index('idx_search_jobs_status', SearchJob.status)
Index('idx_search_jobs_created_at', SearchJob.created_at)
Index('idx_submissions_score', Submission.score)
Index('idx_submissions_created_utc', Submission.created_utc)
Index('idx_comments_score', Comment.score) 