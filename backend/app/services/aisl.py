from fastapi import UploadFile
from utils.file_handler import save_file_to_local, retrieve_full_file_path_from_local
from langchain_google_genai import ChatGoogleGenerativeAI
from rag.vector_db import VectorDB

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
    print(result.content)

    return result.content

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
