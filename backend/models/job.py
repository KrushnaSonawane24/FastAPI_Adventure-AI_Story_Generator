from sqlalchemy import Column, Integer, String,DateTime
#this use to map sql data to fastapi
from sqlalchemy.sql import func

from DB.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"
    
    id=Column(Integer,primary_key=True,index=True)
    job_id=Column(String,unique=True,index=True)
    session_id=Column(String,index=True)
    theme=Column(String)
    story_id=Column(Integer,nullable=True)
    status=Column(String,nullable=True)
    error=Column(String,nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    completed_at=Column(DateTime(timezone=True),nullable=True)





















































































