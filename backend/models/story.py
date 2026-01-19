from sqlalchemy import Column, Integer, String,Boolean, DateTime, Text, ForeignKey,JSON
#this use to map sql data to fastapi
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from DB.database import Base

#here i created sqlalchemy table jese ham sql me karte hai table and tables ke colums 

class Story(Base):#ek stories naam ka table hoga class use kiya kyus ki parent child ko acess kar sakta hai 
    __tablename__="stories"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    session_id=Column(String,index=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    nodes= relationship("StoryNode",back_populates="story")

class StoryNode(Base):
    __tablename__=  "StoryNode"

    id = Column(Integer,primary_key=True,index=True)
    story_id = Column(Integer,ForeignKey("stories.id"),index=True)
    content = Column(String)
    is_root = Column(Boolean,default=False)
    is_ending=Column(Boolean,default=False)
    is_winning_ending=Column(Boolean,default=False)
    options=Column(JSON,default=list)

    story = relationship("Story",back_populates="nodes")


















































































