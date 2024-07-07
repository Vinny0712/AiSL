from fastapi import UploadFile
from utils.file_handler import demo_directory

import os
import time

async def get_demo_input_video() -> str:
  time.sleep(5)
  file_path = os.path.join(demo_directory, "aisl-demo-input.mp4")
  return file_path

async def generate_sign_language_to_text_demo(video: UploadFile) -> str:
  processed_cleaned_captions_json = '{"00:00:00": "I", "00:00:01-00:00:02": "eat", "00:00:03-00:00:04": "apple","00:00:05":"before","00:00:06":"bed"}'
  return processed_cleaned_captions_json

async def generate_video_demo(speech: bool, emoji: bool) -> str:
  time.sleep(10)
  file_name = ""
  if speech and emoji:
    file_name = "aisl-demo-output-captions-speech-emoji.mp4"
  elif speech:
    file_name = "aisl-demo-output-captions-speech.mp4"
  elif emoji:
    file_name = "aisl-demo-output-captions-emoji.mp4"
  else:
    file_name = "aisl-demo-output-captions.mp4"
  
  file_path = os.path.join(demo_directory, file_name)
  return file_path