from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

import services.aisl as aisl_services
from schemas.request import RequestFeaturesSchmea

class AISLController:
  async def generate_sign_language_to_text(file: UploadFile) -> dict[str, str]:
    captions = await aisl_services.generate_sign_language_to_text(video=file)
    if not captions:
      raise HTTPException(500, "Failed to generate captions from sign language!")
    return { "captions": captions }
  
  async def generate_video(
    file: UploadFile,
    captions: str,
    features: RequestFeaturesSchmea
  ) -> FileResponse: 
    speech_audio, emoji_captions = None, None

    # Text to Speech Feature
    if features.sign_to_speech:
      speech_audio = await aisl_services.generate_text_to_speech(captions=captions)
      if not speech_audio:
        raise HTTPException(500, "Failed to generate speech from captions!")
  
    # Text to Emoji Feature
    if features.sign_to_emoji:
      emoji_captions = await aisl_services.generate_text_to_emoji(captions=captions)
      if not emoji_captions:
        raise HTTPException(500, "Failed to generate emojis from captions!")
      captions = emoji_captions # Overwrite the original captions with the emoji version
  
    # Generate Video
    edited_video_file_path = await aisl_services.generate_final_video(
      video=file,
      captions=captions,
      speech_audio=speech_audio
    )
    if not edited_video_file_path:
      raise HTTPException(500, "Failed to generate video!")

    return FileResponse(edited_video_file_path)