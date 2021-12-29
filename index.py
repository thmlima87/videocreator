
# importing sys
import sys
import os
# adding robots to the system path
sys.path.insert(0, './robots')
import saveDatabase as sdb
import nltk # Natural language toolkit
import content # content robot
import images
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





def main():
    try:
        # creating object
        logging.info("Creating the data struct...")
        print("Creating the data struct...", end="\n\n")
        video_content = {}
        video_content['search_term'] = ""
        video_content['original_content'] = ""
        video_content['cleaned_content'] = ""
        video_content['sentences'] = []

        print("Asking for content...")
        # ask for content
        video_content['search_term'] = content.ask_for_a_subject()

        # Buscando conteúdo no Wikipedia
        wikipedia = content.get_wikipedia_content(video_content['search_term'], "pt")
        video_content['original_content'] = wikipedia['extract']
        
        '''
        if 'images' in wikipedia:
            result_download = gt.download_wikipedia_images(wikipedia['images'], name_folder)
        '''
        # salvando objeto no disco
        content.save(video_content)

        # Clean the main text
        if 'extract' in wikipedia:
            cleaned_content = content.clear_text(wikipedia['extract'])
            video_content['cleaned_content'] = cleaned_content
        else:
            raise Exception('Content not found')
        # Breaking the text in sentences
        logging.info("Breaking the context in sentences...")
        print("Quebrando o texto em sentenças...", end="\n\n")
        sentences = nltk.tokenize.sent_tokenize(cleaned_content)


        logging.info("Getting the keywords from sentences...")
        print("Criando as keywords para cada sentença", end='\n\n')
        # iterating in sentences
        for s in sentences:

            try:
                # analyzing the content with watson
                keywords = content.get_keywords_from_sentence(s)
            except Exception as ex_analyze:
                print(ex_analyze)

            video_content['sentences'].append({
                'text': s,
                'keywords': keywords,
                'images': []
            })
        # Persisting the object
        content.save(video_content)

        logging.info("Starting image robot...")
        print("--- Starting image robot ---")
        images.start()

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