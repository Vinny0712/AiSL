from fastapi import UploadFile
import os
import shutil

upload_directory = os.path.join(os.getcwd(), "uploads")

def save_file_to_local(video: UploadFile) -> str:
    """
    Saves File Locally.

    Returns:
        file_path: str
    """
    # Create upload directory if it does not exist
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    # Destination File Path
    file_path = os.path.join(upload_directory, video.filename)

    # Copy the file contents
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return file_path

def retrieve_full_file_path_from_local(relative_file_path: str):
    file_path = os.path.join(upload_directory, relative_file_path)
    return file_path