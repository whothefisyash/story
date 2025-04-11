# D:/Ahh/Projects/story/backend/utils/storage_manager.py
import os
import time
import shutil
import re

class StoryAssetsManager:
    def __init__(self, base_path=None):
        # Default to your current asset storage location if none specified
        self.base_path = base_path or "D:/Ahh/Projects/story/backend/static"
    
    def get_story_dir(self, story_id):
        """Get a clean, isolated directory for a story's assets"""
        # Sanitize the story_id to ensure it's safe for filesystem
        sanitized_id = re.sub(r'[^a-zA-Z0-9_-]', '', str(story_id))
        story_dir = os.path.join(self.base_path, sanitized_id)
        os.makedirs(story_dir, exist_ok=True)
        return story_dir
    
    def save_image(self, story_id, image_data=None, filename=None, image_url=None):
        """Save an image for a specific story from data or URL"""
        if not filename:
            filename = f"page_{int(time.time())}.png"
            
        image_path = os.path.join(self.get_story_dir(story_id), filename)
        
        if image_url:
            # Download from URL
            import requests
            response = requests.get(image_url, stream=True)
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        elif image_data:
            # Save from binary data
            with open(image_path, 'wb') as f:
                f.write(image_data)
                
        return f"/static/{story_id}/{filename}"
    
    def save_audio(self, story_id, audio_data=None, tts_text=None):
        """Save audio for a specific story from data or generate from text"""
        audio_filename = "story_audio.mp3"
        audio_path = os.path.join(self.get_story_dir(story_id), audio_filename)
        
        if tts_text:
            # Generate audio from text
            from gtts import gTTS
            tts = gTTS(tts_text)
            tts.save(audio_path)
        elif audio_data:
            # Save from binary data
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
                
        return f"/static/{story_id}/{audio_filename}"
    
    def clean_temp_assets(self, older_than_hours=24):
        """Clean up temporary assets older than a specified time"""
        now = time.time()
        for dir_name in os.listdir(self.base_path):
            if dir_name.startswith('temp_'):
                dir_path = os.path.join(self.base_path, dir_name)
                if os.path.isdir(dir_path):
                    created_time = os.path.getctime(dir_path)
                    if (now - created_time) > older_than_hours * 3600:
                        shutil.rmtree(dir_path)
