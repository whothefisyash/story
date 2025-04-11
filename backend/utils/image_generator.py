import os
import requests

def generate_image(prompt, output_path=None):
    """
    Generates an image using Pollinations AI.

    Args:
        prompt (str): The text prompt describing the image.
        output_path (str): The path to save the generated image.

    Returns:
        str: The path to the saved image.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    if output_path is None:
        raise ValueError("Output path cannot be empty")

    print(f"Generating image for prompt: {prompt}")
    print(f"Saving image to: {output_path}")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        # Generate image using Pollinations AI
        image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
        print(f"Image URL: {image_url}")

        # Download and save the generated image
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code != 200:
            raise Exception(f"Failed to generate image, status code: {image_response.status_code}")

        with open(output_path, "wb") as f:
            for chunk in image_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Image saved at: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating image: {e}")
        raise e
