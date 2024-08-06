from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

import services.aisl_demo as aisl_demo_services
from schemas.request import RequestFeaturesSchmea

class AISLController:
  async def get_demo_input_video() -> FileResponse:
    file_path = await aisl_demo_services.get_demo_input_video()
    return FileResponse(file_path)

  async def generate_sign_language_to_text(file: UploadFile) -> dict[str, str]:
    # DEMO
    if file.filename == "aisl-demo-input.mp4":
      captions = await aisl_demo_services.generate_sign_language_to_text_demo(video=file)
      return { "captions": captions }
    else:
      raise HTTPException(500, "Server error. Please try again later. Please use the demo video input if you would like to AiSL in action.")
  
  async def generate_video(
    file: UploadFile,
    captions: str,
    features: RequestFeaturesSchmea
  ) -> FileResponse: 
    # DEMO
    if file.filename == "aisl-demo-input.mp4":
      edited_video_file_path = await aisl_demo_services.generate_video_demo(speech=features.sign_to_speech.selected, emoji=features.sign_to_emoji.selected)
      return FileResponse(edited_video_file_path)
    else:
      raise HTTPException(500, "Server error. Please try again later. Please use the demo video input if you would like to AiSL in action.")