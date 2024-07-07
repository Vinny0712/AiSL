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


async def generate_sign_language_to_text(video: UploadFile) -> str:
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
    except:
        print("Failed to import mediapipe")
        raise HTTPException(500, "Server error. Please try again later. Please use the demo video input if you would like to AiSL in action.")
    full_file_path = save_file_to_local(video=video)

    #set up model
    base_options = python.BaseOptions(model_asset_path='gesture_recognizer_9.task')
    options = vision.GestureRecognizerOptions(base_options=base_options)
    recognizer = vision.GestureRecognizer.create_from_options(options)

    # Create a VideoCapture object
    cap = cv2.VideoCapture(full_file_path)

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
        if len(results.gestures)>0:
            top_gesture = results.gestures[0][0]
            
            timestamp_time = str(datetime.timedelta(milliseconds=timestamp))
            if top_gesture.category_name:
                captions[timestamp_time]=top_gesture.category_name
                print("detected",top_gesture.category_name)
        
        

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
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
    # Passing the text and language to the engine, here we have marked slow=False. Which tells 
    # the module that the converted audio should have a high speed
    gTTsObject = gTTS(text=captions, lang='en', slow=False)

    # Saving the converted audio in a mp3 file named
    file_name = str(uuid.uuid4())
    file_path = save_audio_to_local(gTTsObject, f"{file_name}.mp3")

    return file_path

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

    # Format Prompt
    def _get_formatted_input(messages, context):
        system = "System: You are a fun emoji translator that translates words in sentences to emojis where appropriate. The assistant gives a sentence that contains both emoji and words to the user's input based on the context and your understanding of emojis, making a one-to-one substitution of a word or phrase of words. You may use emojis not in the provided context. If no words can be translated to emojis, return the original sentence."
        instruction = ""

        for item in messages:
            if item['role'] == "user":
                ## only apply this instruction for the first user turn
                item['content'] = instruction + " " + item['content']
                break

        conversation = '\n\n'.join(["User: " + item["content"] if item["role"] == "user" else "Assistant: " + item["content"] for item in messages]) + "\n\nAssistant:"
        formatted_input = system + "\n\n" + context + "\n\n" + conversation
        
        return formatted_input

    messages = [
        {"role": "user", "content": captions}
    ]

    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(_get_formatted_input(messages, context))

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
                # Get the text size
                font = cv2.FONT_HERSHEY_PLAIN
                font_scale = 2
                thickness = 2
                text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                text_width, text_height = text_size

                # Calculate the position to center the text at the bottom
                x = (frame_width - text_width) // 2
                y = frame_height - 30  # 30 pixels from the bottom
                cv2.putText(frame, text, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
                out.write(frame)
                print("written",text)
    cap.release()
    out.release()
    print(f"completed writing to {output_path}")

    if speech_audio_file_path:
        # TODO: Add Audio to video
        pass

    # Return generated video file path
    generated_video_file_path = output_path

    return retrieve_full_file_path_from_local(generated_video_file_path)
