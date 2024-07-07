from typing import Annotated
from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import FileResponse

from controllers.aisl import AISLController
from schemas.request import RequestFeaturesSchmea
from schemas.response import UploadVideoResponseSchema

import json

router = APIRouter()

tags_metadata = [
    {
        "name": "AiSL",
        "description": "API Endpoints for AiSL"
    },
]

@router.post("/upload", tags=["AiSL"], response_model=UploadVideoResponseSchema)
async def upload_video(file: UploadFile) -> dict[str, str]:
    """Reference: https://fastapi.tiangolo.com/tutorial/request-files/"""
    print(file.filename)
    print(file.file)
    return await AISLController.generate_sign_language_to_text(file=file)

@router.post("/generate", tags=["AiSL"])
async def generate_video(file: UploadFile, captions: Annotated[str, Form()], features: Annotated[str, Form()]) -> FileResponse:
    """Reference: https://fastapi.tiangolo.com/tutorial/request-forms/"""
    # Parse `features` json
    features_json = json.loads(features)
    features: RequestFeaturesSchmea =  RequestFeaturesSchmea(
        sign_to_emoji=features_json["sign_to_emoji"],
        sign_to_speech=features_json["sign_to_speech"]
    )
    
    print(file.filename)
    print(captions)
    print(features)
    
    return await AISLController.generate_video(
        file=file,
        captions=captions,
        features=features
    )

@router.get("/get_demo_video_input", tags=["AiSL"], response_model=UploadVideoResponseSchema)
async def get_demo_video_input() -> FileResponse:
    return await AISLController.get_demo_input_video()