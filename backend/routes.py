# D:\Ahh\Projects\story\backend\routes.py

from flask import Blueprint, jsonify, request
from flask import send_from_directory
from flask import send_file
from gtts import gTTS
import os
import random
import time
import json
import requests

from utils.story_generator import generate_story
from utils.image_generator import generate_image
from utils.storage_manager import StoryAssetsManager

assets_manager=StoryAssetsManager()

from utils.instagram import InstagramGenerator
from dotenv import load_dotenv

load_dotenv()

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
    data = request.get_json()
    description = data.get('description')
    story_type = data.get('storyType', 'Bedtime')
    moral = data.get('moral')
    
    if not description:
        return jsonify({"error": "Description is required"}), 400

    try:
        # Generate story content
        story_content = generate_story(description, story_type, moral)
        story_id = data.get('id') or f"story_{int(time.time())}_{random.randint(1000, 9999)}"
        sentences = [s.strip() for s in story_content.split(". ") if s.strip()]
        
        generated_pages = []
        illustration_urls = []

        for i, sentence in enumerate(sentences):
            try:
                # Generate image with conflict handling
                image_url = assets_manager.save_image(
                    story_id=story_id,
                    image_url=f"https://image.pollinations.ai/prompt/{sentence}"
                )
                generated_pages.append({"image": image_url, "text": sentence})
                illustration_urls.append(image_url)
                
            except Exception as e:
                print(f"Error generating image for page {i+1}: {e}")
                generated_pages.append({"image": "/static/placeholder.png", "text": sentence})
                illustration_urls.append("/static/placeholder.png")

        return jsonify({
            "id": story_id,
            "title": f"{story_type} Story: {description.split()[0]}",
            "content": story_content,
            "illustration_urls": illustration_urls,
            "pages": generated_pages
        })

    except Exception as e:
        print(f"Error generating story: {str(e)}")
        return jsonify({"error": f"Failed to generate story: {str(e)}"}), 500


@routes.route('/save_story', methods=['POST'])
def save_story():
    data = request.get_json()
    required_fields = ['user_id', 'title', 'description', 'content', 'id']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO stories 
            (user_id, title, description, moral, content, 
            illustration_urls, story_id, audio_url, pages)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['user_id'],
            data['title'],
            data['description'],
            data.get('moral', ''),  # Add moral here
            data['content'],
            ",".join(data.get('illustrations', [])),
            data.get('id'),
            data.get('audio_url', ''),
            json.dumps(data.get('pages', []))
        ))
        
        conn.commit()
        return jsonify({
            "message": "Story saved successfully!",
            "id": cursor.lastrowid,
            "story_id": data['id']
        })
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
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
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, description, content, 
               illustration_urls, pages
        FROM stories 
        WHERE id=?
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
        "illustration_urls": story[4].split(",") if story[4] else [],
        "pages": json.loads(story[5]) if story[5] else []  # Deserialize pages
    })


@routes.route('/generate_tts', methods=['POST'])
def generate_tts():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        audio_url = assets_manager.save_audio_global(tts_text=text)
        return jsonify({"audio_url": audio_url})
    except Exception as e:
        print(f"Error generating TTS: {str(e)}")
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
    

@routes.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename)

@routes.route('/generated_audio/<path:filename>')
def serve_generated_audio(filename):
    return send_from_directory("generated_audio", filename)

@routes.route('/generate-instagram', methods=['POST'])
def generate_instagram_post():
    data = request.get_json()
    user_text = data.get('text')
    if not user_text:
        return jsonify({"error": "Text input is required"}), 400

    try:
        generator = InstagramGenerator()
        post_data = generator.create_instagram_post(user_text)
        return jsonify(post_data)
    except Exception as e:
        print(f"Error generating Instagram post: {str(e)}")
        return jsonify({"error": f"Post generation failed: {str(e)}"}), 500