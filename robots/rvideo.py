import sys
sys.path.insert(0, './')
import rcontent
import logging
import os
import util
from PIL import Image
from rconfig import\
    CONTENT_PATH,\
    CONTENT_IMAGES_PATH,\
    CONTENT_SOUND_PATH,\
    CREDENTIALS_PATH,\
    VIDEO_INTRODUCTION_TEXT,\
    VIDEO_SCREENSIZE,\
    VIDEO_TEXT_COLOR_DEFAULT,\
    VIDEO_TEXT_FONT_DEFAULT,\
    VIDEO_FONT_SIZE_DEFAULT,\
    VIDEO_TEXT_POSITION_DEFAULT,\
    VIDEO_FRAME_DURATION_DEFAULT,\
    VIDEO_TEXT_KERNING_DEFAULT,\
    VIDEO_CODEC_DEFAULT,\
    VIDEO_FPS_DEFAULT


#import numpy as np

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
    
    #os.chdir('./')
    #path = "./content/images"
    path = CONTENT_IMAGES_PATH
    # removing existing composite images
    os.system("rm -rf {}/*_composite*".format(path))
    # create directory
    video_content = rcontent.load()
        
    for root, folders, files in os.walk('./content/images'):

        for f in files:
            f_split = f.split("_")
            idx_sentence = int(f_split[0])
            filename_original = os.path.join(root, f)
            filename_composite = "{}/{}_composite.jpg".format(path, f_split[0])
            filename_resized = "{}/{}_resized.jpg".format(path, f_split[0])
            sentence = video_content['sentences'][idx_sentence]['text']
            # creating comands
            create_image_resized = "convert {} -resize '1280x720' {}".format(filename_original, filename_resized)
            create_image_composite = "convert {} -background 'white' -blur '0x9' -resize '1920x1080^' -extent 1920x1080 \( {} -bordercolor white -border 10x10 \) -compose over -gravity center -composite {}".format(filename_original, filename_resized, filename_composite)
            
            # creating images
            os.system(create_image_resized)
            os.system(create_image_composite)

            # removing resized images
            os.system("rm -rf {}/*_resized*".format(path))


def compile_video():
    logging.info("Compiling video...")

    formatter = {"PNG": "RGBA", "JPEG": "RGB"}
    #os.chdir('./')
    #path = "./content/images"
    path = CONTENT_IMAGES_PATH
    
    # create directory
    video_content = rcontent.load()

    video_filename = util.remove_accents(video_content['search_term']).replace(" ", "_") + ".mp4"
    video_content['video_filename'] = video_filename
    video_content['youtube_details']['title'] = "Um pouco sobre {}".format(video_content['search_term'])

    rcontent.save(video_content)
    # carregando musica
    music = AudioFileClip('{}/gypsy-jaxx.mp3'.format(CONTENT_SOUND_PATH))
    new_audioclip = CompositeAudioClip([music])
    
    screensize = VIDEO_SCREENSIZE
    txt_size = (.8*screensize[0],0)
    color = VIDEO_TEXT_COLOR_DEFAULT
    font = VIDEO_TEXT_FONT_DEFAULT
    font_size = VIDEO_FONT_SIZE_DEFAULT
    list_video_clips = []
    # Criando introdução
    txt_clip1 = TextClip(VIDEO_INTRODUCTION_TEXT,color=color, font=font, kerning = VIDEO_TEXT_KERNING_DEFAULT, fontsize=100, method='caption', size=txt_size).set_pos(VIDEO_TEXT_POSITION_DEFAULT).set_duration(VIDEO_FRAME_DURATION_DEFAULT)
    txt_clip2 = TextClip('um pouco sobre...',color=color, font=font, kerning = VIDEO_TEXT_KERNING_DEFAULT, fontsize=100, method='caption', size=txt_size).set_pos(VIDEO_TEXT_POSITION_DEFAULT).set_duration(VIDEO_FRAME_DURATION_DEFAULT)
    txt_clip3 = TextClip(video_content['search_term'],color=color, font=font, kerning = VIDEO_TEXT_KERNING_DEFAULT, fontsize=100, method='caption', size=txt_size).set_pos(VIDEO_TEXT_POSITION_DEFAULT).set_duration(VIDEO_FRAME_DURATION_DEFAULT)
    img_clip = ImageClip("{}../../default/bg_default_new.jpeg".format(path)).set_duration(VIDEO_FRAME_DURATION_DEFAULT)
    cvc1 = CompositeVideoClip([img_clip,txt_clip1], size=screensize)
    cvc2 = CompositeVideoClip([img_clip,txt_clip2], size=screensize)
    cvc3 = CompositeVideoClip([img_clip,txt_clip3], size=screensize)
    list_video_clips.append(cvc1)
    list_video_clips.append(cvc2)
    list_video_clips.append(cvc3)

    #for root, folders, files in os.walk('./content/images'):
    for idx, sentence in enumerate(video_content['sentences']):

        filename = "{}/{}_composite.jpg".format(path, idx)
        
        # workaround to resolve the problems with grayscale image
        img = Image.open(filename)
        rgbimg = Image.new(formatter.get(img.format, 'RGB'), img.size)
        rgbimg.paste(img)
        rgbimg.save(filename, format=img.format)

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
    final.write_videofile('{}/{}'.format(CONTENT_PATH, video_filename),fps=VIDEO_FPS_DEFAULT,codec=VIDEO_CODEC_DEFAULT)






def start():
    prepare_images_downloaded()
    compile_video()



# em caso de execução do arquivo diretamente
if __name__ == '__main__':
    start()