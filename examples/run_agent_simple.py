#!/usr/bin/env python3
"""Simple example script showing how to run the StoryCoach agent programmatically.

Usage:
    python examples/run_agent_simple.py
"""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from google.genai import types
from agents.main_agent import story_coach_runner, session_service


def example_conversation():
    session_id = str(uuid.uuid4())
    user_id = "example_user"
    print(f"Session ID: {session_id}\n")
    
    try:
        session_service.create_session_sync(
            app_name="agents",
            user_id=user_id,
            session_id=session_id
        )
    except Exception:
        pass
    
    messages = [
        "Hi!",
        "My name is Alex",
        "I want to write a story about a brave little robot",
    ]
    
    print("="*60)
    print("Example Conversation with StoryCoach")
    print("="*60)
    print()
    
    for user_message in messages:
        print(f"You: {user_message}")
        
        try:
            user_content = types.Content(
                parts=[types.Part(text=user_message)],
                role="user"
            )
            
            events = story_coach_runner.run(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content
            )
            
            response_text_parts = []
            for event in events:
                text = None
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                text = part.text
                                break
                if not text and hasattr(event, 'text') and event.text:
                    text = event.text
                if text:
                    response_text_parts.append(text)
            
            response_text = ' '.join(response_text_parts) if response_text_parts else None
            if response_text:
                print(f"StoryCoach: {response_text}")
            print()
            
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print("="*60)
    print("Conversation complete!")
    print("="*60)


if __name__ == "__main__":
    example_conversation()

