
# importing sys
import sys
import os
# adding robots to the system path
sys.path.insert(0, './robots')
import nltk # Natural language toolkit
import rcontent # content robot
import rimage
import rvideo
import ryoutube
import logging # log


def main():
    try:
        # Iniciando o robo de conteúdo
        
        print("Starting Content robot")
        rcontent.start()
        
        print("--- Starting image robot ---")
        rimage.start()
        
        print("--- Starting Video robot ---")
        rvideo.start()
        
        print("--- Starting to upload video to Youtube ---")
        ryoutube.start()

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