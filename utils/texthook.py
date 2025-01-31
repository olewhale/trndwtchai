import cv2
from PIL import Image
import os, sys
import json
import base64
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Create an OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class InstagramReelTextHook(BaseModel):
    full_text: str = Field(..., description="The complete text extracted from the images. Separate sentences")
    text_hook: str = Field(..., description="Copy 1-2 sentences from the 'full_text' which looks like a catchy hook in an Instagram video. it is forbidden to change them, just copy")

def recognition(frame_paths):
    images_base64 = []
    for frame_path in frame_paths:
        with open(frame_path, 'rb') as image_file:
            images_base64.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"}
            })

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": '''#ROLE
You are an expert with years of experience creating instagram reels.
#TASK
Your goal is to extract only the text hook from these frames of an Instagram reel 
without additional formatting, explanation, or structure. The text hook can be 1-2 sentences 
and should engage the audience so that they continue watching this reel video.
#STEPS
##STEP_1
Write all text found in the images to 'full_text'.
The two images must have the same text. If the text is different, 
use the text from the first image only!
##STEP_2
Copy 1-2 sentences from the 'full_text' which looks like a catchy hook in an Instagram.

#EXAMPLE
"full_text": "Stop ‘pretending’ your content is under control (when it really isn’t)\nHERE’S 5 EXAMPLES ON HOW TO ACTUALLY GET IT ORGANISED\nWhy automate when you can micromanage every little detail yourself?",
"text_hook": "Stop ‘pretending’ your content is under control (when it really isn’t). Here’s 5 examples on how to actually get it organised!"

#CONTEXT
- It is forbidden to change text, just copy!

'''
            },
            {
                "role": "user",
                "content": images_base64
            }
        ],
        temperature=0,
        max_tokens=15000,
        response_format=InstagramReelTextHook
    )

    return completion.choices[0].message.parsed

# Ensure 'texthook' directory exists
os.makedirs('texthook', exist_ok=True)

# Path to the video file
video_path = 'texthook/video6.mp4'

# Initialize video capture
cap = cv2.VideoCapture(video_path)

# Frame counter
frame_count = 0

# Initialize a list to store the results
results = []

# Initialize a dictionary to store the results for all frames
result = {'video_path': video_path}

# Process specific frames: 5, 25
frame_numbers = {5, 25}
frame_paths = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count in frame_numbers:
        frame_path = f'texthook/frame_{frame_count}.png'
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
    
    frame_count += 1

cap.release()

if frame_paths:
    extracted_text = recognition(frame_paths)

    print("------------------")
    print(json.dumps(extracted_text.dict(), indent=4, ensure_ascii=False))
    print("------------------")

    result['frames_paths'] = frame_paths
    result['full_text'] = extracted_text.full_text
    result['text_hook'] = extracted_text.text_hook

# Append the result to the list
results.append(result)

# Define the path for the JSON file
json_path = 'texthook/results.json'

# Load existing data if the JSON file exists
existing_data = []
if os.path.exists(json_path):
    with open(json_path, 'r') as f:
        existing_data = json.load(f)

# Append new results to existing data
existing_data.extend(results)

# Write the updated data back to the JSON file
with open(json_path, 'w') as f:
    json.dump(existing_data, f, indent=4)