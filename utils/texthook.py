import cv2
from PIL import Image
import os, sys
import json
import base64
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from tqdm import tqdm

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
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": '''#ROLE
You are an expert with years of experience creating high-performing Instagram Reels.

#TASK
Your goal is to extract only the text hook from these frames of an Instagram Reel 
without any additional formatting, explanation, or structure. The hook should be 1-2 sentences 
and must be engaging enough to capture attention and keep viewers watching.

#STEPS
##STEP_1
Extract all visible text from both images and store it in 'full_text'.
- If the text is **split across multiple frames** (e.g., different words appearing on different images), **combine them into a single logical sentence**.  
- Preserve the **natural reading order** of the text as it would appear if read sequentially from the images.  
- Ensure that **the final extracted text forms a grammatically correct, meaningful sentence**.

##STEP_2
Extract the **first complete sentence** from 'full_text' as the Instagram hook.
- The **first sentence** is the one that appears first in logical reading order.  
- If words are split across frames, make sure to **combine them into a complete sentence** instead of taking partial fragments.  
- **Do not cut off sentences** mid-way. If a sentence starts but does not finish, always extract the full sentence.
- Ignore repetitive or generic phrases that appear later in the text if the first sentence is meaningful.

#EXAMPLES
✅ **Correct behavior:**
"full_text": "ПОСМОТРИ ЭТИ 6 ЛЕКЦИИ КОТОРЫЕ НАУЧАТ ВАС",
"text_hook": "ПОСМОТРИ ЭТИ 6 ЛЕКЦИИ КОТОРЫЕ НАУЧАТ ВАС"

✅ **Correct behavior (text split across multiple frames):**
Image 1: "Как увеличить"
Image 2: "доход в 2 раза?"
"full_text": "Как увеличить доход в 2 раза? Вот я вошел в свой офис",
"text_hook": "Как увеличить доход в 2 раза?"

✅ **Correct behavior (text scattered across multiple images but forms one idea):**
Image 1: "Лучшая стратегия"
Image 2: "для роста бизнеса"
"full_text": "Лучшая стратегия для роста бизнеса. Я сейчас вам такое покажу",
"text_hook": "Лучшая стратегия для роста бизнеса"

❌ **Incorrect behavior (Don't cutting off the sentence):**
"full_text": "ПОСМОТРИ ЭТИ 6 ЛЕКЦИИ КОТОРЫЕ НАУЧАТ ВАС",
"text_hook": "ПОСМОТРИ ЭТИ 6 ЛЕКЦИИ"

✅ **Correct behavior:**
"full_text": "ПОСМОТРИ ЭТИ 6 ЛЕКЦИИ КОТОРЫЕ НАУЧАТ ВАС",
"text_hook": "ПОСМОТРИ ЭТИ 6 ЛЕКЦИИ КОТОРЫЕ НАУЧАТ ВАС"

❌ **Incorrect behavior (Don't cutting off the sentence):**
"full_text": "АМЕРИКАНЦЫ НЕ СНИМАЮТ СТОРИС НЕ ДЕЛАЮТ ЗАПУСКИ",
"text_hook": "АМЕРИКАНЦЫ НЕ СНИМАЮТ СТОРИС"

✅ **Correct behavior:**
"full_text": "АМЕРИКАНЦЫ НЕ СНИМАЮТ СТОРИС НЕ ДЕЛАЮТ ЗАПУСКИ",
"text_hook": "АМЕРИКАНЦЫ НЕ СНИМАЮТ СТОРИС НЕ ДЕЛАЮТ ЗАПУСКИ"

#CONTEXT
- Do NOT modify or rewrite the text—simply extract it as-is.
- The hook is typically positioned in the center or top of the image.
- If a sentence is split across multiple frames, **reconstruct it properly** to preserve its full meaning.
- Ensure that the extracted text is not subtitles from the video’s voiceover. Subtitles are positioned at the bottom of the image.

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

# List of video paths
video_paths = [
    'texthook_folder/folder/test1.mp4',
    'texthook_folder/folder/test2.mp4',
    'texthook_folder/folder/test3.mp4',
    'texthook_folder/folder/test4.mp4',
    'texthook_folder/folder/test5.mp4',
    'texthook_folder/folder/test6.mp4',
    'texthook_folder/folder/test7.mp4'
]

video_paths2 = [
    'texthook_folder/test1.mp4',
    'texthook_folder/test2.mp4',
    'texthook_folder/test3.mp4',
    'texthook_folder/test4.mp4',
    'texthook_folder/test5.mp4',
    'texthook_folder/test6.mp4',
    'texthook_folder/test7.mp4',
    'texthook_folder/test8.mp4',
    'texthook_folder/test9.mp4',
    'texthook_folder/test10.mp4',
    'texthook_folder/test11.mp4',
    'texthook_folder/test12.mp4',
    'texthook_folder/test13.mp4',
    'texthook_folder/test14.mp4'
]

# Initialize a list to store the results
results = []

# Process each video with progress bar
for video_path in tqdm(video_paths, desc="Processing videos"):
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    # Frame counter
    frame_count = 0

    # Initialize a dictionary to store the results for all frames
    result = {'video_path': video_path}

    # Process specific frames: 5, 25
    frame_numbers = {5, 25, 50, 75, 100}
    frame_paths = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count in frame_numbers:
            # Calculate crop dimensions
            height, width = frame.shape[:2]
            top_crop = int(height * 0.0781)
            bottom_crop = int(height * 0.1875)

            # Crop the frame
            cropped_frame = frame[top_crop:height-bottom_crop, :]

            # Calculate new dimensions for resizing
            new_height = 512
            aspect_ratio = cropped_frame.shape[1] / cropped_frame.shape[0]
            new_width = int(new_height * aspect_ratio)

            # Resize the cropped frame
            resized_frame = cv2.resize(cropped_frame, (new_width, new_height))

            # Save the processed frame
            frame_path = f'texthook/frame_{frame_count}.png'
            cv2.imwrite(frame_path, resized_frame)
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