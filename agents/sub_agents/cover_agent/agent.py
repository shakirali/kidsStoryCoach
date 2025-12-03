"""Cover Image Generation Agent for Kids Story Creator.

This agent generates kid-friendly cover images for storybooks.
It first generates a prompt, then creates the actual image.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool
from google.genai import types
from .prompts import instruction_cover_agent
from .image_generator import generate_image

from config.settings import get_config
from google.adk.models.lite_llm import LiteLlm


def generate_cover_image(prompt: str) -> str:
    """
    Generate a cover image from a text prompt. Use this after creating the image prompt description.
    
    Args:
        prompt: Text description of the cover image to generate
    
    Returns:
        Path to the generated image file
    """
    return generate_image(prompt, prefix="cover")


# Create function tool for image generation
generate_image_tool = FunctionTool(func=generate_cover_image)

config = get_config()
model = LiteLlm(model=config.text_model_name)

cover_agent = Agent(
    model=model,
    name="cover_agent",
    instruction=instruction_cover_agent(),
    tools=[generate_image_tool],
    generate_content_config=types.GenerateContentConfig(temperature=0.7),
    description="Generates child-friendly cover images for storybooks.",
)

cover_tool = AgentTool(agent=cover_agent)
