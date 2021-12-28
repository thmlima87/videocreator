import wget
import urllib
import Algorithmia
import yaml
import requests
import json
import os
import errno
import logging
import re # regular expression

# pegando as credenciais das apis
with open("credentials.yml","r") as c:
    try:
        credentials = yaml.safe_load(c)
    except yaml.YAMLError as exc:
        print(exc)

'''
def getWikipediaContent(subject, lang):

    # Algorithmia
    try:
        client = Algorithmia.client(credentials['algo_key'])
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=500) # optional

        # Algorithmia params
        input_params = {
            "articleName": "{}".format(subject),
            "lang": "{}".format(lang)
        }
        result = algo.pipe(input_params).result
    except Exception as ex:
        result = ex

    return result
'''
def get_wikipedia_content(subject, lang):
    logging.info("Searching about the content choosen on wikipedia")
    print("")
    print("---------------------------------------------------------------------------------------------")
    print("Buscando conteúdo na wikipedia para assunto escolhido: {}".format(subject), end="\n\n")
    try:
        # main subject
        #url = "https://{}.wikipedia.org/api/rest_v1/page/summary/{}".format(lang, subject)
        main_url = "https://{}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&exlimit=1&titles={}&explaintext=1&formatversion=2&media=1".format(lang, urllib.parse.unquote(subject))
        main_content = requests.get(main_url)
        main_content_json = main_content.json()
        main_result = main_content_json['query']['pages'][0]
        if  'missing' in main_content_json:
            main_result['missing'] = main_content_json['missing']
        # media
        media_url = "https://{}.wikipedia.org/api/rest_v1/page/media-list/{}?redirect=false".format(lang, subject)
        media_content = requests.get(media_url)
        media_content_json = media_content.json()
        # get images if there is
        if 'items' in media_content_json:
            media_result = media_content_json['items']
            # incluindo imagens no payload principal
            main_result['images'] = media_result
        # removing unnecessary keys
        main_result.pop('pageid', None)
        main_result.pop('ns', None)

        result = main_result
    except Exception as ex:
        logging.error('Não foi possível buscar conteúdo do wikipedia')
        result = ex

    return result

#
#Download das imagens do conteúdo do wikipedia
#
'''def download_wikipedia_images(images):

    images = list(set(images))

    for img in images:

        i = urllib.parse.unquote(img)
        try:
            image_filename = wget.download(i, "images/download")
            print("")
        except:
            continue
    
    return "Download concluído!!!"


def download_wikipedia_images(img):

    i = urllib.parse.unquote(img)
    try:
        image_filename = wget.download(i, "images/download")
        print("")
    except Exception as ex:
        print(ex)
    
    return "Download concluído!!!"
'''


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

def clear_text(text):
    logging.info('Cleaning text...')
    print ("Limpando texto...", end="\n\n")
    return re.sub(r"\([^()]*\)", '', text)
