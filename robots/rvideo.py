import sys
sys.path.insert(0, './')
import rcontent
import logging
import os

import numpy as np

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects



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
            idx_sentence = int(f_split[0])
            filename_original = os.path.join(root, f)
            #filename_with_border = "{}/{}_{}_bordered.jpg".format(path, f_split[0], f_split[1])
            #filename_bg = "{}/{}_{}_bg.jpg".format(path, f_split[0], f_split[1])
            filename_composite = "{}/{}_composite.jpg".format(path, f_split[0])
            #filename_text = "{}/{}_text.jpg".format(path, f_split[0])
            sentence = video_content['sentences'][idx_sentence]['text']

            #create_bg_imagem = "convert {} -background 'white' -blur '0x9' -resize '1920x1080^' -gravity center -extent 1920x1080 {}".format(filename_original, filename_bg)
            #create_image_with_border = "convert {} -bordercolor white -border 10x10 {}".format(filename_original, filename_with_border)
            #create_composite = "convert -compose 'over' -composite -gravity 'center' {} {} {}".format(filename_bg, filename_with_border, filename_composite)

            command = "convert {} -background 'white' -blur '0x9' -resize '1920x1080^' -extent 1920x1080 \( {} -bordercolor white -border 10x10 \) -compose over -gravity center -composite {}".format(filename_original, filename_original, filename_composite)
            os.system(command)
            
            #command_text = "convert -size 1024x720 -font helvetica -background 'transparent' -fill white caption:'{}' {}".format(sentence, filename_text)
            #os.system(command_text)
            
            #os.system(create_image_with_border)
            #os.system(create_bg_imagem)
            #os.system(create_composite)



def compile_video():
    logging.info("Compiling video...")

    os.chdir('./')
    path = "./content/images"
    
    # create directory
    video_content = rcontent.load()

    # carregando musica
    music = AudioFileClip('./content/music/gypsy-jaxx.mp3')
    new_audioclip = CompositeAudioClip([music])

    screensize = (1920,1080)
    txt_size = (.8*screensize[0],0)
    color = 'white'
    font = 'helvetica'
    font_size = 50
    list_video_clips = []
    # Criando introdução
    txt_clip1 = TextClip('Variavel Constante\npresents...',color=color, font=font, kerning = 5, fontsize=100, method='caption', size=txt_size).set_pos('center').set_duration(4)
    txt_clip2 = TextClip('um pouco sobre...',color=color, font=font, kerning = 5, fontsize=100, method='caption', size=txt_size).set_pos('center').set_duration(4)
    txt_clip3 = TextClip(video_content['search_term'],color=color, font=font, kerning = 5, fontsize=100, method='caption', size=txt_size).set_pos('center').set_duration(4)
    img_clip = ImageClip("{}../../default/bg_default_new.jpeg".format(path)).set_duration(4)
    cvc1 = CompositeVideoClip([img_clip,txt_clip1], size=screensize)
    cvc2 = CompositeVideoClip([img_clip,txt_clip2], size=screensize)
    cvc3 = CompositeVideoClip([img_clip,txt_clip3], size=screensize)
    list_video_clips.append(cvc1)
    list_video_clips.append(cvc2)
    list_video_clips.append(cvc3)

    #for root, folders, files in os.walk('./content/images'):
    for idx, sentence in enumerate(video_content['sentences']):
        filename = "{}/{}_composite.jpg".format(path, idx)
        
        duration = int(len(sentence['text'])/15)

        txt_clip = TextClip('{}'.format(sentence['text']),color=color, font=font, kerning = 5, fontsize=font_size, method='caption', size=txt_size).set_pos('center').set_duration(duration)
        im_width, im_height = txt_clip.size
        color_clip = ColorClip(size=(1920, int(im_height*3)), color=(0, 0, 0)).set_pos('center')
        color_clip = color_clip.set_opacity(.6)
        
        clip_to_overlay = CompositeVideoClip([color_clip, txt_clip], size=screensize).set_position('center')
        #cvc = CompositeVideoClip([txt_clip,img_clip], size=screensize)
        if os.path.isfile(filename):
            img_clip = ImageClip(filename).set_duration(duration)
            cvc = CompositeVideoClip([img_clip,clip_to_overlay], size=screensize).set_duration(duration)
        else:
            cvc = CompositeVideoClip([clip_to_overlay], size=screensize).set_duration(duration)

        list_video_clips.append(cvc)
    
    # Criando o fechamento do video
    txt_fechamento = TextClip('Obrigado por assistir!!!\nd(~.~)b',color=color, font=font, kerning = 5, fontsize=100, method='caption', size=screensize).set_pos('center').set_duration(4)
    list_video_clips.append(txt_fechamento)

    #final_clip = concatenate_videoclips(clips)
    #final_clip.write_videofile('./content/coolTextEffects.avi',fps=25,codec='mpeg4')
    final_clip = concatenate_videoclips(list_video_clips)

    audio = afx.audio_loop(music, duration=final_clip.duration)
    final = final_clip.set_audio(audio).audio_fadeout(5)
    final.write_videofile('./content/video_sentences.avi',fps=30,codec='mpeg4')






def start():
    prepare_images_downloaded()
    compile_video()




# Para execução sozinha
if len(sys.argv) > 1:
    if sys.argv[1] == 'start':
        start()