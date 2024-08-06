from fastapi import UploadFile
from utils.file_handler import save_file_to_local, retrieve_full_file_path_from_local, save_audio_to_local,generate_captioned_video_filepath
from utils.caption_formatting import process_timestamps , clean_repeated_words
from langchain_google_genai import ChatGoogleGenerativeAI
from rag.vector_db import VectorDB
from gtts import gTTS # For text to speech conversion
import uuid
import cv2
import datetime
import json
from fastapi import HTTPException
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import moviepy.editor as mp_editor
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pydub import AudioSegment
import os
import librosa
import soundfile as sf

async def generate_sign_language_to_text(video: UploadFile) -> str:
    # try:
    #     import mediapipe as mp
    #     from mediapipe.tasks import python
    #     from mediapipe.tasks.python import vision
    # except:
    #     print("Failed to import mediapipe")
    #     raise HTTPException(500, "Server error. Please try again later. Please use the demo video input if you would like to AiSL in action.")
    print("save file...")
    full_file_path = save_file_to_local(video=video)

    #set up model
    print("load model...")
    base_options = python.BaseOptions(model_asset_path='services/gesture_recognizer_refined_23.task')
    print("load gesture recognizer options...")
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)
    print("opening capture...")

    # Create a VideoCapture object
    cap = cv2.VideoCapture(full_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    rate=1
    count=1

    captions={}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)

        # Convert the frame to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # Process the image and detect hands
        results = recognizer.recognize(mp_image)
        if len(results.gestures)>0 and (count%rate==0):
            top_gesture = results.gestures[0][0]
            
            timestamp_time = str(datetime.timedelta(milliseconds=timestamp))
            if top_gesture.category_name:
                captions[timestamp_time]=top_gesture.category_name
                print("detected",top_gesture.category_name)
        
        

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        count+=1
    cap.release()

    
    # format captions
    processed_captions = process_timestamps(captions)
    processed_cleaned_captions = clean_repeated_words(processed_captions)
    processed_cleaned_captions_json = json.dumps(processed_cleaned_captions)
    print("formatted_captions",processed_cleaned_captions_json)
    
    
    
    return str(processed_cleaned_captions_json)

async def generate_text_to_speech(captions: str) -> str:
    """
    Returns the full file path to the audio file.
    """

    file_name = str(uuid.uuid4())
    

    final_audio = AudioSegment.empty()
    processed_cleaned_captions = json.loads(captions)
    prev_end_total_seconds=0
    
    for timestamp_range,text in processed_cleaned_captions.items():
        

        #check if there are breaks of silence, and if so, add some silence
        if '-' in timestamp_range:
            start_time_str, end_time_str = timestamp_range.split('-')
            hours, minutes, seconds = map(int, start_time_str.split(':'))
            start_total_seconds = hours * 3600 + minutes * 60 + seconds
            hours, minutes, seconds = map(int, end_time_str.split(':'))
            end_total_seconds = hours * 3600 + minutes * 60 + seconds
        else:
            hours, minutes, seconds = map(int, timestamp_range.split(':'))
            start_total_seconds = hours * 3600 + minutes * 60 + seconds
            end_total_seconds = hours * 3600 + minutes * 60 + seconds

        silence_duration_seconds=start_total_seconds-prev_end_total_seconds

        if silence_duration_seconds>1:
            silence=AudioSegment.silent(duration=silence_duration_seconds*1000) #in ms
            final_audio+=silence
        if text:
            #add audio of text for this timestamp range    
            tts = gTTS(text)
            tts.save("temp.mp3")
            word_audio = AudioSegment.from_file("temp.mp3")
            final_audio += word_audio
        else:
            silence=AudioSegment.silent(duration=1000) #in ms
            final_audio+=silence


        prev_end_total_seconds=end_total_seconds

    file_path = save_audio_to_local(final_audio, f"{file_name}.mp3")

    
    # use librosa to match length of audio to video , speed up without chipmunk sound
    
    y, sr = librosa.load(file_path, sr=None)  # Load the audio with its original sample rate

    # Define the speed factor (e.g., 1.5 for 1.5x speed)
    speed_factor = final_audio.duration_seconds/prev_end_total_seconds

    # Apply time-stretching
    y_stretched = librosa.effects.time_stretch(y, rate=speed_factor)

    # Save the sped-up audio to a new file
    sf.write(file_path, y_stretched, sr)
    
        

    return file_path

    # Format Prompt
