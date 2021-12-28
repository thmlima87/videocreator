import yaml
import json
from ibm_watson import NaturalLanguageUnderstandingV1
import ibm_watson.natural_language_understanding_v1 as nlu #import Features, EntitiesOptions, KeywordsOptions, 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

with open("credentials.yml","r") as c:
    try:
        credentials = yaml.safe_load(c)
    except yaml.YAMLError as exc:
        print(exc)


authenticator = IAMAuthenticator(credentials['nlu_watson_api_key'])
service = NaturalLanguageUnderstandingV1(version='2021-09-26',authenticator=authenticator)
service.set_service_url(credentials['nlu_watson_url'])

def content_analyze(content):
    response = service.analyze(
        text=content,
        features=nlu.Features(entities=nlu.EntitiesOptions(),
                        keywords=nlu.KeywordsOptions(),
                        emotion=nlu.EmotionOptions(),
                        sentiment=nlu.SentimentOptions(),
                        summarization=nlu.SummarizationOptions()
                        )).get_result()
    return json.dumps(response, indent=2)

def get_keywords_from_sentence(sentence):
    response = service.analyze(
        text=sentence,
        features=nlu.Features(
                        keywords=nlu.KeywordsOptions())
    ).get_result()
    
    # returning just the list of keywords when relevance > 0.5
    return [d['text'] for d in response['keywords'] if d['relevance'] > 0.5]