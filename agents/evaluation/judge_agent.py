"""Evaluation Judge Agent for Kids Story Creator.

This agent evaluates outputs from other agents using structured criteria
and returns scores with reasoning. It acts as an automated quality checker.

The judge agent uses a low temperature (0.0) for consistent, deterministic
evaluations. The instruction prompt can be swapped depending on what type
of output is being evaluated (titles, covers, pages, etc.).
"""

from google.adk.agents import Agent
from google.genai import types
from .prompts import instruction_title_judge

from config.settings import get_config
from google.adk.models.lite_llm import LiteLlm

config = get_config()
model = LiteLlm(model=config.text_model_name)

# Create the judge agent
# Note: We use temperature=0.0 for consistent, deterministic evaluations
# The instruction can be changed at runtime for different evaluation types
judge_agent = Agent(
    model=model,
    name="evaluation_judge",
    instruction=instruction_title_judge(),  # Default instruction (can be swapped)
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    description="Evaluates agent outputs against quality criteria and returns structured scores with reasoning.",
)

