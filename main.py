from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import logging
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.INFO)


# Authenticate in Google Drive
def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)


drive = authenticate_google_drive()


# Download file to Google Drive
def upload_file_to_drive(file_path, file_name):
    file_drive = drive.CreateFile({'title': file_name})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()


# Upload file from Google Drive
def download_file_from_drive(file_name, save_path):
    file_list = drive.ListFile({'q': f"title='{file_name}' and trashed=false"}).GetList()
    if len(file_list) == 0:
        raise HTTPException(status_code=404, detail="File not found")
    else:
        file_list[0].GetContentFile(save_path)


# Create folder on Google Drive
def create_folder_on_drive(folder_name):
    print(f"{folder_name}", "****************", "-------------------")
    folder_drive = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
    folder_drive.Upload()


# Delete file or folder on Google Drive
def delete_file_or_folder_from_drive(file_name):
    file_list = drive.ListFile({'q': f"title='{file_name}' and trashed=false"}).GetList()
    if len(file_list) == 0:
        raise HTTPException(status_code=404, detail="File not found")
    else:
        file_list[0].Trash()


# Move file or folder into Google Drive
def moving_file_or_folder(file_name, new_parent_id):
    file_list = drive.ListFile({'q': f"title='{file_name}' and trashed=false"}).GetList()
    if len(file_list) == 0:
        raise HTTPException(status_code=404, detail="File not found")
    else:
        file_list[0].SetContentFile({'id': new_parent_id})
        file_list[0].Upload(param={'supportsTeamDrives': True})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page with forms for work with Google Drive."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Uploading file to Google Drive."""
    logging.info(f"File uploaded: {file.filename}")
    with open(f"{file.filename}", "wb") as temp_file:
        temp_file.write(file.file.read())
    upload_file_to_drive(file.filename, file.filename)
    # os.remove(temp_file)
    return {"message": "File uploaded successfully"}


@app.get("/download/")
async def download_file(file_name: str):
    """Download file from Google Drive."""
    if not os.path.exists("./downloads/"):
        os.makedirs("./downloads/")
    save_path = f"./downloads/{file_name}"
    download_file_from_drive(file_name, save_path)
    return {"message": f"File {file_name} downloaded successfully"}


@app.post("/create_folder/")
async def create_folder(folder_name: str):
    """Create folder on Google Drive."""
    print(f"{folder_name=}", "************************")
    logging.info(f"Folder created: {folder_name}")
    create_folder_on_drive(folder_name)
    return {"message": f"Folder {folder_name} created successfully"}


@app.post("/delete/")
async def delete_file_or_folder(file_name: str):
    """Delete folder or file Google Drive."""
    logging.info(f"File or folder deleted: {file_name}")
    delete_file_or_folder_from_drive(file_name)
    return {"message": f"File or folder {file_name} deleted successfully"}


@app.post("/move/")
async def move_file_or_folder(file_name: str, new_parent_id: str):
    """Moving file or folder on Google Drive."""
    logging.info(f"File or folder moved: {file_name} to {new_parent_id}")
    moving_file_or_folder(file_name, new_parent_id)
    return {"message": f"File or folder {file_name} moved successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
