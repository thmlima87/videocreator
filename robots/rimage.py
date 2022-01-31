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




def fetch_images_links(query, qtde=5, searchType='image', imgSize='XLARGE', start=1):
    
    my_api_key = credentials['gcs_api_key']
    my_cse_id = credentials["gcs_search_engine_id"]

    def google_search_images(query, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
        if 'items' in res:
            result = [d['link'] for d in res['items']]
        else:
            result = []
        
        return result

    results = google_search_images(query, my_api_key, my_cse_id, num=qtde, searchType=searchType, imgSize=imgSize)
    return results


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
    #os.chdir('./')
    #path = "./content/images"
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
                # if an image dosen't downloaded, try another one
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




def download_wikipedia_images():
    logging.info("Downloading images from Wikipedia")

    os.chdir('./')
    path = "./content/images"    
    # create directory
    os.makedirs(path, exist_ok=True)
    
    video_content = rcontent.load()

    print("Baixando imagens...", end="\n\n")

    # create data struct
    list_dict_img = []
        
    for img in video_content['wikipedia_images']:
        dict_img = {}
        dict_img['title'] = img['title']
        dict_img['type'] = img['type']
        # creating caption key if exists
        if 'caption' in img:
            dict_img['caption'] = img['caption']['text']
        dict_img['srcset'] = img['srcset']
        
        list_dict_img.append(dict_img)
        # removing duplicates
        list_img = []

        for idx, src in enumerate(img['srcset']):
            i = urllib.parse.unquote('https:{}'.format(src['src']))
            filename = "{}_original".format(idx)
            try:
                if src['src'] not in list_img:
                    image_filename = wget.download(i, "{}/{}".format(path, filename))
                    #image_filename = wget.download(i)
                    list_img.append(i)
            except:
                continue
            
    # saving metadata of images
    image_json_file = open('{}images.json'.format(path), 'w')
    json.dump(list_dict_img, image_json_file,  indent=4)
    image_json_file.close()

    return "Download concluído!!!"



def start():
    logging.info("Starting robot image...")
    fetch_images_from_sentences()
    download_images()



# em caso de execução do arquivo diretamente
if __name__ == '__main__':
    start()