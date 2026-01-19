# here all stroy endpoints that are in schemas story 
import uuid
from uuid import uuid4,UUID
from typing import Optional
from datetime import datetime
from fastapi import FastAPI 
from fastapi import HTTPException,APIRouter,Depends,Cookie,Response,BackgroundTasks
from sqlalchemy.orm import Session  

from DB.database import  get_db,SessionLocal
from models.story import StoryNode,Story
from models.job import StoryJob
from schemas.story import (CompleteStoryNodeResponse,CreateStoryRequst,CompleteStoryResponse) 
from schemas.job import StoryJobsResponse
from core.story_generetor import StoryGenerator

router=APIRouter(prefix="/stories",#like app=fastapi()
                    tags=["stories "])

def get_settion_id(session_id:Optional[str]=Cookie(None)):
    if not session_id:
        session_id=str(uuid.uuid4())    
    return session_id

#thsi is for a create the story

@router.post("/create",response_model=StoryJobsResponse)
def create_story(
        request:CreateStoryRequst,
        background_tasks:BackgroundTasks,
        response: Response ,
        session_id: str=Depends(get_settion_id),
        db:Session=Depends(get_db)):

    response.set_cookie(key="session_id",value=session_id,httponly=True) 
    
    job_id= str(uuid.uuid4())


    job= StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="panding"
    )
    
    db.add(job)
    db.commit()#orm objecj reletion mapping 

    #add background task
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        session_id=session_id,
        theme=request.theme
    )

    return job

def generate_story_task(job_id:str,theme:str,session_id:str):
    db=SessionLocal()

    try:
        job=db.query(StoryJob).filter(StoryJob.job_id==job_id).first()

        if not job:
            return

        try:
            job.status="processing"
            db.commit()

            story=StoryGenerator.generate_story(db,session_id,theme) #todo story generate 

            job.story_id=story.id
            job.status = "completed"
            job.completed_at=datetime.now()
            db.commit()

        except Exception as e :
            
            job.status = "faild"
            job.completed_at=datetime.now()
            job.error=str(e)
            db.commit()  
    finally:
        db.close()           


# this is for a get the story 

@router.get("/{story_id}/complete",response_model=CompleteStoryResponse)
def get_complte_story(story_id:int,db:Session=Depends(get_db)):
    story=db.query(Story).filter(Story.id==story_id).first()

    if not story:
        raise HTTPException (status_code=404,detail="story not found")
    complete_story=build_complete_story_tree(db,story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=str(story.id),
        title= story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )















































