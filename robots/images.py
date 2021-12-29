import sys
import os
# adding robots to the system path
sys.path.insert(0, './')
import json
import content # robot content
from googleapiclient.discovery import build
import util
import pprint
import logging

# buscando credenciais
credentials = util.getCredentials()

def fetch_images_links(query, qtde=2, searchType='image', imgSize='HUGE'):
    
    my_api_key = credentials['gcs_api_key']
    my_cse_id = credentials["gcs_search_engine_id"]

    def google_search_images(query, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
        return res['items']
        #return res

    results = google_search_images(query, my_api_key, my_cse_id, num=qtde, searchType=searchType, imgSize=imgSize)
    return [d['link'] for d in results]



def fetch_images_from_sentences():
    logging.info("Fetching images from sentences...")
    print("Fetching images from sentences", end='\n\n')
    # loading content
    logging.info("Get sentences from object saved")
    print("Loading content from content.json")
    for root, folders, files in os.walk('./content'):
        for f in files:
            if f == 'content.json':
                video_content = content.load(os.path.join(root, f))
                for sentence in video_content['sentences']:
                    if len(sentence['keywords'])>0:
                        if video_content['search_term'] != sentence['keywords'][0]:
                            sentence['google_search_query'] = "{} {}".format(video_content['search_term'], sentence['keywords'][0])
                            sentence['images'] = fetch_images_links(sentence['google_search_query'])
                content.save(video_content)




def start():
    fetch_images_from_sentences()




# Para execução sozinha
if len(sys.argv) > 1:
    if sys.argv[1] == 'start':
        start()

#fetch_images_from_sentences()
#print(images_links)
#print(content)