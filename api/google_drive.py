import os
import logging

from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.google_drive import (
    upload_file_to_drive,
    download_file_from_drive,
    create_folder_on_drive,
    delete_file_or_folder_from_drive,
    moving_file_or_folder
)


router = APIRouter(tags=["Google Drive"])
logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page with forms for work with Google Drive."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Uploading file to Google Drive."""
    logging.info(f"File uploaded: {file.filename}")
    with open(f"{file.filename}", "wb") as temp_file:
        temp_file.write(file.file.read())
    upload_file_to_drive(file.filename, file.filename)
    # os.remove(temp_file)
    logging.info("File uploaded successfully")
    return RedirectResponse("/", status_code=302)


@router.get("/download/")
async def download_file(file_name: str):
    """Download file from Google Drive."""
    if not os.path.exists("./downloads/"):
        os.makedirs("./downloads/")
    save_path = f"./downloads/{file_name}"
    download_file_from_drive(file_name, save_path)
    logging.info(f"File {file_name} downloaded successfully")
    return RedirectResponse("/", status_code=302)


@router.post("/create_folder/")
async def create_folder(folder_name: str):
    """Create folder on Google Drive."""
    logging.info(f"Folder created: {folder_name}")
    create_folder_on_drive(folder_name)
    logging.info(f"Folder {folder_name} created successfully")
    return RedirectResponse("/", status_code=302)


@router.post("/delete/")
async def delete_file_or_folder(file_name: str):
    """Delete folder or file Google Drive."""
    logging.info(f"File or folder deleted: {file_name}")
    delete_file_or_folder_from_drive(file_name)
    logging.info(f"File or folder {file_name} deleted successfully")
    return RedirectResponse("/", status_code=302)


@router.post("/move/")
async def move_file_or_folder(file_name: str, new_parent_id: str):
    """Moving file or folder on Google Drive."""
    logging.info(f"File or folder moved: {file_name} to {new_parent_id}")
    moving_file_or_folder(file_name, new_parent_id)
    logging.info(f"File or folder {file_name} moved successfully")
    return RedirectResponse("/", status_code=302)
