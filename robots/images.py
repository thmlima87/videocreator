import sys
# adding robots to the system path
sys.path.insert(0, './')
import json
import content
from googleapiclient.discovery import build
import util
import pprint

# buscando credenciais
credentials = util.getCredentials()

def fetch_images_links(query,qtde=10, searchType='image', imgSize='HUGE'):
    
    my_api_key = credentials['gcs_api_key']
    my_cse_id = credentials["gcs_search_engine_id"]

    def google_search_images(query, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
        return res['items']
        #return res

    results = google_search_images(query, my_api_key, my_cse_id, num=qtde, searchType=searchType, imgSize=imgSize)
    return [d['link'] for d in results]

images_links = fetch_images_links('Michael Jackson')
content = content.load()

print(images_links)
print(content)