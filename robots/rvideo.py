import sys
sys.path.insert(0, './')
import rcontent
import logging
import os

'''
def prepare_images_downloaded():
    logging.info("Preparing images downloaded to compile the video")

    os.chdir('./')
    path = "./content/images"
    
    # create directory
    video_content = rcontent.load()
    
    for idx, sentence in enumerate(video_content['sentences']):
        
        filename = "content/images/{}_sentence.png".format(idx)
        
        for root, folders, files in os.walk('.'):
            for f in files:
                if f.startswith(str("{}_".format(idx))):
                    print("{} = {}".format(idx, f))
                    #filename = 
                    #command = "convert -size 1920x1080 -font helvetica -pointsize 66 -border 30x30 -background 'transparent' -fill white -gravity center caption:'{}' {}".format(sentence['text'], filename)
                    #command = "convert -font helvetica -fill white -pointsize 36 -draw 'text 10,50 \"{}\"' {} {}".format(sentence['text'], f)
        
        #os.system(command)
        #print(texto)
'''     



def prepare_images_downloaded():
    logging.info("Preparing images downloaded to compile the video")

    os.chdir('./')
    path = "./content/images"
    
    # create directory
    video_content = rcontent.load()
        
    for root, folders, files in os.walk('./content/images'):

        for f in files:
            f_split = f.split("_")
            filename_original = os.path.join(root, f)
            #filename_with_border = "{}/{}_{}_bordered.jpg".format(path, f_split[0], f_split[1])
            #filename_bg = "{}/{}_{}_bg.jpg".format(path, f_split[0], f_split[1])
            filename_composite = "{}/{}_{}_composite.jpg".format(path, f_split[0], f_split[1])

            #create_bg_imagem = "convert {} -background 'white' -blur '0x9' -resize '1920x1080^' -gravity center -extent 1920x1080 {}".format(filename_original, filename_bg)
            #create_image_with_border = "convert {} -bordercolor white -border 10x10 {}".format(filename_original, filename_with_border)
            #create_composite = "convert -compose 'over' -composite -gravity 'center' {} {} {}".format(filename_bg, filename_with_border, filename_composite)

            command = "convert {} -background 'white' -blur '0x9' -resize '1920x1080^' -gravity center -extent 1920x1080 \( {} -bordercolor white -border 10x10 \) -compose over -composite {}".format(filename_original, filename_original, filename_composite)
            os.system(command)

            #os.system(create_image_with_border)
            #os.system(create_bg_imagem)
            #os.system(create_composite)

        



def start():
    prepare_images_downloaded()




# Para execução sozinha
if len(sys.argv) > 1:
    if sys.argv[1] == 'start':
        start()