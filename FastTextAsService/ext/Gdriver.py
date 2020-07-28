from __future__ import print_function
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


class Gdrive:

    def __init__(self, credential):

        self.service = build('drive', 'v3', credentials=credential)

    def GetIdFiles(self):
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def DwnldFileById(self, file_id: str, filename: str):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        return True

    def UpldFile(self, filename: str):
        file_metadata = {'name': filename}
        media = MediaFileUpload(filename)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()

        file_id = file.get('id')

        return file_id
