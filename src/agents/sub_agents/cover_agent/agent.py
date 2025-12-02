"""Story Title Generator Agent for Kids Story Creator.

This agent generates engaging, age-appropriate story titles based on the child's name and story concept.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from prompts import instruction_cover_agent

from src.config.settings import get_config

config = get_config()

instruction_cover_agent = Agent(
    model=config.image_model_name,
    name="cover_agent",
    instruction=instruction_cover_agent(),
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Generates child-friendly cover illustration prompts.",
)

cover_tool = AgentTool(agent=instruction_cover_agent)
