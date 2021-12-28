import requests
import xmltodict
import json
import datetime
import util
import logging

def formatMessageFromGoogleToTelegram(content):
    msg = "1) {}\n2) {} \n3) {}".format(content[0]['title'], content[1]['title'], content[2]['title'])
    return msg

def formatMessageFromTwitterToTelegram(content):
    msg = "1) {}\n2) {} \n3) {}".format(content[0]['name'], content[1]['name'], content[2]['name'])
    return msg

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


def getGoogleTrends():
    logging.info("--- Buscando assunto no GOOGLE TRENDS ---")
    #print("--- Buscando assunto no GOOGLE TRENDS ---", end="\n\n")
    # URL do trending topics do Google
    url = "https://trends.google.com.br/trends/trendingsearches/daily/rss?geo=BR"

    content = requests.get(url)
    return parser_xml(content.text)


def getTwitterTrends():
    logging.info("--- Buscando assunto no TWITTER TRENDS ---")
    # buscando credenciais
    credentials = util.getCredentials()

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