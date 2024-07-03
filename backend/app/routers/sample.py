from fastapi import APIRouter

from controllers.sample import SampleController

router = APIRouter()

tags_metadata = [
    {
        "name": "Sample",
        "description": "API Endpoints for Sample"
    },
]

@router.post("/sample", tags=["Sample"])
def sample():
    return SampleController.sample()