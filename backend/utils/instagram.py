# utils/instagram.py

import os
import urllib.parse
import requests
import google.generativeai as genai
import json
import re

# Configure Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class InstagramGenerator:
    def __init__(self):
        self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')

    def generate_image_url(self, prompt: str, width: int = 1080, height: int = 1080) -> str:
        """
        Generate an Instagram-style image using pollinations.ai
        Returns direct image URL
        """
        full_prompt = f"{prompt}, Instagram post, high quality, trending, aesthetic"
        encoded_prompt = urllib.parse.quote(full_prompt)
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true"

    def clean_gemini_json_response(self, response_text: str) -> str:
        """
        Removes triple backticks and optional 'json' from Gemini's markdown code block.
        """
        cleaned = response_text.strip()
        # Remove leading triple backticks and optional 'json'
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        # Remove trailing triple backticks
        cleaned = re.sub(r"\s*```$", "", cleaned)
        return cleaned


    def _parse_gemini_response(self, response_text: str) -> dict:
        """
        Parse Gemini's JSON response, flatten hashtags array to string if needed,
        and remove hashtags from the caption if they are present.
        """
        cleaned = self.clean_gemini_json_response(response_text)
        try:
            result = json.loads(cleaned)
            caption = result.get("caption", "")
            hashtags = result.get("hashtags", [])
            if isinstance(hashtags, list):
                hashtags_str = " ".join(hashtags)
            else:
                hashtags_str = hashtags

            # Remove hashtags from the end of the caption if present
            if hashtags_str and hashtags_str in caption:
                caption = caption.replace(hashtags_str, "").strip()
            # Also, remove any trailing hashtags from caption
            caption = re.sub(r"(#\w+\s*)+$", "", caption).strip()

            return {"caption": caption, "hashtags": hashtags_str}
        except Exception:
            # Fallback: treat the whole text as caption
            return {"caption": cleaned, "hashtags": ""}


    def generate_caption_and_hashtags(self, prompt: str) -> dict:
        """
        Generate Instagram caption and hashtags using Gemini 1.5 Pro.
        Returns {'caption': str, 'hashtags': str}
        """
        system_prompt = (
            "You are an Instagram content creator. "
            "Generate: 1 engaging caption (with emojis), and 5-7 relevant hashtags. "
            "Return only valid JSON, no markdown or code block formatting. "
            'Format: {"caption": "...", "hashtags": ["#tag1", "#tag2", ...]}'
        )
        response = self.gemini_model.generate_content([
            system_prompt,
            f"Post content: {prompt}"
        ])
        return self._parse_gemini_response(response.text)

    def create_instagram_post(self, user_prompt: str) -> dict:
        """
        Complete Instagram post generator.
        Returns:
        {
            "image_url": "https://...",
            "caption": "Engaging caption...",
            "hashtags": "#tag1 #tag2 #tag3"
        }
        """
        # Generate image
        image_url = self.generate_image_url(user_prompt)
        # Generate text content
        text_content = self.generate_caption_and_hashtags(user_prompt)
        return {
            "image_url": image_url,
            "caption": text_content.get("caption", "Check out this new post! 🚀"),
            "hashtags": text_content.get("hashtags", "#AI #GeneratedContent"),
        }
