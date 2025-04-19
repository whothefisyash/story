import os
import google.generativeai as genai
import json
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def clean_gemini_json_response(response_text: str) -> str:
    """
    Removes triple backticks and optional 'json' from Gemini's markdown code block.
    """
    cleaned = response_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)  # Fixed regex
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned

def generate_quiz_from_story(story_text: str) -> list:
    """
    Generate 5 MCQs from a story using Gemini 1.5 Pro.
    Returns a list of dicts with 'question', 'options', and 'answer'.
    """
    prompt = (
        "Generate 5 multiple choice quiz questions based on the following story. "
        "For each question, provide:\n"
        "- question: the question text\n"
        "- options: an array of 4 options (one correct, three incorrect)\n"
        "- answer: the correct answer\n\n"
        "Return only valid JSON, no markdown or code block formatting. "
        'Format: [{"question": "...", "options": ["...", "...", "...", "..."], "answer": "..."}]\n\n'
        f"Story:\n{story_text}"
    )

    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    cleaned = clean_gemini_json_response(response.text)

    try:
        quiz = json.loads(cleaned)
        # Validate structure
        if isinstance(quiz, list) and all(
            isinstance(q, dict) and
            'question' in q and 'options' in q and 'answer' in q
            for q in quiz
        ):
            return quiz
    except Exception as e:
        print("Error parsing JSON:", e)

    return []
