"""StoryCoach Runner and Session Service for CLI and programmatic usage."""

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from agents.story_coach.agent import root_agent

session_service = InMemorySessionService()
story_coach_runner = Runner(app_name="story_coach", agent=root_agent, session_service=session_service)

