from typing import List,Dict,Optional
from typing_extensions import Annotated
from pydantic import BaseModel 
from datetime import datetime   

class StoryJobsBase(BaseModel):
    theme:str

class StoryJobsResponse(BaseModel):
    job_id: str
    status:str
    created_at:datetime
    story_id:Optional[int]=None
    completed_at:Optional[datetime]=None
    error:Optional[str]=None    

    class config:
        from_attributes=True

class StoryJobCreate(StoryJobsBase):
    pass 