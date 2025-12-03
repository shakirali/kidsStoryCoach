#!/usr/bin/env python3
"""Simple example script showing how to run the StoryCoach agent programmatically.

This script demonstrates a basic interaction with the agent without the UI.
You can modify this to create automated tests or batch processing scripts.

Usage:
    python examples/run_agent_simple.py
"""

import sys
import uuid
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.main_agent import story_coach_runner


def example_conversation():
    """Example of a simple conversation with the StoryCoach agent."""
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}\n")
    
    # Example conversation flow
    messages = [
        "Hi!",
        "My name is Alex",
        "I want to write a story about a brave little robot",
        "The robot goes on an adventure to find its missing friend",
        "The robot searches through a magical forest",
        "The robot finds its friend and they return home together",
        "I'm done!"
    ]
    
    print("="*60)
    print("Example Conversation with StoryCoach")
    print("="*60)
    print()
    
    for user_message in messages:
        print(f"You: {user_message}")
        
        try:
            # Send message to the agent
            response = story_coach_runner.run(
                message=user_message,
                session_id=session_id
            )
            
            # Extract response text
            response_text = None
            if hasattr(response, 'text'):
                response_text = response.text
            elif hasattr(response, 'content'):
                content = response.content
                if isinstance(content, str):
                    response_text = content
                elif isinstance(content, list) and len(content) > 0:
                    text_parts = []
                    for part in content:
                        if hasattr(part, 'text'):
                            text_parts.append(part.text)
                        elif isinstance(part, str):
                            text_parts.append(part)
                    response_text = ' '.join(text_parts)
                else:
                    response_text = str(content)
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)
            
            if response_text:
                print(f"StoryCoach: {response_text}")
            else:
                print(f"StoryCoach: [Response received]")
            
            print()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Note: You may need to adjust the Runner API call based on your Google ADK version.")
            break
    
    print("="*60)
    print("Conversation complete!")
    print("="*60)


if __name__ == "__main__":
    example_conversation()

