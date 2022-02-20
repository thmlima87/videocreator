#!/usr/bin/python

import httplib2
import os
import random
import time
import sys
sys.path.insert(0, './')
import logging
import rcontent
from rconfig import CONTENT_PATH, CONTENT_IMAGES_PATH, CREDENTIALS_PATH
# imports for youtube upload
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

##########################################################################################################
# Define some constants
##########################################################################################################

YOUTUBE_VIDEO_PRIVACY_STATUS = 'private'

YOUTUBE_VIDEO_THUMBNAILS = {
    "default": {
        "url": CONTENT_IMAGES_PATH + "/thumb_default.png",
        "width": 120,
        "height": 90
    },
    "medium": {
        "url": CONTENT_IMAGES_PATH + "/thumb_medium.png",
        "width": 320,
        "height": 180
    },
    "high": {
        "url": CONTENT_IMAGES_PATH + "/thumb_high.png",
        "width": 480,
        "height": 360
    },
    "standard": {
        "url": CONTENT_IMAGES_PATH + "/thumb_standard.png",
        "width": 640,
        "height": 480
    },
    "maxres": {
        "url": CONTENT_IMAGES_PATH + "/thumb_maxres.png",
        "width": 1280,
        "height": 720
    }
}

#print(YOUTUBE_VIDEO_THUMBNAILS)

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "{}/youtube_client_secrets.json".format(CREDENTIALS_PATH)

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),CLIENT_SECRETS_FILE))


VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage("{}/{}-oauth2.json".format(CREDENTIALS_PATH, sys.argv[0]))
    credentials = storage.get()
    
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))



def get_tags(video_content):
    keywords = []

    for sentence in video_content['sentences']:
        for k in sentence['keywords']:
            if k not in keywords:
                keywords.append(k)
    
    return keywords




def initialize_upload(youtube, video_content):
    list_of_used_images = '\n'.join('✅ ' + img for img in video_content['images_used'])
    list_of_sentences = '\n'.join([ s['text'] for s in video_content['sentences']])
    YOUTUBE_VIDEO_DESCRIPTION = """
Conheça um pouco mais sobre {}:

{}

👉 Referências:

💥 Wikipedia
💥 Custom Search API - Bing.

👉 Imagens utilizadas no vídeo:

{}
""".format(video_content['search_term'], list_of_sentences, list_of_used_images)

    YOUTUBE_VIDEO_FILE = CONTENT_PATH + '/{}'.format(video_content['video_filename'])
        
    body= {
        "snippet": {
            "title": video_content['youtube_details']['title'],
            "description": YOUTUBE_VIDEO_DESCRIPTION,
            "tags": get_tags(video_content),
            "categoryId": video_content['youtube_details']['category_id']
        },
        "status": {
            "privacyStatus": YOUTUBE_VIDEO_PRIVACY_STATUS
        }
    }
    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    # The chunksize parameter specifies the size of each chunk of data, in
    # bytes, that will be uploaded at a time. Set a higher value for
    # reliable connections as fewer chunks lead to faster uploads. Set a lower
    # value for better recovery on less reliable connections.
    #
    # Setting "chunksize" equal to -1 in the code below means that the entire
    # file will be uploaded in a single HTTP request. (If the upload fails,
    # it will still be retried where it left off.) This is usually a best
    # practice, but if you're using Python older than 2.6 or if you're
    # running on App Engine, you should set the chunksize to something like
    # 1024 * 1024 (1 megabyte).
    media_body=MediaFileUpload(YOUTUBE_VIDEO_FILE, chunksize=-1, resumable=True)
    )
    insert_response = resumable_upload(insert_request)
    # set thumbnail
    set_thumbnail(youtube, insert_response['id'])

    
# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print ("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print ("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print (error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)

    return response



def  create_thumbnail(video_content):
    logging.info("Creating Thumbnail...")

    # apagando as thumbs existentes
    os.system("rm -rf {}/thumb*".format(CONTENT_IMAGES_PATH))

    # criando os comandos para execução.
    # Importante: Refatorar para que a montagem do comando esteja dentro de um for

    command_thumb_default = "convert -size {}x{} -font helvetica -pointsize 24 -background 'black' -fill white -gravity center caption:'{}' ./content/images/thumb_default.png"\
        .format(YOUTUBE_VIDEO_THUMBNAILS['default']['width'],YOUTUBE_VIDEO_THUMBNAILS['default']['height'], video_content['youtube_details']['title'])
        
    command_thumb_medium = "convert -size {}x{} -font helvetica -pointsize 26 -background 'black' -fill white -gravity center caption:'{}' ./content/images/thumb_medium.png"\
        .format(YOUTUBE_VIDEO_THUMBNAILS['medium']['width'],YOUTUBE_VIDEO_THUMBNAILS['medium']['height'], video_content['youtube_details']['title'])

    command_thumb_high = "convert -size {}x{} -font helvetica -pointsize 30 -background 'black' -fill white -gravity center caption:'{}' ./content/images/thumb_high.png"\
        .format(YOUTUBE_VIDEO_THUMBNAILS['high']['width'],YOUTUBE_VIDEO_THUMBNAILS['high']['height'], video_content['youtube_details']['title'])
    
    command_thumb_standard = "convert -size {}x{} -font helvetica -pointsize 50 -background 'black' -fill white -gravity center caption:'{}' ./content/images/thumb_standard.png"\
        .format(YOUTUBE_VIDEO_THUMBNAILS['standard']['width'],YOUTUBE_VIDEO_THUMBNAILS['high']['height'], video_content['youtube_details']['title'])

    command_thumb_maxres = "convert -size {}x{} -font helvetica -pointsize 70 -background 'black' -fill white -gravity center caption:'{}' ./content/images/thumb_maxres.png"\
        .format(YOUTUBE_VIDEO_THUMBNAILS['maxres']['width'],YOUTUBE_VIDEO_THUMBNAILS['high']['height'], video_content['youtube_details']['title'])

    os.system(command_thumb_default)
    os.system(command_thumb_medium)
    os.system(command_thumb_high)
    os.system(command_thumb_standard)
    os.system(command_thumb_maxres)
    

def set_thumbnail(youtube, video_id):
    print('Setting the thumbnail: {} for video: {}'.format(CONTENT_IMAGES_PATH + "/thumb_maxres.png", video_id))
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=CONTENT_IMAGES_PATH + "/thumb_maxres.png"
    ).execute()


def start():
    logging.info('--- Starting Youtube robot ---')
    video_content = rcontent.load()
    youtube = get_authenticated_service()
    try:
        create_thumbnail(video_content)
        initialize_upload(youtube, video_content)
        result = "Upload concluído!"
    except HttpError as e:
            result = "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    except Exception as ex:
        result = ex
    print(result)

    



# em caso de execução do arquivo diretamente
if __name__ == '__main__':
    start()