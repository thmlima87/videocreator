import json
import logging
import os

def load():
    logging.info("Loading content...")
    try:
        os.chdir("./")
        # carrega arquivo
        with open("content.json", encoding="utf-8") as f:
            content = json.load(f)
    except Exception as ex:
        logging.error(ex)
        content = 'Oops... não foi possível carregar o conteúdo...'

    return content

def save_file(object):
    logging.info("Persisting the object...")
    print("Salvando objeto... ", end="\n\n")
    with open("content.json", "w", encoding='utf8') as f:
        try:
            json.dump(object, f, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(ex)