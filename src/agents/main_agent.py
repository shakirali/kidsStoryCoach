"""StoryCoach Root Agent for Kids Story Creator.

This is the main conversational agent that interacts with children and orchestrates
the story creation process by delegating to specialist agents via AgentTools.
"""

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from src.config.settings import get_config
from src.agents.prompts import instruction_story_coach
from src.agents.sub_agents.content_moderation.agent import content_moderation_tool
from src.agents.sub_agents.title_generator.agent import title_generator_tool
from src.agents.sub_agents.cover_agent.agent import cover_tool
from src.agents.sub_agents.page_writer.agent import page_writer_tool
from src.agents.sub_agents.page_illustration.agent import page_illustration_tool

config = get_config()

# Root StoryCoach agent
root_agent = LlmAgent(
    model=config.text_model_name,
    name="StoryCoach",
    instruction=instruction_story_coach(),
    tools=[
        content_moderation_tool,
        title_generator_tool,
        cover_tool,
        page_writer_tool,
        page_illustration_tool,
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.8),
)

# Session service for maintaining story state
session_service = InMemorySessionService()

# Runner for executing conversations with the StoryCoach
story_coach_runner = Runner(agent=root_agent, session_service=session_service)
