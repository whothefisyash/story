import os
from image_generator import generate_image

# Define the absolute path for testing
image_path = 'D:/Ahh/Projects/story/backend/generated_images/page_1.png'

# Generate an image
generate_image("A magical forest with glowing lights", image_path)

# Check if the file exists
if os.path.exists(image_path):
    print(f"Image successfully saved at {image_path}")
else:
    print(f"Image not found at {image_path}")
