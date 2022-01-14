import datetime
from Google import *
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'credentials/client_secrets.json'
API_NAME = 'YOUTUBE'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

upload_date_time = datetime.datetime(2022, 1, 11, 20, 00, 0).isoformat() + '.000Z'

request_body = {
    'snippet':{
        'categoryId': 19,
        'title': 'Upload Testing',
        'description': 'First automatic upload video on youtube via python',
        'tags': ['Travel', 'video test']
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False,
    },
    'notifySubscribers': False
}


media_file = MediaFileUpload('./content/video_sentences.avi')

response_upload = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=media_file
).execute()

service.thumbnails().set(
    videoId=response_upload.get('id'),
    media_body=MediaFileUpload('./content/default/bg_default_new.jpeg')
).execute()