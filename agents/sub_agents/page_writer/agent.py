"""Page Writer Agent for Kids Story Creator.

This agent helps children write story pages while preserving their voice and ideas.
It provides light grammar correction and optional story starters without taking over the writing.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from .prompts import instruction_page_writer_agent

from config.settings import get_config
from google.adk.models.lite_llm import LiteLlm

config = get_config()
model = LiteLlm(model=config.text_model_name)

page_writer_agent = Agent(
    model=model,
    name="page_writer_agent",
    instruction=instruction_page_writer_agent(),
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Helps children write story pages while preserving their voice and providing light grammar correction.",
)

page_writer_tool = AgentTool(agent=page_writer_agent)

