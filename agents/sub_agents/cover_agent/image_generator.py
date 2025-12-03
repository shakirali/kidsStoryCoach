"""Image generation utility for cover and page illustrations."""

import hashlib
from pathlib import Path
from typing import Optional

import requests
from openai import OpenAI

from config.settings import get_config


def generate_image(prompt: str, output_dir: Optional[str] = None, prefix: str = "image") -> str:
    """
    Generate an image using OpenAI's image generation API.
    
    Args:
        prompt: Text prompt describing the image to generate
        output_dir: Optional directory to save the image. If None, uses config OUTPUT_DIR.
        prefix: Prefix for the filename (e.g., "cover" or "page")
    
    Returns:
        Path to the saved image file
    """
    config = get_config()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=config.openai_api_key)
    
    # Use output_dir from config if not provided
    if output_dir is None:
        output_dir = config.output_dir
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate image using OpenAI API
        # OpenAI image generation uses the images.generate endpoint
        # Supported models: dall-e-2, dall-e-3
        # For gpt-image-1 models, they may use a different endpoint
        model = config.image_model_name.lower()
        
        # Handle different model types
        if "dall-e" in model or "dalle" in model:
            # Use DALL-E models
            dalle_model = "dall-e-3" if "3" in model else "dall-e-2"
            response = client.images.generate(
                model=dalle_model,
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard" if "3" in model else None
            )
            image_url = response.data[0].url
        elif "gpt-image" in model:
            # gpt-image models may need different handling
            # Try using the images.generate endpoint without model specification
            # or use a compatible model
            response = client.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
        else:
            # Default: try standard image generation
            response = client.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
        
        # Download and save the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Generate filename
        filename_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        filename = f"{prefix}_{filename_hash}.png"
        filepath = Path(output_dir) / filename
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_response.content)
        
        return str(filepath)
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate image: {e}") from e

