"""Story Title Generator Agent for Kids Story Creator.

This agent generates engaging, age-appropriate story titles based on the child's name and story concept.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from .prompts import instruction_title_agent

from config.settings import get_config
from google.adk.models.lite_llm import LiteLlm

config = get_config()

model = LiteLlm(model=config.text_model_name)

title_generator_agent = Agent(
    model=model,
    name="title_agent",
    instruction=instruction_title_agent(),
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Generates creative story titles for children's stories.",
)

title_generator_tool = AgentTool(agent=title_generator_agent)
