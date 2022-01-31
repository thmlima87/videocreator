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
import nltk # Natural language toolkit
from rconfig import *

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

    logging.info("--- Getting GOOGLE TRENDS ---")
    # URL do trending topics do Google
    url = "https://trends.google.com.br/trends/trendingsearches/daily/rss?geo=BR"

    content = requests.get(url)
    return parser_xml(content.text)


def get_twitter_trends():
    logging.info("--- Getting TWITTER TRENDS ---")
    
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
        main_url = WIKIPEDIA_MAIN_URL.format(lang, urllib.parse.unquote(subject))
        main_content = requests.get(main_url)
        main_content_json = main_content.json()
        main_result = main_content_json['query']['pages'][0]
        if  'missing' in main_content_json:
            return main_content_json['missing']
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

        if 'extract' in main_result:
            return main_result['extract']
        else:
            raise ValueError("Conteúdo não encontrado")

    except Exception as ex:
        logging.error(ex)
        print(ex)




def ask_for_a_subject():
    try:
        print("Getting google Trends...")
        gsubject = get_google_trends()
        print("Getting Twitter Trends...", end="\n\n")
        tsubject = get_twitter_trends()

        options = {}
        options[1] = gsubject[0]['title']
        options[2] = tsubject[0]['name']
        options[3] = "Outro"

        # log
        logging.info("--- Asking for content ---")
        # define variable
        content_choosen = "Nenhuma opção escolhida"
        print("Escolha uma das opções", end="\n\n")
        for k in options:
            print("{}) {}".format(k, options[k]))
        
        while content_choosen not in options:
            user_input = int(input("Digite o numero do conteúdo desejado: "))
            if user_input in options:
                content_choosen = options[int(user_input)]
                if content_choosen == 'Outro':
                    content_choosen = input("Digite um termo para ser pesquisado: ")
                    break    
                break
            else:
                print("Escolha uma opção válida")
    except Exception as ex:
        return ex

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
Create sentences from text
'''
def create_sentences_from_text(cleaned_content):
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
    
    # Loading content from content.json    
    #content = load()
    # creating sentences
    sentences = nltk.tokenize.sent_tokenize(cleaned_content)[:MAX_SENTENCES_TO_FETCH]
    list_sentences = []

    for s in sentences:
        try:
            # analyzing the content with watson
            keywords = get_keywords_from_sentence(s)
        except Exception as ex_analyze:
            print(ex_analyze)

        list_sentences.append({
            'text': s,
            'keywords': keywords,
            'images': []
        })

    return list_sentences






'''
Get keywords from a list of sentence from content.json
'''
def get_keywords_from_list_of_sentences():
    logging.info("Getting keywords from content from content.json file")
    # load content from file
    content = load()
    # iterating in sentences
    for s in content['sentences']:
        # params from Watson API
        authenticator = IAMAuthenticator(credentials['nlu_watson_api_key'])
        service = NaturalLanguageUnderstandingV1(version='2021-09-26',authenticator=authenticator)
        service.set_service_url(credentials['nlu_watson_url'])
        response = service.analyze(
            text=s['text'],
            features=nlu.Features(
                            keywords=nlu.KeywordsOptions())
        ).get_result()
        
        s['keywords'] = [d['text'] for d in response['keywords'] if d['relevance'] > 0.5]
    
    save(content)
    # returning just the list of keywords when relevance > 0.5
    return 




def load():
    logging.info("Loading content...")
    path = 'content/content.json'
    try:
        #os.chdir("./")
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
    path = "content"
    # create directory
    os.makedirs(os.path.dirname("{}/content.json".format(path)), exist_ok=True)

    with open("{}/content.json".format(path), "w", encoding='utf8') as f:
        try:
            json.dump(content, f, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex)



def ask_for_a_category():
    # log
    logging.info("--- Asking for a category ---")
    print("Qual a categoria do conteúdo? ", end="\n\n")

    category_choosen = 0
    available_options = []
    for category in YOUTUBE_CATEGORY_LIST:
        print("{}) {}".format(category[0], category[1]))
        available_options.append(category[0])
    
    while category_choosen == 0:
        user_input = int(input("Digite o numero da categoria escolhida: "))
        if user_input in available_options:
            category_choosen = user_input
            break
        else:
            print("Escolha uma opção válida")

    return str(category_choosen)


'''
# function start()
'''
def start():
    
    logging.info("Asking for a subject...")
    content = {}
    content['youtube_details'] = {}
    content['search_term'] = ask_for_a_subject()
    content['youtube_details']['category_id'] = ask_for_a_category()
    content['original_content'] = get_wikipedia_content(content['search_term'], "pt")
    
    if content['original_content'] is not None:
        content['cleaned_content'] = clear_text(content['original_content'])

        # Breaking the text in sentences
        logging.info("Breaking the main text in sentences...")
        print("Creating sentences from cleaned text...")
        content['sentences'] = create_sentences_from_text(content['cleaned_content'])
        response = True
    else:
        response = False
        raise ValueError("Conteúdo não encontrado")
    
    save(content)
    return response
    


# em caso de execução do arquivo diretamente
if __name__ == '__main__':
    start()