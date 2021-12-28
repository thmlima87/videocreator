
# importing sys
import sys
import os
# adding robots to the system path
sys.path.insert(0, './robots')

import find_subject as fs
import get_content as gt
import saveDatabase as sdb
import ibm_watson_nlu as watson 
import nltk # Natural language toolkit
import util
import content
import logging # log


# abrindo conexão
#conn = sdb.connect()
# Salvando google trends
#print(sdb.saveMany(conn, gsubject, 'googleTrends'), end="\n\n")

# Salvando twitter trends
#print(sdb.saveMany(conn, tsubject, 'twitterTrends'), end="\n\n")

#print(fs.formatMessageFromGoogleToTelegram(gsubject))
#print(fs.formatMessageFromTwitterToTelegram(tsubject))

#print(watson.get_keywords_from_sentence(sentences[0]))



def print_options(options):
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

def main():
    try:
        options = {}
        # buscando os trending topics
        # google
        gsubject = fs.getGoogleTrends()

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
            #print(gsubject[0]['description'])

        options['google'] = gsubject[0]['title']
        # buscando trending topics do twitter
        tsubject = fs.getTwitterTrends()
        options['twitter'] = tsubject[0]['name']
        # mostrando as opções de conteúdo
        content_choosen = print_options(options)

        # Buscando conteúdo no Wikipedia
        wikipedia = gt.get_wikipedia_content(content_choosen, "pt")
        # creating name folder
        name_folder = content_choosen.lower().replace(" ", "_")
        '''
        if 'images' in wikipedia:
            result_download = gt.download_wikipedia_images(wikipedia['images'], name_folder)
        '''

        # Clean the main text
        if 'extract' in wikipedia:
            cleanedContent = gt.clear_text(wikipedia['extract'])
        else:
            raise Exception('Content not found')
        # Breaking the text in sentences
        logging.info("Breaking the context in sentences...")
        print("Quebrando o texto em sentenças...", end="\n\n")
        sentences = nltk.tokenize.sent_tokenize(cleanedContent)

        # creating the final object
        logging.info("Creating the final object to save on filesystem")
        print("Criando o objeto final para salvar em disco...", end="\n\n")
        video_content = {}
        video_content['original_content'] = wikipedia['extract']
        video_content['cleanedContent'] = cleanedContent
        video_content['sentences'] = []

        logging.info("Getting the keywords from sentences...")
        print("Criando as keywords de cada sentença", end='\n\n')
        # iterating in sentences
        for s in sentences:

            try:
                # analyzing the content with watson
                keywords = watson.get_keywords_from_sentence(s)
            except Exception as ex_analyze:
                print(ex_analyze)

            video_content['sentences'].append({
                'text': s,
                'keywords': keywords,
                'images': []
            })
        # Persisting the object
        content.save_file(video_content)
        print('Processo finalizado!!!')
 
    except Exception as ex:
        logging.error(ex)
        print('Oops... something went wrong!')



if __name__ == '__main__':
    logging.info("Starting video creator")
    print('----------------------------------------------------')
    print('Video Creator')
    print('----------------------------------------------------', end='\n\n')
    print('Starting...', end='\n\n')
    main()