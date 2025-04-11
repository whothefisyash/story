import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def generate_story(description, story_type="Bedtime", moral=None): 
    if not description or not description.strip():
        raise ValueError("Description cannot be empty")

    try:
        # Craft the prompt
        prompt = f"Write a {story_type} story based on this description: '{description}'."
        if moral:
            prompt += f" The story should teach this moral lesson: '{moral}'."
        
        # Add instructions for story format
        prompt += " The story should be appropriate for children, with one paragraph and simple language."

        print(f"Sending prompt to Gemini API: {prompt}")

        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Generate the story
        response = model.generate_content(prompt)
        story_content = response.text
        
        print("Successfully generated story using Gemini API")
        
        return story_content

    except Exception as e:
        print(f"Error generating story with Gemini API: {e}")
        raise e



# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
# import os

# # Local model path
# BASE_MODEL_PATH = "D:/Ahh/Projects/story/models/phi2-lora-merged"

# print("Loading tokenizer and model...")

# # Load model and tokenizer once
# tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

# model = AutoModelForCausalLM.from_pretrained(
#     BASE_MODEL_PATH,
#     torch_dtype=torch.float32,
#     device_map="auto"  # Will use GPU if available, else CPU
# )

# print("Model loaded successfully.")

# def generate_story(description, story_type="Bedtime", moral=None):
#     if story_type not in ["Bedtime", "Educational"]:
#         raise ValueError("Invalid story type. Choose either 'Bedtime' or 'Educational'.")

#     prompt = f"Write a {story_type} story based on this description: '{description}'."
#     if moral:
#         prompt += f" Include this moral: '{moral}'."

#     print("\nPrompt:", prompt)
#     print("Generating...")

#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=100,  # Reduced for faster generation
#             temperature=0.7,
#             top_p=0.9,
#             do_sample=True
#         )

#     print("Generation complete!")
#     return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
