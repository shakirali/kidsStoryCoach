# Kids Story Creator

A conversational AI system for helping children (ages 5-11) create their own stories using Google Agent Development Kit (ADK).

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables** (create a `.env` file in the project root):
```
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
TEXT_MODEL_NAME=your_text_model
IMAGE_MODEL_NAME=your_image_model
MAX_STORY_PAGES=10
OUTPUT_DIR=./outputs
```

**Note:** The `.env` file is automatically loaded by `utils/env.py` using `python-dotenv`.

## Running the Application

### Using adk web

```bash
adk web agents
```

This will discover the `story_coach` agent in `agents/story_coach/`.

### Programmatic Usage

```python
from agents.main_agent import story_coach_runner

# Use the pre-configured runner
response = story_coach_runner.run(user_input="Hello!", session_id="your_session_id")
```

Or create your own runner:

```python
from agents.story_coach.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

session_service = InMemorySessionService()
runner = Runner(app_name="story_coach", agent=root_agent, session_service=session_service)
```

## Project Structure

```
agents/
  ├── main_agent.py          # Pre-configured runner for programmatic use
  ├── story_coach/           # Root StoryCoach agent (for adk web discovery)
  │   ├── __init__.py
  │   ├── agent.py           # Contains root_agent
  │   └── prompts.py
  └── sub_agents/            # Specialist agents as AgentTools
      ├── content_moderation/
      ├── title_generator/
      ├── cover_agent/        # Includes image_generator.py
      ├── page_writer/
      └── page_illustration/
config/
  └── settings.py            # Configuration management
utils/
  └── env.py                 # Environment variable helpers
outputs/                      # Generated images (cover and page illustrations)
specifictions/                # Architecture and evaluation specifications
tests/                        # Test directories (unit, integration, evaluation)
```

## Architecture

The system uses a root `StoryCoach` agent (`LlmAgent`) that orchestrates specialist agents via `AgentTool`:

- **StoryCoach** (Root Agent): Main conversational agent that interacts with children and delegates tasks
- **ContentModerationAgent**: Ensures all inputs and generated content are safe and age-appropriate
- **TitleGeneratorAgent**: Generates engaging, age-appropriate story titles
- **CoverAgent**: Generates cover image prompts and creates cover illustrations
- **PageWriterAgent**: Helps children write pages while preserving their voice (light grammar correction)
- **PageIllustrationAgent**: Generates page illustrations with consistent style

### Key Features

- **Session Management**: Uses ADK `InMemorySessionService` for story state
- **Image Generation**: Uses OpenAI's image generation API (DALL-E) for cover and page illustrations
- **Configuration**: Centralized config via `config/settings.py` with environment variable support
- **Safety First**: Content moderation on all inputs and outputs

## Configuration

All configuration is managed through environment variables loaded via `config/settings.py`:

- `OPENAI_API_KEY`: Required for text and image generation
- `GOOGLE_API_KEY`: Required for Google ADK
- `TEXT_MODEL_NAME`: LLM model name (e.g., "gpt-4o-mini")
- `IMAGE_MODEL_NAME`: Image generation model (e.g., "dall-e-3")
- `MAX_STORY_PAGES`: Maximum number of pages allowed per story
- `OUTPUT_DIR`: Directory where generated images are saved (default: `./outputs`)
