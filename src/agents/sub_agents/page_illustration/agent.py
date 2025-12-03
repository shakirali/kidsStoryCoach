"""Page Illustration Agent for Kids Story Creator.

This agent generates kid-friendly illustration prompts for story pages.
It maintains consistent art style and colour palette across all pages.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from .prompts import instruction_page_illustration_agent

from src.config.settings import get_config

config = get_config()

page_illustration_agent = Agent(
    model=config.image_model_name,
    name="page_illustration_agent",
    instruction=instruction_page_illustration_agent(),
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Generates child-friendly illustration prompts for story pages with consistent style.",
)

page_illustration_tool = AgentTool(agent=page_illustration_agent)

