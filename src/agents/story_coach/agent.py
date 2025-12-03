"""StoryCoach Root Agent for Kids Story Creator.

This is the main conversational agent that interacts with children and orchestrates
the story creation process by delegating to specialist agents via AgentTools.

This file is required for adk web to discover the root_agent.

Simple setup: Uses environment variables directly, no package installation needed.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root (simple, no config module needed)
project_root = Path(__file__).parent.parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Add project root to path for imports (simple fallback)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
from google.genai import types

# Use environment variables directly (no config module dependency)
TEXT_MODEL_NAME = os.getenv("TEXT_MODEL_NAME", "gpt-4o-mini")

from .prompts import instruction_story_coach
from src.agents.sub_agents.content_moderation.agent import content_moderation_tool
from src.agents.sub_agents.title_generator.agent import title_generator_tool
from src.agents.sub_agents.cover_agent.agent import cover_tool
from src.agents.sub_agents.page_writer.agent import page_writer_tool
from src.agents.sub_agents.page_illustration.agent import page_illustration_tool

# Root StoryCoach agent
# This variable name must be exactly 'root_agent' for adk web to discover it
root_agent = LlmAgent(
    model=TEXT_MODEL_NAME,
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

