"""Helper functions for evaluating agent outputs using the judge agent.

This module provides utilities to simplify the process of evaluating
agent outputs with the judge agent.
"""

import json
import re
from typing import Dict, Any, Optional
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from .judge_agent import judge_agent


def parse_json_response(text: str) -> dict:
    """
    Parse JSON from judge agent response.
    
    The judge should return valid JSON, but sometimes LLMs wrap it in text.
    This function tries to extract JSON from the response.
    
    Args:
        text: The raw text response from the judge agent
        
    Returns:
        Parsed JSON as a dictionary
        
    Raises:
        ValueError: If no valid JSON can be found
    """
    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from text (look for {...})
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    raise ValueError(f"Could not parse JSON from response: {text[:200]}")


async def call_judge_async(
    query: str,
    runner: Runner,
    user_id: str,
    session_id: str
) -> str:
    """
    Send a query to the judge agent asynchronously and return the final response text.
    
    Args:
        query: The evaluation input query
        runner: The Runner instance for the judge agent
        user_id: User identifier
        session_id: Session identifier
        
    Returns:
        The final response text as a string
    """
    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = ""

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            break

    return final_response_text


async def evaluate_with_judge(
    judge_instruction: str,
    evaluation_input: str,
    session_service: InMemorySessionService,
    runner: Runner,
    user_id: str,
    session_id: str,
    app_name: str = "judge_test",
    expected_min_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    Evaluate agent output using the judge agent.
    
    This is a convenience function that handles the full evaluation workflow:
    1. Updates the judge agent's instruction
    2. Creates a session
    3. Calls the judge agent
    4. Parses the JSON response
    5. Validates the structure
    6. Optionally checks minimum score
    
    Args:
        judge_instruction: The judge prompt instruction to use
        evaluation_input: The input to send to the judge (formatted string)
        session_service: The session service instance
        runner: The Runner instance for the judge agent
        user_id: User identifier
        session_id: Session identifier
        app_name: Application name for session creation
        expected_min_score: Optional minimum overall score to validate
        
    Returns:
        Dictionary with evaluation results including:
        - scores: Dictionary of individual scores
        - overall_score: Average of all scores
        - reasoning: Explanation of the evaluation
        - pass: Boolean indicating if overall_score >= 3.5 (or expected_min_score if provided)
        
    Raises:
        ValueError: If JSON cannot be parsed from judge response
        AssertionError: If expected_min_score is provided and not met
    """
    # Update judge agent instruction for this evaluation type
    judge_agent.instruction = judge_instruction
    
    # Create session
    session = await session_service.create_session(
        session_id=session_id,
        user_id=user_id,
        app_name=app_name
    )
    
    # Call judge agent
    response_text = await call_judge_async(
        query=evaluation_input,
        runner=runner,
        user_id=user_id,
        session_id=session.id
    )
    
    # Parse JSON response
    result = parse_json_response(response_text)
    
    # Validate structure
    required_fields = ["scores", "overall_score", "reasoning", "pass"]
    for field in required_fields:
        if field not in result:
            raise ValueError(f"Judge response missing required field: {field}")
    
    # Validate scores structure
    scores = result["scores"]
    if not isinstance(scores, dict):
        raise ValueError("Judge response 'scores' must be a dictionary")
    
    # Check minimum score if provided
    if expected_min_score is not None:
        overall_score = result["overall_score"]
        if overall_score < expected_min_score:
            raise AssertionError(
                f"Judge evaluation score {overall_score} below minimum {expected_min_score}. "
                f"Reasoning: {result.get('reasoning', 'N/A')}"
            )
    
    return result

