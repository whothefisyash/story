# Test saving and retrieving a story
import requests

# Generate a story
gen_response = requests.post("http://localhost:5000/generate_story", json={
    "description": "Test story",
    "storyType": "Bedtime"
}).json()

# Save the story
save_response = requests.post("http://localhost:5000/save_story", json={
    "user_id": 1,
    "title": gen_response["title"],
    "description": "Test description",
    "content": gen_response["content"],
    "id": gen_response["id"],
    "illustrations": gen_response["illustration_urls"],
    "pages": gen_response["pages"]
}).json()

# Retrieve the saved story
retrieve_response = requests.get(f"http://localhost:5000/story/{save_response['id']}").json()
print(retrieve_response["pages"])  # Should show populated array
