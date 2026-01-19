#add your post and update logic here pydantic model 

from typing import List,Optional,Dict
from typing_extensions import Annotated
from datetime import datetime
from pydantic import BaseModel,Field

class storyOptionSchema(BaseModel):
    text:Annotated[str,Field()]

    node_id:Optional[str]=None

class StoryNodeBase(BaseModel):
    content:str
    is_ending:bool=False
    is_winning_ending:bool=False

class CompleteStoryNodeResponse(StoryNodeBase):
    id : int
    options: List[storyOptionSchema]=[]

    class config:
        from_attributes=True

class StoryBase(BaseModel):
    title:str
    session_id: Optional[str]=None

    class config:
        from_attributes=True

class CreateStoryRequst(BaseModel):
    theme:str

class CompleteStoryResponse(StoryBase):
    id:str
    created_at:datetime
    root_node: CompleteStoryNodeResponse
    all_nodes:Dict[int,CompleteStoryNodeResponse]

    class config:
        from_attributes=True


































































