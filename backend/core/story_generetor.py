from sqlalchemy.orm import Session
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from models.story import Story, StoryNode
from core.prompts import STORY_PROMPT
from core.models import StoryLLMResponse, StoryNodeLLM

load_dotenv()

class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=google_api_key, transport="rest")
        return genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        model = cls._get_llm()
        prompt = STORY_PROMPT.replace("{theme}", theme)
        prompt += f"\n\nCreate a story with theme: {theme}"
        response = model.generate_content(prompt)
        story_text = response.text
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
                child_node = cls._process_story_node(db, story_id, option.nextNode, False)
                options_list.append({"text": option.text, "node_id": child_node.id})
            node.options = options_list
        db.flush()
        return node