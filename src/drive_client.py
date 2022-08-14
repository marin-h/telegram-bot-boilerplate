# api client for google cloud services
import google.auth
import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
CONFIG_FOLDER_ID = os.getenv('CONFIG_FOLDER_ID')
SCOPES = ['https://www.googleapis.com/auth/drive']

from google.oauth2 import service_account

def get_authorized_client():
    credentials = get_scoped_credentials()
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

def get_scoped_credentials():
    if GOOGLE_SERVICE_ACCOUNT_CREDENTIALS is not None:
        credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_CREDENTIALS)
        scoped_credentials = credentials.with_scopes(SCOPES)
    else:
        scoped_credentials, project = google.auth.default(scopes=SCOPES)
    return scoped_credentials

def upload_file(file_path, filename):
    print("Will upload {} to drive as {}".format(file_path, filename))
    service = get_authorized_client() 
    media = MediaFileUpload(file_path, mimetype='text/plain')
    file_metadata = {
        'name': filename, 
        'parents': [CONFIG_FOLDER_ID], 
        'mimeType': 'application/json'
    }
    file = service.files().create(body=file_metadata, media_body=media).execute()
    return file

def download_file(file_path, filename):
    service = get_authorized_client()

    if filename:
        query = "'{}' and '{}' in parents and name='{}'".format(filename, CONFIG_FOLDER_ID)
        print("search by filename filter: {}".format(query))
    else:
        query = "trashed=false and '{}' in parents".format(CONFIG_FOLDER_ID)
        print("search latest created_at: {}".format(query))
    
    results = service.files().list(
        q=query, orderBy="createdTime desc", 
        pageSize = 1000, fields = "nextPageToken, files(id, mimeType, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['mimeType']))
        
    file_metadata = items[0]
    file_id = file_metadata['id']
    print(file_metadata)

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d." % int(status.progress() * 100))
    return fh.getvalue().decode("utf-8") 