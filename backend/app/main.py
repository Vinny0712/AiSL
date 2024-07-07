from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import aisl

load_dotenv()

app = FastAPI()

# CORS
origins = [
  "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aisl.router)

# @app.get("/")
# def read_root():
#     return {"API Docs": "http://127.0.0.1:8000/docs#/"}
from services.aisl import generate_text_to_speech

@app.get("/")
async def read_root():
    await generate_text_to_speech("Hi! My Name is Alex and I like to eat apples!")
    return {"API Docs": "http://127.0.0.1:8000/docs#/"}