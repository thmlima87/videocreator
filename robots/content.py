import sys
sys.path.insert(0, './')
import requests
import urllib
import json
import logging
import os
import xmltodict
import datetime
import util
import re
from ibm_watson import NaturalLanguageUnderstandingV1
import ibm_watson.natural_language_understanding_v1 as nlu #import Features, EntitiesOptions, KeywordsOptions, 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# buscando credenciais
credentials = util.getCredentials()

def get_google_trends():

    def parser_xml(v_xml):
        key_words = []
        # parser
        content_xml = xmltodict.parse(v_xml)

        for i in content_xml['rss']['channel']['item']:
            
            rel_news = []

            for j in i['ht:news_item']:
                
                if not isinstance(j, str):
                    rel_news.append(j['ht:news_item_title'])

            obj = {
                "title": "{}".format(i['title']), 
                "traffic": "{}".format(i['ht:approx_traffic']),
                "pubDate": "{}".format(i['pubDate']),
                "description": "{}".format(i['description']),
                "related_news": rel_news,
                "dateInsert": datetime.datetime.now()
                }
            key_words.append(obj)
        
        return key_words

    logging.info("--- Buscando assunto no GOOGLE TRENDS ---")
    #print("--- Buscando assunto no GOOGLE TRENDS ---", end="\n\n")
    # URL do trending topics do Google
    url = "https://trends.google.com.br/trends/trendingsearches/daily/rss?geo=BR"

    content = requests.get(url)
    return parser_xml(content.text)


def get_twitter_trends():
    logging.info("--- Buscando assunto no TWITTER TRENDS ---")
    
    headers = {"Authorization": "Bearer {}".format(credentials['api_bearer_token'])}
    url = "https://api.twitter.com/1.1/trends/place.json?id=23424768"
    response = requests.get(url, headers=headers)
    
    content = []
    
    for i in response.json():
        for j in i['trends']:
            content.append({
                "at": datetime.datetime.now(),
                "as_of": i['as_of'],
                "location": i['locations'][0]['name'],
                "name": j['name'],
                "tweet_volume": j['tweet_volume']
            })
    return content




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



def ask_for_a_subject():
    logging.info("--- Asking for content ---")
    logging.info("Getting Google Trends...")
    gsubject = get_google_trends()
    logging.info("Getting Twitter Trends..")
    tsubject = get_twitter_trends()
    # creating options
    options = {}
    options['google'] = gsubject[0]['title']
    options['twitter'] = tsubject[0]['name']

    print("Here some insights...",end='\n\n')

    print(gsubject[0]['title'], end="\n\n")

    if "related_news" in gsubject[0]:
        
        print("Notícias relacionadas: ",end="\n\n")

        for i in gsubject[0]['related_news']:
            print(i)
        print("")

    if "description" in gsubject[0]:
        
        print("Descrição: ", end="\n\n")

        for i in gsubject[0]['description'].split(","):
            print(i.strip())
        print("")

    logging.info('Showing content options')
    content_choosen = "Nenhuma opção escolhida"

    print("Escolha uma das opções")
    print("1) {}".format(options['google']))
    print("2) {}".format(options['twitter']))
    print("3) Outro... ", end="\n\n")

    while True:
        user_input = int(input("Digite o numero do conteúdo desejado: "))
        if user_input == 1:
            content_choosen = options['google']
            break
        elif user_input == 2:
            content_choosen = options['twitter']
            break
        elif user_input == 3:
            content_choosen = input("Digite um termo para ser pesquisado: ")
            break
        else:
            print("Escolha uma opção válida")

    return str(content_choosen)
    

'''
Clear text
'''
def clear_text(text):
    logging.info('Cleaning text...')
    print ("Limpando texto...", end="\n\n")
    return re.sub(r"\([^()]*\)", '', text)


'''
Text Analyze
'''
def content_analyze(content):
    # params from Watson API
    authenticator = IAMAuthenticator(credentials['nlu_watson_api_key'])
    service = NaturalLanguageUnderstandingV1(version='2021-09-26',authenticator=authenticator)
    service.set_service_url(credentials['nlu_watson_url'])

    response = service.analyze(
        text=content,
        features=nlu.Features(entities=nlu.EntitiesOptions(),
                        keywords=nlu.KeywordsOptions(),
                        emotion=nlu.EmotionOptions(),
                        sentiment=nlu.SentimentOptions(),
                        summarization=nlu.SummarizationOptions()
                        )).get_result()
    return json.dumps(response, indent=2)

'''
Get Keywords from a Sentece
'''
def get_keywords_from_sentence(sentence):
    # params from Watson API
    authenticator = IAMAuthenticator(credentials['nlu_watson_api_key'])
    service = NaturalLanguageUnderstandingV1(version='2021-09-26',authenticator=authenticator)
    service.set_service_url(credentials['nlu_watson_url'])
    response = service.analyze(
        text=sentence,
        features=nlu.Features(
                        keywords=nlu.KeywordsOptions())
    ).get_result()
    
    # returning just the list of keywords when relevance > 0.5
    return [d['text'] for d in response['keywords'] if d['relevance'] > 0.5]



def load(path):
    logging.info("Loading content...")
    try:
        os.chdir("./")
        # carrega arquivo
        with open(path, encoding="utf-8") as f:
            content = json.load(f)
    except Exception as ex:
        logging.error(ex)
        content = 'Oops... não foi possível carregar o conteúdo...'

    return content

def save(content):
    logging.info("Saving content...")
    print("Saving content...", end='\n\n')
    # creating name folder
    name_folder = content['search_term'].lower().replace(" ", "_")

    path = "content/{}".format(name_folder)
    # create directory
    os.makedirs(os.path.dirname("{}/content.json".format(path)), exist_ok=True)

    with open("{}/content.json".format(path), "w", encoding='utf8') as f:
        try:
            json.dump(content, f, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex)