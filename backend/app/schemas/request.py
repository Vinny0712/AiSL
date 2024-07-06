from pydantic import BaseModel

class _SignToSpeechSchema(BaseModel):
  selected: bool

class _SignToEmojiSchema(BaseModel):
  selected: bool

class RequestFeaturesSchmea(BaseModel):
  sign_to_speech: _SignToSpeechSchema
  sign_to_emoji: _SignToEmojiSchema