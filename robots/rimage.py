import sys
import os
# adding robots to the system path
sys.path.insert(0, './')
import json
import rcontent # robot content
from googleapiclient.discovery import build
import util
import pprint
import logging
import wget

# buscando credenciais
credentials = util.getCredentials()

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
                sentence['google_search_query'] = "{} {}".format(video_content['search_term'], sentence['keywords'][0])
                sentence['images'] = fetch_images_links(sentence['google_search_query'])
    rcontent.save(video_content)



def download_images():
    logging.info("Downloading images from each sentences")

    os.chdir('./')
    path = "./content/images"
    
    # create directory
    os.makedirs(path, exist_ok=True)
    video_content = rcontent.load()

    list_img = []

    for idx_s, sentence in enumerate(video_content['sentences']):
        for idx_i, image in enumerate(sentence['images']):
            if image not in list_img:
                #print("{}_{}_original.jpg".format(idx_s,idx_i))
                list_img.append(image)
                try:
                    image_filename = "{}/{}_{}_original.jpg".format(path,idx_s,idx_i)
                    wget.download(image,image_filename)
                except:
                    continue




def download_wikipedia_images(images, folder):
    logging.info("Downloading images from Wikipedia")
    print("Baixando imagens...", end="\n\n")
    # path
    path = "images/download/{}".format(folder)
    # create directory
    os.makedirs(os.path.dirname("{}/images.json".format(path)), exist_ok=True)

    # change directory
    os.chdir(path)
    # create data struct
    list_dict_img = []
        
    for img in images:
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

        for src in img['srcset']:
            i = urllib.parse.unquote('https:{}'.format(src['src']))
            try:
                if src['src'] not in list_img:
                    #image_filename = wget.download(i, path)
                   image_filename = wget.download(i) 
            except:
                continue
            
    # saving metadata of images
    image_json_file = open('images.json', 'w')
    json.dump(list_dict_img, image_json_file,  indent=4)
    image_json_file.close()

    return "Download concluído!!!"



def start():
    #fetch_images_from_sentences()
    download_images()




# Para execução sozinha
if len(sys.argv) > 1:
    if sys.argv[1] == 'start':
        start()

#fetch_images_from_sentences()
#print(images_links)
#print(content)