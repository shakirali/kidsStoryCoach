# Kids Story Creator

A conversational AI system for helping children (ages 5-11) create their own stories using Google Agent Development Kit (ADK).

## Running Agents Without the UI

You can run the StoryCoach agent via command line without using the Gradio UI in two ways:

### 1. Interactive CLI

Use the interactive command-line interface to chat with the StoryCoach agent:

```bash
python -m src.cli
# or
python src/cli.py
```

You can also resume a previous conversation by providing a session ID:

```bash
python src/cli.py --session-id <your-session-id>
```

**Commands:**
- Type your messages to interact with the agent
- Type `quit`, `exit`, or `bye` to end the conversation
- Type `new` to start a new story session

### 2. Programmatic Usage

For automated testing or batch processing, you can use the agent programmatically:

```python
from src.agents.main_agent import story_coach_runner
import uuid

session_id = str(uuid.uuid4())

# Send a message to the agent
response = story_coach_runner.run(
    message="Hi! My name is Alex",
    session_id=session_id
)

# Extract and use the response
if hasattr(response, 'text'):
    print(response.text)
```

See `examples/run_agent_simple.py` for a complete example.

### Example Script

Run the example script to see a sample conversation:

```bash
python examples/run_agent_simple.py
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create a `.env` file):
```
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
TEXT_MODEL_NAME=your_text_model
IMAGE_MODEL_NAME=your_image_model
MAX_STORY_PAGES=10
OUTPUT_DIR=./story_images
```

3. Run the CLI:
```bash
python -m src.cli
```

## Architecture

The system uses a root `StoryCoach` agent that orchestrates specialist agents:
- **ContentModerationAgent**: Ensures all content is safe for children
- **TitleGeneratorAgent**: Generates story titles
- **CoverAgent**: Creates cover descriptions
- **PageWriterAgent**: Helps children write pages while preserving their voice
- **PageIllustrationAgent**: Generates page illustrations

See `specifictions/AgentsFramework.md` for detailed architecture documentation.
