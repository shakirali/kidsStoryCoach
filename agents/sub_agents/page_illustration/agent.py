"""Page Illustration Image Generation Agent for Kids Story Creator.

This agent generates kid-friendly illustration images for story pages.
It maintains consistent art style and colour palette across all pages.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool
from google.genai import types
from .prompts import instruction_page_illustration_agent
from agents.sub_agents.cover_agent.image_generator import generate_image

from config.settings import get_config
from google.adk.models.lite_llm import LiteLlm


def generate_page_image(prompt: str) -> str:
    """
    Generate a page illustration image from a text prompt. Use this after creating the image prompt description.
    
    Args:
        prompt: Text description of the page illustration to generate
    
    Returns:
        Path to the generated image file
    """
    return generate_image(prompt, prefix="page")


# Create function tool for image generation
generate_image_tool = FunctionTool(func=generate_page_image)

config = get_config()
model = LiteLlm(model=config.text_model_name)

page_illustration_agent = Agent(
    model=model,
    name="page_illustration_agent",
    instruction=instruction_page_illustration_agent(),
    tools=[generate_image_tool],
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Generates child-friendly illustration images for story pages with consistent style.",
)

page_illustration_tool = AgentTool(agent=page_illustration_agent)
