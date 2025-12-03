"""StoryCoach Root Agent for Kids Story Creator.

This is the main conversational agent that interacts with children and orchestrates
the story creation process by delegating to specialist agents via AgentTools.
"""

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from src.agents.agent import root_agent

APP_NAME = "story_coach"
USER_ID = "1234"
SESSION_ID = "session1234"

# Session service for maintaining story state
session_service = InMemorySessionService()

session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

# Runner for executing conversations with the StoryCoach
# Use "agents" as app_name to match ADK's inference based on agent module location
story_coach_runner = Runner(app_name="agents", agent=root_agent, session_service=session_service)

def main():
    while True:
        user_input = input("You: ")
        response = story_coach_runner.run(user_input)
        print(response)

if __name__ == "__main__":
    main()