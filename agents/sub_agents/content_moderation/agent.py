"""Content Moderation Agent for Kids Story Creator.

This agent ensures all inputs and generated content are safe and age-appropriate
for children aged 5-11. It checks for violence, profanity, adult content,
dangerous content, hate speech, and harassment.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai import types
from .prompts import instruction_content_moderation_agent

from config.settings import get_config
from google.adk.models.lite_llm import LiteLlm

config = get_config()
model = LiteLlm(model=config.text_model_name)

content_moderation_agent = Agent(
    model=model,
    name="content_moderation_agent",
    instruction=instruction_content_moderation_agent(),
    generate_content_config=types.GenerateContentConfig(temperature=0.3),
    description="Checks content for safety and age-appropriateness, returning approval/rejection with kid-friendly messages.",
)

content_moderation_tool = AgentTool(agent=content_moderation_agent)

