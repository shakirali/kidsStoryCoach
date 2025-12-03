"""Lightweight helpers for loading and reading environment variables.

Uses python-dotenv to populate os.environ from a local .env file without
overwriting already-set environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env(env_path: str | Path = ".env") -> bool:
    """Load environment variables from a .env file if it exists.

    Returns True if a file was found and loaded, False otherwise.
    """
    env_file = Path(env_path)
    if not env_file.exists():
        return False
    load_dotenv(env_file, override=False)
    return True


def get_env(
    key: str,
    default: Optional[str] = None,
    *,
    required: bool = False,
) -> str:
    """Retrieve an environment variable with optional default/required semantics."""
    value = os.getenv(key, default)
    if required and value is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value


# Load .env values once at import; does not override existing environment.
load_env()
