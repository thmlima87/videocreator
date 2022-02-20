import sys
import os
from rconfig import CONTENT_PATH, CONTENT_IMAGES_PATH, CREDENTIALS_PATH
# adding robots to the system path
sys.path.insert(0, './')
import json
import rcontent # robot content
from googleapiclient.discovery import build
import util
import pprint
import logging
import wget
import urllib
import requests
import time

# buscando credenciais
credentials = util.getCredentials()


# implementando busca de imagens pelo Bing
def search_images_on_bing(query, count="1"):
    logging.info("Searching images on Bing with custom bing image search")

    url = credentials['bing_endpoint'] + "?q=" + query + "&count="+ count +"&customconfig=" + credentials['bing_custom_config_id'] +"&licence=ShareCommercially&size=Large"
    r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': credentials['azure_subscription_key']})
    response = json.loads(r.text)
    if 'value' in response:
        result = [d['contentUrl'] for d in response['value']]
    else:
        result = []
    
    return result

def fetch_images_from_sentences():
    logging.info("Fetching images from sentences...")
    print("Fetching images from sentences", end='\n\n')
    # loading content
    logging.info("Get sentences from object saved")
    print("Loading content from content.json")
    video_content = rcontent.load()
    for sentence in video_content['sentences']:
        if len(sentence['keywords'])>0:
            if video_content['search_term'] != sentence['keywords'][0]:
                sentence['image_search_query'] = "{} {}".format(video_content['search_term'], sentence['keywords'][0])
                sentence['images'] = search_images_on_bing(sentence['image_search_query'], "5")
                time.sleep(1.5)
    rcontent.save(video_content)


def download_images():
    logging.info("Downloading images from each sentences")
    
    path = CONTENT_IMAGES_PATH

    # create directory
    os.makedirs(path, exist_ok=True)
    # limpando a pasta
    os.system("rm -rf {}/*".format(path))
    video_content = rcontent.load()

    list_img = []

    for idx_s, sentence in enumerate(video_content['sentences']):
        for idx_i, image in enumerate(sentence['images']):
            if image not in list_img:
                # if an image doesn't downloaded, try another one
                try:
                    print("Trying to download: ", image)
                    image_filename = "{}/{}_original.jpg".format(path,idx_s)
                    wget.download(image,image_filename)
                    list_img.append(image)
                    print("")
                    break
                except Exception as ex:
                    logging.error(ex)
                    continue
    
    video_content['images_used'] = list_img
    rcontent.save(video_content)


def start():
    logging.info("Starting robot image...")
    fetch_images_from_sentences()
    download_images()



# em caso de execução do arquivo diretamente
if __name__ == '__main__':
    start()