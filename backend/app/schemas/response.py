from pydantic import BaseModel

class UploadVideoResponseSchema(BaseModel):
  captions: str