from fastapi import HTTPException

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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

# Get files list from the Google Drive
def files_list():
    try:
        file_list = drive.ListFile(
            {'q': "'root' in parents and trashed=false"}
        ).GetList()
        files_info = [
            {"name": file['title'], "id": file['id']} for file in file_list
        ]
        return files_info
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
