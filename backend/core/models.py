#for loading llm

from typing import List,Dict,Any,Optional
from pydantic import BaseModel,Field

class StoryOptionLLM( BaseModel):
    text:str=Field(description="the text of the optiona show to the user")
    nextNode:Dict[str,Any]=Field(description="the next node content and its option")


class StoryNodeLLM(BaseModel):
    content:str=Field(description="the main content of story node ")
    isEnding:bool=Field(description="wether this node is winning node ")
    isWinningEnding:bool=Field(description="wether this is node is winning ending node  ")
    options:Optional[List[StoryOptionLLM]]=Field(default=None)

class StoryLLMResponse(BaseModel):
    title:str=Field(description="the titel of the story")
    rootNode:StoryNodeLLM=Field(description="the root node of the story")




