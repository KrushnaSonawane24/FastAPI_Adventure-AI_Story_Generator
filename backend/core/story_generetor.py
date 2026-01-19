from sqlalchemy.orm import Session
import os
import json
import requests
from dotenv import load_dotenv
from models.story import Story, StoryNode
from core.prompts import STORY_PROMPT
from core.models import StoryLLMResponse, StoryNodeLLM

load_dotenv()

class StoryGenerator:
    @classmethod
    def _get_groq_response(cls, prompt: str) -> str:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a creative story writer that creates engaging choose-your-own-adventure stories in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "llama-3.3-70b-versatile",
            "temperature": 0.7,
            "max_tokens": 4096
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                error_detail = response.text
                raise ValueError(f"Groq API error {response.status_code}: {error_detail}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to connect to Groq API: {str(e)}")

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        prompt = STORY_PROMPT.replace("{theme}", theme)
        prompt += f"\n\nCreate a story with theme: {theme}"
        
        story_text = cls._get_groq_response(prompt)
        
        if "```json" in story_text:
            story_text = story_text.split("```json")[1].split("```")[0].strip()
        elif "```" in story_text:
            story_text = story_text.split("```")[1].split("```")[0].strip()
        
        try:
            story_data = json.loads(story_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse story JSON: {e}\nResponse: {story_text[:500]}")
        
        story_llm = StoryLLMResponse.model_validate(story_data)
        story_db = Story(title=story_llm.title, session_id=session_id)
        db.add(story_db)
        db.flush()
        
        root_node_data = story_llm.rootNode
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)
        
        db.commit()
        return story_db

    @classmethod
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isWinningEnding,
            options=[]
        )
        db.add(node)
        db.flush()
        
        if not node.is_ending and node_data.options:
            options_list = []
            for option in node_data.options:
                # Convert dict to Pydantic model if needed
                next_node_data = option.nextNode
                if isinstance(next_node_data, dict):
                    next_node_data = StoryNodeLLM.model_validate(next_node_data)
                
                child_node = cls._process_story_node(db, story_id, next_node_data, False)
                options_list.append({"text": option.text, "node_id": child_node.id})
            node.options = options_list
        
        db.flush()
        return node