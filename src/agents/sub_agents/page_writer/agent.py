"""Page Writer Agent for Kids Story Creator.

This agent helps children write story pages while preserving their voice and ideas.
It provides light grammar correction and optional story starters without taking over the writing.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from .prompts import instruction_page_writer_agent

from src.config.settings import get_config

config = get_config()

page_writer_agent = Agent(
    model=config.text_model_name,
    name="page_writer_agent",
    instruction=instruction_page_writer_agent(),
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Helps children write story pages while preserving their voice and providing light grammar correction.",
)

page_writer_tool = AgentTool(agent=page_writer_agent)

