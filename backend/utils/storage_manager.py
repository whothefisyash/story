import os
import time
import shutil
import re
import requests
from gtts import gTTS

class StoryAssetsManager:
    def __init__(self, base_path=None,audio_dir=None):
        """
        Manages storage of story assets with conflict-safe filenames.
        """
        self.base_path = base_path or "D:/Ahh/Projects/story/backend/static"
        self.audio_dir = audio_dir or "D:/Ahh/Projects/story/backend/generated_audio"
        os.makedirs(self.audio_dir, exist_ok=True)


    def get_story_dir(self, story_id):
        """Create and return a sanitized directory path for a story"""
        sanitized_id = re.sub(r'[^a-zA-Z0-9_-]', '', str(story_id))
        story_dir = os.path.join(self.base_path, sanitized_id)
        os.makedirs(story_dir, exist_ok=True)
        return story_dir, sanitized_id

    def save_image(self, story_id, image_data=None, filename=None, image_url=None):
        """
        Save an image with conflict-safe filenames.
        Returns URL path like: /static/{sanitized_story_id}/page_1698765300_1.png
        """
        story_dir, sanitized_id = self.get_story_dir(story_id)

        # Generate unique filename
        if not filename:
            base_name = f"page_{int(time.time())}"
            extension = "png"
        else:
            base_name, extension = os.path.splitext(filename)
            extension = extension.lstrip('.')

        # Handle filename conflicts
        counter = 1
        final_filename = f"{base_name}.{extension}"
        while os.path.exists(os.path.join(story_dir, final_filename)):
            final_filename = f"{base_name}_{counter}.{extension}"
            counter += 1

        # Save the file
        image_path = os.path.join(story_dir, final_filename)
        if image_url:
            self._download_image(image_url, image_path)
        elif image_data:
            self._save_binary_data(image_data, image_path)

        return f"/static/{sanitized_id}/{final_filename}"

    def save_audio_global(self, tts_text):
        """
        Save audio to a single, fixed location (always overwritten).
        Returns the URL for frontend access.
        """
        audio_filename = "story_audio.mp3"
        audio_path = os.path.join(self.audio_dir, audio_filename)
        tts = gTTS(tts_text)
        tts.save(audio_path)
        return f"/generated_audio/{audio_filename}"

    def clean_temp_assets(self, older_than_hours=24):
        """Clean up temporary assets older than specified hours"""
        now = time.time()
        for dir_name in os.listdir(self.base_path):
            if dir_name.startswith('temp_'):
                dir_path = os.path.join(self.base_path, dir_name)
                if os.path.isdir(dir_path):
                    created_time = os.path.getctime(dir_path)
                    if (now - created_time) > older_than_hours * 3600:
                        shutil.rmtree(dir_path)

    # Helper methods
    def _download_image(self, url, save_path):
        """Download image from URL"""
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def _save_binary_data(self, data, save_path):
        """Save raw binary data to file"""
        with open(save_path, 'wb') as f:
            f.write(data)

    def _generate_tts(self, text, save_path):
        """Generate TTS audio from text"""
        tts = gTTS(text)
        tts.save(save_path)
