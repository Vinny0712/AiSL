from fastapi import UploadFile
from utils.file_handler import save_file_to_local, retrieve_full_file_path_from_local

async def generate_sign_language_to_text(video: UploadFile) -> str:
    full_file_path = save_file_to_local(video=video)

    # TODO: Sign Language to Text
    return "Sign Language to Text"

async def generate_text_to_speech(captions: str):
    """
    Returns an Audio File.
    """
    # TODO: Text to Speech
    return "Text to Speech"

async def generate_text_to_emoji(captions: str) -> str:
    """
    Returns the updated caption with emojis in `string` format"""
    # TODO: Text to Emoji
    return "Text to Emoji"

async def generate_final_video(video: UploadFile, captions: str, speech_audio: bytes | None):
    """
    Generates an edited video based on the input `captions` and `speech_audio`.

    Returns:
        Generated video file path in `string` format.
    """
    full_file_path = save_file_to_local(video=video)
    
    # TODO: Edit the Video

    if speech_audio:
        # TODO: Add Audio to video
        pass

    # TODO: Save Generated Video to local

    # TODO: Return generated video file path
    generated_video_file_path = full_file_path

    return retrieve_full_file_path_from_local(generated_video_file_path)