def _get_formatted_input(messages, context,system_msg):
    system = system_msg
    instruction = ""

    for item in messages:
        if item['role'] == "user":
            ## only apply this instruction for the first user turn
            item['content'] = instruction + " " + item['content']
            break

    conversation = '\n\n'.join(["User: " + item["content"] if item["role"] == "user" else "Assistant: " + item["content"] for item in messages]) + "\n\nAssistant:"
    formatted_input = system + "\n\n" + context + "\n\n" + conversation
    
    return formatted_input
async def generate_text_to_emoji(captions: str) -> str:
    """
        Returns the updated caption with emojis in `string` format

        @docs: https://huggingface.co/nvidia/Llama3-ChatQA-1.5-70B
    """
    # RAG
    db = VectorDB()
    documents = db.query(captions)

    # Context
    context = ""

    for document in documents:
        context += document.page_content + "\n"

    messages = [
        {"role": "user", "content": captions}
    ]
    system="System: You are a fun emoji translator that translates words in sentences to emojis where appropriate.The assistant gives a sentence that contains both emoji and words to the user's input based on the context and your understanding of emojis, making a one-to-one substitution of a word or phrase of words.You may use emojis not in the provided context. If no words can be translated to emojis, return the original sentence.Follow the same json structure provided.Strictly do not modify the timestamps"
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(_get_formatted_input(messages, context,system))

    return result.content

async def generate_final_video(video: UploadFile, captions: str, speech_audio_file_path: str):
    """
    Generates an edited video based on the input `captions` and `speech_audio`.

    Arguments:
        video: UploadFile
        captions: str
        speech_audio_file_path: str (Absolute file path)

    Returns:
        Generated video file path in `string` format.
    """
    
    # Edit the Video
    full_file_path = save_file_to_local(video=video)
    video_path = full_file_path
    output_path = generate_captioned_video_filepath(full_file_path)
    cap = cv2.VideoCapture(video_path)

    # Get the frame rate and frame size of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object   
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    frame_count=0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count+=1
        current_time = frame_count / fps
        timestamp_str = '0'+str(datetime.timedelta(seconds=int(current_time)))
        
        processed_cleaned_captions = json.loads(captions)


        if timestamp_str in processed_cleaned_captions.keys():
            
            text=processed_cleaned_captions[timestamp_str]
            

            # Convert the OpenCV image (BGR) to a Pillow image (RGB)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            
            #cv2 text does not support emojis
            # Draw text with emojis using Pillow
            draw = ImageDraw.Draw(pil_img)
            #load font which supports emoji eg seguiemj
            font = ImageFont.truetype('services/seguiemj.ttf',30,encoding='unic')
            # Calculate the width and height of the text to be drawn
            text_width = draw.textlength(text, font=font)

            # Calculate x, y position to center the text
            x = (frame_width - text_width) // 2
            y = frame_height - 50  # 50 pixels from the bottom

            # Draw the text on the image
            # White color, embedded color to true for colored emojis
            draw.text((x, y), text, font=font,embedded_color=True)  

            # Convert the Pillow image back to OpenCV format (BGR)
            frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)           
            out.write(frame)
            print("written",text)

    cap.release()
    out.release()
    new_file_name=output_path.split(".")[0]+'-edited'+'.mp4'
    #need to convert to h264 encoding to render on web
    command=f"ffmpeg -i {output_path} -vcodec libx264 {new_file_name}"
    
    os.system(command)
    print(f"completed writing to {new_file_name}")

    if speech_audio_file_path:
        # Add audio to the processed video
        video = mp_editor.VideoFileClip(new_file_name)
        audio = mp_editor.AudioFileClip(speech_audio_file_path)


        # # Combine video with audio
        final_video = video.set_audio(audio)
        with_audio_file_name=output_path.split(".")[0]+'-voice'+'.mp4'
        final_video.write_videofile(with_audio_file_name, codec="libx264", audio_codec="mp3")

    # Return generated video file path
    generated_video_file_path = new_file_name

    return retrieve_full_file_path_from_local(generated_video_file_path)
