#!/usr/bin/env python3
"""Command-line interface for running the StoryCoach agent without the UI.

Usage:
    python -m src.cli
    python src/cli.py

Note: The Runner API may vary depending on your Google ADK version.
If you encounter errors, you may need to adjust the `run()` method call
in this file to match your ADK version's API.
"""

import sys
import uuid
from pathlib import Path
from typing import Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import after path setup
from google.genai import types  # noqa: E402
from src.agents.main_agent import story_coach_runner, session_service  # noqa: E402


def run_cli(session_id: Optional[str] = None):
    """Run an interactive CLI session with the StoryCoach agent.
    
    Args:
        session_id: Optional session ID to resume a previous conversation.
                   If None, a new session will be created.
    """
    user_id = "cli_user"  # Default user ID for CLI
    
    if session_id is None:
        session_id = str(uuid.uuid4())
        print(f"Starting new session: {session_id}")
        # Create the session in the session service
        try:
            session_service.create_session_sync(
                app_name="agents",
                user_id=user_id,
                session_id=session_id
            )
        except Exception:
            # Session might already exist or creation might not be needed
            # Continue anyway as Runner might handle it
            pass
    else:
        print(f"Resuming session: {session_id}")
    
    print("\n" + "="*60)
    print("StoryCoach CLI - Interactive Story Creation")
    print("="*60)
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("Type 'new' to start a new story session.")
    print("="*60 + "\n")
    
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nGoodbye! Thanks for creating a story with StoryCoach!")
                break
            
            if user_input.lower() == 'new':
                session_id = str(uuid.uuid4())
                print(f"\nStarting new session: {session_id}\n")
                # Create the new session
                try:
                    session_service.create_session_sync(
                        app_name="agents",
                        user_id=user_id,
                        session_id=session_id
                    )
                except Exception:
                    pass
                continue
            
            # Send message to the agent
            try:
                # Create Content object from user input
                user_message = types.Content(
                    parts=[types.Part(text=user_input)],
                    role="user"
                )
                
                # Use the Runner's run method
                # Runner.run() returns a generator of events
                events = story_coach_runner.run(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=user_message
                )
                
                # Collect the response from events
                response_text_parts = []
                for event in events:
                    # Try to extract text from various event structures
                    text = None
                    
                    # Check if event has content directly
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts') and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    text = part.text
                                    break
                    
                    # Check if event has text directly
                    if not text and hasattr(event, 'text') and event.text:
                        text = event.text
                    
                    # Check if event has message with content
                    if not text and hasattr(event, 'message'):
                        msg = event.message
                        if hasattr(msg, 'content') and msg.content:
                            if hasattr(msg.content, 'parts') and msg.content.parts:
                                for part in msg.content.parts:
                                    if hasattr(part, 'text') and part.text:
                                        text = part.text
                                        break
                    
                    # Add text to response if found
                    if text:
                        response_text_parts.append(text)
                
                # Combine all text parts
                response_text = ' '.join(response_text_parts) if response_text_parts else None
                
                if response_text:
                    print(f"\nStoryCoach: {response_text}\n")
                else:
                    print("\nStoryCoach: [No response text available]\n")
                    
            except Exception as e:
                error_msg = str(e)
                # Provide more helpful error messages for common issues
                if "Model" in error_msg and "not found" in error_msg:
                    print(f"\nError: {error_msg}")
                    print("\nThis appears to be a model configuration issue.")
                    print("Please check your .env file and ensure TEXT_MODEL_NAME")
                    print("is set to a valid Google ADK model identifier.\n")
                else:
                    print(f"\nError: {error_msg}\n")
                print("Please try again or type 'quit' to exit.\n")
                
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run StoryCoach agent via command line"
    )
    parser.add_argument(
        '--session-id',
        type=str,
        help="Resume a previous conversation with a specific session ID"
    )
    
    args = parser.parse_args()
    run_cli(session_id=args.session_id)


if __name__ == "__main__":
    main()

