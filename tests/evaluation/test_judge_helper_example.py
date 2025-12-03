"""Example test demonstrating the use of evaluate_with_judge helper function.

This test shows how to use the helper function to simplify evaluation tests.
"""

import pytest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.evaluation.helpers import evaluate_with_judge
from agents.evaluation.prompts import instruction_title_judge
from agents.evaluation.judge_agent import judge_agent


@pytest.fixture
def session_id():
    """Create a random session id."""
    import random
    return str(random.randint(1000000000, 9999999999))


@pytest.fixture
def user_id():
    """Create a random user id."""
    import random
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


@pytest.mark.asyncio
async def test_helper_simplifies_evaluation(judge_runner, session_service, session_id, user_id, app_name):
    """Example test showing how the helper function simplifies evaluation."""
    # Prepare test input
    story_concept = "A brave knight saves a dragon from an evil wizard"
    generated_title = "The Knight's Dragon Friend"
    
    evaluation_input = f"story_concept: {story_concept}\ngenerated_title: {generated_title}"
    
    # Use the helper function - much simpler!
    result = await evaluate_with_judge(
        judge_instruction=instruction_title_judge(),
        evaluation_input=evaluation_input,
        session_service=session_service,
        runner=judge_runner,
        user_id=user_id,
        session_id=session_id,
        app_name=app_name,
        expected_min_score=3.5  # Optional: validate minimum score
    )
    
    # Verify the result structure
    assert "scores" in result
    assert "overall_score" in result
    assert "reasoning" in result
    assert "pass" in result
    
    # Verify scores
    scores = result["scores"]
    assert "relevance" in scores
    assert "age_appropriateness" in scores
    assert "creativity" in scores
    assert "length" in scores
    
    # Verify score ranges
    for score_value in scores.values():
        assert 1 <= score_value <= 5
    
    # Verify overall score meets minimum
    assert result["overall_score"] >= 3.5
    assert result["pass"] is True
    
    print(f"\nEvaluation Result:")
    print(f"  Scores: {scores}")
    print(f"  Overall: {result['overall_score']}")
    print(f"  Reasoning: {result['reasoning']}")

