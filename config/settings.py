"""Configuration helper for loading environment-backed settings."""

from __future__ import annotations

from dataclasses import dataclass

from utils.env import get_env, load_env


@dataclass(frozen=True)
class Config:
    openai_api_key: str
    google_api_key: str
    text_model_name: str
    image_model_name: str
    max_story_pages: int
    output_dir: str

    @classmethod
    def from_env(cls) -> "Config":
        """Build Config from environment variables (loading .env if present)."""
        load_env()
        max_pages_raw = get_env("MAX_STORY_PAGES", required=True)
        try:
            max_pages = int(max_pages_raw)
        except ValueError as exc:
            raise RuntimeError("MAX_STORY_PAGES must be an integer") from exc
        return cls(
            openai_api_key=get_env("OPENAI_API_KEY", required=True),
            google_api_key=get_env("GOOGLE_API_KEY", required=True),
            text_model_name=get_env("TEXT_MODEL_NAME", required=True),
            image_model_name=get_env("IMAGE_MODEL_NAME", required=True),
            max_story_pages=max_pages,
            output_dir=get_env("OUTPUT_DIR", required=True),
        )


# Singleton-style accessor
_CONFIG: Config | None = None


def get_config() -> Config:
    """Return a cached Config instance loaded from environment."""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = Config.from_env()
    return _CONFIG
