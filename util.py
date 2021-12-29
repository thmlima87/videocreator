# Arquivo com métodos úteis
import yaml
import json
import logging

def getCredentials():
    
    # pegando as credenciais das apis
    with open("credentials.yml","r") as c:
        try:
            credentials = yaml.safe_load(c)
        except yaml.YAMLError as exc:
            credentials = exc
    
    return credentials

