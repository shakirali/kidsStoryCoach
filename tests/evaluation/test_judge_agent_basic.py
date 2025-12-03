"""Basic tests for the Evaluation Judge Agent.

This test module verifies that the judge agent:
1. Can be instantiated and run
2. Returns valid JSON output
3. Has the expected structure (scores, overall_score, reasoning, pass)
4. Produces scores in the valid range (1-5)
"""

import json
import re
import pytest
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.evaluation.judge_agent import judge_agent
from google.genai import types
import random


async def call_agent_async(query: str, runner, user_id: str, session_id: str) -> str:
    """
    Send a query to the agent asynchronously and return the final response text.
    
    Args:
        query: The user's input query
        runner: The Runner instance
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

@pytest.fixture
def session_id():
    """Create a random session id."""
    return str(random.randint(1000000000, 9999999999))

@pytest.fixture
def user_id():
    """Create a random user id."""
    return str(random.randint(1000000000, 9999999999))

@pytest.fixture
def app_name():
    return "judge_test"

@pytest.fixture
def session_service():
    """Create a session service for tests."""
    return InMemorySessionService()


@pytest.fixture
def judge_runner(session_service):
    """Create a runner for the judge agent."""
    return Runner(
        app_name="judge_test",
        agent=judge_agent,
        session_service=session_service
    )


@pytest.fixture(scope="session", autouse=True)
def cleanup_async_resources():
    """Ensure async resources are properly cleaned up after all tests."""
    yield
    # Try to clean up any pending async tasks
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is running, schedule cleanup
            pending = asyncio.all_tasks(loop)
            if pending:
                for task in pending:
                    if not task.done():
                        task.cancel()
    except RuntimeError:
        # No event loop, nothing to clean up
        pass


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


@pytest.mark.asyncio
async def test_judge_agent_returns_valid_json(judge_runner, session_service, session_id, user_id, app_name):
    """Test that the judge agent returns valid JSON output."""
    # Prepare test input
    test_input = """story_concept: A brave knight saves a dragon from an evil wizard
generated_title: The Knight's Dragon Friend"""
    
    # Create a session via session service
    session = await session_service.create_session(session_id=session_id, user_id=user_id, app_name=app_name)
    
    # Run the judge agent asynchronously
    response_text = await call_agent_async(test_input, judge_runner, user_id, session.id)
    
    # Verify we got a response
    assert response_text is not None, "Judge agent should return a response"
    assert len(response_text) > 0, "Judge agent response should not be empty"
    
    # Parse JSON
    result = parse_json_response(response_text)
    
    # Verify it's a dictionary
    assert isinstance(result, dict), "Judge should return a JSON object"


@pytest.mark.asyncio
async def test_judge_agent_output_structure(judge_runner, session_service, session_id, user_id, app_name):
    """Test that the judge agent output has the expected structure."""
    test_input = """story_concept: A magical forest adventure with talking animals
generated_title: The Enchanted Forest"""
    
    session = await session_service.create_session(session_id=session_id, user_id=user_id, app_name=app_name)
    response_text = await call_agent_async(test_input, judge_runner, user_id, session.id)
    result = parse_json_response(response_text)
    
    # Check required fields exist
    assert "scores" in result, "Output should contain 'scores' field"
    assert "overall_score" in result, "Output should contain 'overall_score' field"
    assert "reasoning" in result, "Output should contain 'reasoning' field"
    assert "pass" in result, "Output should contain 'pass' field"
    
    # Check scores structure
    scores = result["scores"]
    assert isinstance(scores, dict), "'scores' should be a dictionary"
    assert "relevance" in scores, "Scores should contain 'relevance'"
    assert "age_appropriateness" in scores, "Scores should contain 'age_appropriateness'"
    assert "creativity" in scores, "Scores should contain 'creativity'"
    assert "length" in scores, "Scores should contain 'length'"


@pytest.mark.asyncio
async def test_judge_agent_scores_range(judge_runner, session_service, session_id, user_id, app_name):
    """Test that all scores are in the valid range (1-5)."""
    test_input = """story_concept: A robot learns to dance
generated_title: Dancing Robot"""
    
    session = await session_service.create_session(session_id=session_id, user_id=user_id, app_name=app_name)
    response_text = await call_agent_async(test_input, judge_runner, user_id, session.id)
    result = parse_json_response(response_text)
    
    scores = result["scores"]
    
    # Check each score is in valid range
    for score_name, score_value in scores.items():
        assert isinstance(score_value, int), f"{score_name} should be an integer"
        assert 1 <= score_value <= 5, f"{score_name} should be between 1 and 5, got {score_value}"


@pytest.mark.asyncio
async def test_judge_agent_overall_score_calculation(judge_runner, session_service, session_id, user_id, app_name):
    """Test that overall_score is the average of individual scores."""
    test_input = """story_concept: A space adventure
generated_title: Journey to the Stars"""
    
    session = await session_service.create_session(session_id=session_id, user_id=user_id, app_name=app_name)
    response_text = await call_agent_async(test_input, judge_runner, user_id, session.id)
    result = parse_json_response(response_text)
    
    scores = result["scores"]
    overall_score = result["overall_score"]
    
    # Calculate expected average
    score_values = list(scores.values())
    expected_average = sum(score_values) / len(score_values)
    
    # Allow small floating point differences
    assert abs(overall_score - expected_average) < 0.01, \
        f"overall_score should be average of scores. Expected {expected_average}, got {overall_score}"


@pytest.mark.asyncio
async def test_judge_agent_pass_fail_logic(judge_runner, session_service, session_id, user_id, app_name):
    """Test that 'pass' field is correctly set based on overall_score."""
    test_input = """story_concept: A friendly monster
generated_title: The Friendly Monster"""
    
    session = await session_service.create_session(session_id=session_id, user_id=user_id, app_name=app_name)
    response_text = await call_agent_async(test_input, judge_runner, user_id, session.id)
    result = parse_json_response(response_text)
    
    overall_score = result["overall_score"]
    pass_value = result["pass"]
    
    # Verify pass is a boolean
    assert isinstance(pass_value, bool), "'pass' should be a boolean"
    
    # Verify pass logic: true if overall_score >= 3.5, false otherwise
    if overall_score >= 3.5:
        assert pass_value is True, f"pass should be True when overall_score ({overall_score}) >= 3.5"
    else:
        assert pass_value is False, f"pass should be False when overall_score ({overall_score}) < 3.5"


