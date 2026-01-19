from uuid import uuid4
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException,Cookie
from sqlalchemy.orm import Session

from DB.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobsResponse

router = APIRouter(prefix="/jobs",tags=["jobs"])

@router.get(path="/{job_id}",response_model=StoryJobsResponse)
def get_job_status(job_id:str,db:Session=Depends(get_db)):
    job=db.query(StoryJob).filter(StoryJob.job_id==job_id).first()

    if not job:
        raise HTTPException(status_code=404,detail="job not found")
    return job