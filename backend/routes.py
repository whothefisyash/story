from flask import Blueprint, jsonify, request
from flask import send_from_directory
from flask import send_file
from gtts import gTTS
import os
import random
import time
import json

from utils.story_generator import generate_story
from utils.image_generator import generate_image
from utils.storage_manager import StoryAssetsManager

import sqlite3
DATABASE = "skibidi_story.db"

# Define the absolute path for generated images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_IMAGES_DIR = os.path.join(BASE_DIR, "../generated_images")

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    """
    Root route to check if the server is running.
    """
    return jsonify({"message": "Welcome to Skibidi Story API!"})

@routes.route('/generate_story', methods=['POST'])
def generate_story_endpoint():
    """
    Endpoint to generate a story with images.
    Expected input: JSON with 'description', 'storyType', and optional 'moral'.
    """
    data = request.get_json()
    description = data.get('description')
    story_type = data.get('storyType', 'Bedtime')  # Default to Bedtime if not provided
    moral = data.get('moral', None)

    if not description:
        return jsonify({"error": "Description is required"}), 400

    try:
        # Generate story using the utility function
        print(f"Generating story with prompt: '{description}', type: '{story_type}', moral: '{moral}'")
        story_content = generate_story(description, story_type, moral)

        # Split story into pages (e.g., 2 sentences per page)
        sentences = story_content.split(". ")
        sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty sentences
        pages = [{"text": sentences[i], "image_prompt": sentences[i]} for i in range(len(sentences))]

        # Save images in a single directory
        image_dir = f"D:/Ahh/Projects/story/backend/static/generated_images/"
        os.makedirs(image_dir, exist_ok=True)

        generated_pages = []
        illustration_urls = []

        for i, page in enumerate(pages):
            try:
                image_filename = f"page_{i+1}.png"
                image_path = os.path.join(image_dir, image_filename)

                print(f"Generating image for page {i+1} with prompt: '{page['image_prompt'][:50]}...'")
                generate_image(page["image_prompt"], image_path)

                # Create properly formatted URLs for frontend
                image_url = f"/static/generated_images/{image_filename}"
                illustration_urls.append(image_url)
                generated_pages.append({"image": image_url, "text": page["text"]})

                print(f"Generated image saved at: {image_path}")
            except Exception as e:
                print(f"Error generating image for page {i+1}: {e}")
                illustration_urls.append("/static/placeholder.png")
                generated_pages.append({"image": "/static/placeholder.png", "text": page["text"]})

        return jsonify({
            "title": f"{story_type} Story: {description.split()[0]}",
            "content": story_content,
            "illustration_urls": illustration_urls,
            "pages": generated_pages
        })

    except Exception as e:
        print(f"Error generating story: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate story: {str(e)}"}), 500



@routes.route('/save_story', methods=['POST'])
def save_story():
    data = request.get_json()
    
    # Extract fields
    required_fields = ['user_id', 'title', 'description', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Serialize pages array to JSON
    pages = data.get('pages', [])
    pages_json = json.dumps(pages)

    # Build SQL query
    query = '''
        INSERT INTO stories 
        (user_id, title, description, content, 
         illustration_urls, pages, story_id, audio_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    values = (
        data['user_id'],
        data['title'],
        data['description'],
        data['content'],
        ",".join(data.get('illustrations', [])),
        pages_json,
        data.get('id'),
        data.get('audio_url', '')
    )

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return jsonify({
            "message": "Story saved successfully!",
            "id": cursor.lastrowid
        })
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()



@routes.route('/get_stories', methods=['GET'])
def get_stories():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, description, content, 
                   illustration_urls, pages, story_id, audio_url 
            FROM stories WHERE user_id=?
        ''', (user_id,))
        
        stories = []
        for row in cursor.fetchall():
            stories.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "content": row[3],
                "illustration_urls": row[4].split(",") if row[4] else [],
                "pages": json.loads(row[5]) if row[5] else [],
                "story_id": row[6],
                "audio_url": row[7]
            })
            
        return jsonify(stories)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()


@routes.route('/story/<int:story_id>', methods=['GET'])
def get_story_by_id(story_id):
    """
    Endpoint to fetch a single story by its ID.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, description, content, illustration_urls FROM stories WHERE id=?
    ''', (story_id,))
    
    story = cursor.fetchone()
    
    conn.close()
    
    if not story:
        return jsonify({"error": "Story not found"}), 404
    
    return jsonify({
        "id": story[0],
        "title": story[1],
        "description": story[2],
        "content": story[3],
        "illustration_urls": story[4].split(",")  # Convert back to list
    })


@routes.route('/generate_tts', methods=['POST'])
def generate_tts():
    """
    Endpoint to generate Text-to-Speech (TTS) audio for a story.
    Expected input: JSON with 'text' and 'id'.
    """
    data = request.get_json()
    text = data.get('text')
    story_id = data.get('id')  # Story ID is required
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    # Generate a unique story ID if not provided
    if not story_id:
        story_id = f"story_{int(time.time())}_{random.randint(1000, 9999)}"
        print(f"Generated unique story ID for audio: {story_id}")

    try:
        # Create a folder for the current story ID using the same structure as generate_story
        audio_dir = f"D:/Ahh/Projects/story/backend/static/stories/{story_id}"
        os.makedirs(audio_dir, exist_ok=True)
        
        print(f"Generating audio for story ID: {story_id}")
        print(f"Audio directory: {audio_dir}")

        # Generate TTS audio using gTTS
        tts = gTTS(text)
        audio_path = os.path.join(audio_dir, "story_audio.mp3")
        tts.save(audio_path)

        print(f"Audio generated at: {audio_path}")

        # Return the audio file URL with the updated path structure
        audio_url = f"/static/stories/{story_id}/story_audio.mp3"
        return jsonify({"audio_url": audio_url, "id": story_id})
    except Exception as e:
        print(f"Error generating TTS: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate TTS: {str(e)}"}), 500
  
@routes.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    """
    Endpoint to generate interactive quiz questions for a story.
    Expected input: JSON with 'content', 'moral', and 'description'.
    """
    data = request.get_json()
    content = data.get('content')
    moral = data.get('moral')
    description = data.get('description')

    if not all([content, moral, description]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Extract keywords and generate questions
        keywords = random.sample(content.split(), min(5, len(content.split())))
        main_character = description.split()[0]  # Assume first word of description is the main character

        questions = [
            {
                "question": f"What is the moral of the story?",
                "options": [moral, "Always tell lies", "Never help others"],
                "answer": moral
            },
            {
                "question": f"What does '{keywords[0]}' mean?",
                "options": ["Meaning 1", "Meaning 2", "Meaning 3"],
                "answer": "Meaning 1"
            },
            {
                "question": f"Who is the main character in the story?",
                "options": [main_character, "Harry", "John"],
                "answer": main_character
            }
        ]

        return jsonify({"questions": questions})
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return jsonify({"error": "Failed to generate quiz"}), 500
    
@routes.route('/static/generated_images/<path:filename>')
def serve_generated_image(filename):
    return send_from_directory(
        'static/generated_images', 
        filename,
        mimetype='image/png'
    )
