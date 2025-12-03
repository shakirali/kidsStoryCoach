# Kids Story Creator

A conversational AI system for helping children (ages 5-11) create their own stories using Google Agent Development Kit (ADK).

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables** (create a `.env` file):
```
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
TEXT_MODEL_NAME=your_text_model
IMAGE_MODEL_NAME=your_image_model
MAX_STORY_PAGES=10
OUTPUT_DIR=./story_images
```

**Note:** No package installation needed! The flat structure works directly.

## Running Agents

### Using adk web

```bash
adk web agents
```

This will discover the `story_coach` agent in `agents/story_coach/`.

### Using CLI

```bash
python cli.py
```

### Programmatic Usage

```python
from agents.story_coach.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

session_service = InMemorySessionService()
runner = Runner(app_name="agents", agent=root_agent, session_service=session_service)
```

## Project Structure

```
agents/
  ├── story_coach/          # Agent directory for adk web
  │   ├── __init__.py
  │   ├── agent.py          # Contains root_agent
  │   └── prompts.py
  └── sub_agents/           # Specialist agents
config/                     # Configuration
utils/                      # Utilities
cli.py                      # CLI interface
main.py                     # Main entry point
```

**Simple flat structure - no `src/` folder needed!**

## Architecture

The system uses a root `StoryCoach` agent that orchestrates specialist agents:
- **ContentModerationAgent**: Ensures all content is safe for children
- **TitleGeneratorAgent**: Generates story titles
- **CoverAgent**: Creates cover descriptions
- **PageWriterAgent**: Helps children write pages while preserving their voice
- **PageIllustrationAgent**: Generates page illustrations
