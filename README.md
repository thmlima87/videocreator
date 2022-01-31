# video-creator
Projeto para criação automática de videos

## Links úteis
https://google-api-client-libraries.appspot.com/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html
https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
https://amhajja.medium.com/overlaying-text-on-images-using-moviepy-a396b028e14f
https://zulko.github.io/moviepy/ref/audiofx/moviepy.audio.fx.all.audio_loop.html
https://www.reddit.com/r/moviepy/comments/343q8j/what_is_the_correct_way_to_add_audio_to_a_video/
https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-custom-images-api-v7-reference#:~:text=The%20maximum%20file%20size%20that%20you%20may%20specify%20is%20520%2C192%20bytes.
https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=26196
http://sergioaraujo.pbworks.com/w/page/15863922/imagemagick
#### Remoção de acentuação
https://rogeriopradoj.com/2019/07/14/como-tirar-acentos-de-string-no-python-transliterate-unicodedata-e-unidecode//

#### Compute Search Engine
https://cse.google.com/cse/all

### APIS do Wikipedia
https://www.mediawiki.org/wiki/API:Main_page
https://www.mediawiki.org/w/api.php?action=help&modules=query

### Image Magick
https://www.imagemagick.org/script/index.php
http://sergioaraujo.pbworks.com/w/page/15863922/imagemagick
https://docs.wand-py.org/en/0.6.7/ ???  

#### Installing on Ubuntu
sudo apt-get install imagemagick

#### Default path for configs
/etc/ImageMagick-x

#### Comandos Úteis

##### criando imagem borrada
> convert arquivo_original.jpg -background 'white' -blur '0x9' -resize '1920x1080' novo_arquivo.jpg
> convert arquivo_original.jpg -background 'white' -blur '0x9' -resize '1920x1080^' -gravity center -extent 1920x1080 arquivo_convertido.jpg

##### Criar borda fade na imagem
> convert 3_0_original.jpg6wf6ou70.tmp -bordercolor black -fill white \
   \( -clone 0 -colorize 100 -shave 10x10 -border 10x10 -blur 0x10 \) \
   -compose copyopacity -composite output.png

convert 3_0_original.jpg6wf6ou70.tmp -bordercolor white -border 10x10 output.png

##### Criando composição
> convert -compose 'over' -composite -gravity 'center' 0_1_bg.jpg 0_1_original.jpg 0_1_converted.jpg

##### Criando imagens com texto
convert -size 800x500 -font helvetica -pointsize 36 -background 'transparent' -fill white -gravity south caption:'teste teste' texto.png
convert -font helvetica -fill white -pointsize 36 -draw 'text 10,50 "Floriade 2002, Canberra, Australia"' input_file.jpg output_file.png

##### Montagem com fotos
montage *.jpg -shadow -geometry +10+10 montagem.jpg


## Video
https://zulko.github.io/moviepy/gallery.html

#### Configurações importantes
- No linux, ao instalar o moviepy, ele automaticamente sabe onde está instalado o Image Magick. No windows é preciso criar a variável de ambiente IMAGEMAGICK_BINARY contendo o caminho do binário.
- O Moviepy faz uso de recursos do Image Magick. É preciso configurar uma política de segurança, do contrário, dará erro na hora de compilar o video.
- Como isso é somente uma POC, apenas comentei no arquivo /etc/ImageMagick-x/policy.xml algumas linhas.

```html
<!--<policy domain="path" rights="none" pattern="@*"/>-->
<!--<policy domain="resource" name="width" value="16KP"/>-->
<!--<policy domain="resource" name="height" value="16KP"/>-->
```

## Bing Custom Search
1) Criar conta em https://portal.azure.com/
2) Criar uma subscription pay as you go
2) Criar o bing resource com Free Tier
3) Criar uma instancia do bing custom search em: https://www.customsearch.ai/applications



# PRÓXIMOS PASSOS
1) Add logs e diminuir prints
2) Verificar tamanho das imagens baixadas, e converter todas as necessárias para o tamanho padrão HD
3) Implementar template para construção do video


# Chamada para upload de video
python upload_video.py --file="content/video_sentences.avi" --title="Just a test" --description="Just a simple test" --keywords="test, simple" --category="19" --privacyStatus="private"


# Little tricks
Depois de importar a lib nltk, será necessário executar a linha debaixo:

  >>> import nltk
  >>> nltk.download('punkt')


# INFORMAÇÕES ÚTEIS
https://github.com/Zulko/moviepy/issues/623

A lib moviepy apresenta o seguinte erro com imagens em preto e branco

```python
Error: could not broadcast input array from shape (1080,1920) into shape (1080,1920,3)
```

#### Contornando o problema
```python
from PIL import Image
formatter = {"PNG": "RGBA", "JPEG": "RGB"}
img = Image.open(file_name)
rgbimg = Image.new(formatter.get(img.format, 'RGB'), img.size)
rgbimg.paste(img)
rgbimg.save(file_name, format=img.format)
```




# YOUTUBE CATEGORIES LIST

1 - Film & Animation
2 - Autos & Vehicles
10 - Music
15 - Pets & Animals
17 - Sports
18 - Short Movies
19 - Travel & Events
20 - Gaming
21 - Videoblogging
22 - People & Blogs
23 - Comedy
24 - Entertainment
25 - News & Politics
26 - Howto & Style
27 - Education
28 - Science & Technology
29 - Nonprofits & Activism
30 - Movies
31 - Anime/Animation
32 - Action/Adventure
33 - Classics
34 - Comedy
35 - Documentary
36 - Drama
37 - Family
38 - Foreign
39 - Horror
40 - Sci-Fi/Fantasy
41 - Thriller
42 - Shorts
43 - Shows
44 - Trailers