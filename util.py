# Arquivo com métodos úteis
import yaml
import json
import logging
import unidecode
import unicodedata

def getCredentials():
    
    # pegando as credenciais das apis
    with open("./credentials/credentials.yml","r") as c:
        try:
            credentials = yaml.safe_load(c)
        except yaml.YAMLError as exc:
            credentials = exc
    
    return credentials


def remove_accents(text):
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")


if __name__ == '__main__':

    texto = "acentuação"
    #print(unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8"))
    print(unicodedata.normalize("NFD", texto))