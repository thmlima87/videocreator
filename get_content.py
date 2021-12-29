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