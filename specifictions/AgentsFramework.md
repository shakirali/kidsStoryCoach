# Kids Story Creator – Agent Framework & Architecture (Final AgentTool Design)

This document is the **single source of truth** for the Kids Story Creator app.  
It combines the previous *Agents.md* (architecture/design) and *AgentsFramework.md* (implementation) into one unified spec.

- **Framework:** Google Agent Development Kit (ADK) – Python  
- **Frontend:** Gradio 6 (ChatInterface + Story Preview panel)  
- **Models:** OpenAI / Gemini models via ADK-compatible clients  
- **Pattern:** Root `LlmAgent` + AgentTools (specialist agents)  
- **Session:** ADK SessionService (in-memory or DB-backed)  

---

## 🎯 Goal

Create an interactive story-writing experience for children (ages 5–11) where:

- A friendly **StoryCoach** agent chats with the child.
- The LLM asks for their **name**, **story idea**, and **what happens next**.
- The LLM delegates tasks (title, cover, page text, page illustrations) to specialist agents via **AgentTools**.
- A **live preview panel** shows the storybook as it is being built (title, cover, pages).
- The child can continue adding pages until they say **“finish story”**.
- The story can be **exported** (images/PDF/text) when complete.

---

## 🌟 Design Principles

1. **Child-Centred**  
   - Encourage kids to use their own ideas and imagination.  
   - The system supports them rather than taking over.

2. **Help Kids**  
   - Fix grammar/punctuation and suggest starters.  
   - Do NOT write full pages or entire stories.  
   - Preserve the child’s voice.
   - Encourage them and provide hints if asked.

3. **Safety First**  
   - Strong content moderation on input and generated output.  
   - Kid-friendly rejection and guidance messages.

4. **Conversational Flow (LLM-driven)**  
   - The child chats in natural language.  
   - The StoryCoach decides when to use tools (agents) based on conversation context.

5. **Visual Engagement**  
   - Generate cover and page illustrations.  
   - Keep style consistent, colourful, and kid-friendly.

---

## 🧩 Agent Architecture (Conceptual)

We use one root conversational agent and several specialist agents.

### 1. StoryCoach (Root Agent)

- **Type:** `LlmAgent` (chat-facing orchestration agent)
- **Role:** The only agent that talks to the child.
- **Responsibilities:**
  - Greet the child.
  - Ask for name and story concept.
  - Call Content Moderation on inputs and outputs.
  - Use AgentTools to:
    - generate title (`TitleAgent`),
    - generate cover (`CoverAgent`),
    - help write pages (`PageWriterAgent`),
    - generate page illustrations (`PageIllustrationAgent`).
  - Maintain story progress (current page, completion).
  - Detect when the child’s story is finished.
  - Coordinate export (if enabled).

The StoryCoach does not directly perform specialized creative tasks; it delegates via tools.

---

### 2. ContentModerationAgent

- **Type:** Guardrail / Safety Agent (implemented as an LLM agent or dedicated moderation tool).
- **Purpose:** Ensure all inputs and generated content are safe for children.

**Responsibilities:**

- Check child inputs (name, concept, per-page descriptions).
- Check generated content:
  - titles,
  - page text,
  - illustration prompts.
- Apply safety rules and thresholds.
- Return decisions: approved / rejected + kid-friendly messages.
- Apply additional filtering for borderline content.

**Safety Categories (at minimum):**

- Violence  
- Profanity  
- Adult content  
- Dangerous content  
- Hate speech  
- Harassment  

---

### 3. TitleAgent

- **Type:** `LlmAgent` (wrapped as `AgentTool`)
- **Purpose:** Generate an engaging, age-appropriate story title.

**Inputs:**

- `author_name`
- `story_concept`

**Output:**

- `story_title` (string, max 60 characters)

**Constraints:**

- Creative, fun, and age-appropriate.
- Reflects the story concept.
- No explanation, title only.

---

### 4. CoverAgent

- **Type:** `LlmAgent` (wrapped as `AgentTool`)
- **Purpose:** Generate a cover description or image prompt (and optionally trigger image generation).

**Inputs:**

- `author_name`
- `story_concept`
- `story_title`

**Output:**

- Cover prompt text, and/or
- `cover_image` URL/path (if image generation is integrated).

**Requirements:**

- Bright, engaging, kid-friendly imagery.
- Visual style consistent with children’s storybooks.

---

### 5. PageWriterAgent

- **Type:** `LlmAgent` (wrapped as `AgentTool`)
- **Purpose:** Help the child write each page while preserving their voice.

**Inputs:**

- `child_page_description` (raw input)
- `story_title`
- `story_concept`
- `current_page_number`
- Previous pages (for continuity, if needed)

**Responsibilities:**

- Lightly correct grammar and punctuation.
- Suggest a short story starter (e.g. first sentence) if helpful.
- Maintain continuity with previous pages.
- Do NOT write full pages or the whole story.

**Output:**

- Final page text (cleaned child’s content + optional starter).

---

### 6. PageIllustrationAgent

- **Type:** `LlmAgent` (wrapped as `AgentTool`; may call image API under the hood)
- **Purpose:** Generate illustrations for each page.

**Inputs:**

- `page_text`
- `page_number`
- `story_title` / `story_concept`
- Optional: previous style hints (for consistency)

**Output:**

- Image prompt and/or `image_url` for the page.

**Requirements:**

- Consistent colour palette and art style.
- Kid-friendly, non-violent, non-scary visuals.

---

## 🧠 Session Handling with Google ADK

### Mandatory Requirements

- Must use ADK `SessionService` (e.g. `InMemorySessionService`) for all story state.
- No custom or ad-hoc session stores.

### Session Data Structure (Conceptual)

```python
{
  "session_id": str,
  "author_name": str | None,
  "story_concept": str | None,
  "story_title": str | None,
  "cover_image": str | None,            # path or URL
  "current_page_number": int,
  "pages": [
      {
        "page_number": int,
        "text": str,
        "image_url": str | None,
      }
  ],
  "style_references": {
    "color_palette": list[str] | None,
    "art_style": str | None,
    "character_notes": str | None,
  },
  "story_complete": bool,
}
