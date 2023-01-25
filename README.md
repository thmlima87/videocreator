# Video Creator
Projeto para criação automática de videos.

Este projeto foi inspirado pelo canal do Filipe Deschamps. Mais precisamente pela série de videos onde ele programou 4 robôs para criar videos para o Youtube:

https://www.youtube.com/watch?v=kjhu1LEmRpY&list=PLMdYygf53DP4YTVeu0JxVnWq01uXrLwHi

Resolvi fazer a minha versão, em Python, com algumas ferramentas alternativas como o as próprias APIs do Wikipedia para download do conteúdo, a lib NLTK para geração das sentenças, o Bing Custom Search para a busca de imagens, o MoviePy para a compilação do video além da implementação de sugestões de conteúdo baseado nas pesquisas diárias do Google e no Trending topics do Twitter.

### Onde encontro mais detalhes?
Afim de fixar e compartilhar o conteúdo aprendido, resolvi criar uma série de posts explicando todo o processo de criação desse projeto, segue o link:

https://variavelconstante.com.br/2022/03/03/python-na-pratica-gerando-videos-para-o-youtube-de-forma-automatica/


## Abaixo algumas anotações que fui fazendo no decorrer do projeto.


### Links úteis
1. https://google-api-client-libraries.appspot.com/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html
2. https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
3. https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
4. https://amhajja.medium.com/overlaying-text-on-images-using-moviepy-a396b028e14f
5. https://zulko.github.io/moviepy/ref/audiofx/moviepy.audio.fx.all.audio_loop.html
6. https://www.reddit.com/r/moviepy/comments/343q8j/what_is_the_correct_way_to_add_audio_to_a_video/
7. https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-custom-images-api-v7-reference#:~:text=The%20maximum%20file%20size%20that%20you%20may%20specify%20is%20520%2C192%20bytes.
8. https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=26196
9. http://sergioaraujo.pbworks.com/w/page/15863922/imagemagick
10. https://rogeriopradoj.com/2019/07/14/como-tirar-acentos-de-string-no-python-transliterate-unicodedata-e-unidecode//
11. https://cse.google.com/cse/all
12. https://www.mediawiki.org/wiki/API:Main_page
13. https://www.mediawiki.org/w/api.php?action=help&modules=query
14. https://www.imagemagick.org/script/index.php
15. http://sergioaraujo.pbworks.com/w/page/15863922/imagemagick


### Image Magick
#### Installing on Ubuntu
```console
sudo apt-get install imagemagick
```
#### Default path for configs
```console
/etc/ImageMagick-x
```

#### Comandos Úteis

##### criando imagem borrada
```console
convert arquivo_original.jpg -background 'white' -blur '0x9' -resize '1920x1080' novo_arquivo.jpg
convert arquivo_original.jpg -background 'white' -blur '0x9' -resize '1920x1080^' -gravity center -extent 1920x1080 arquivo_convertido.jpg
```
##### Criar borda fade na imagem
```console
convert arquivo_original.jpg -bordercolor black -fill white \
   \( -clone 0 -colorize 100 -shave 10x10 -border 10x10 -blur 0x10 \) \
   -compose copyopacity -composite output.png


convert arquivo_original -bordercolor white -border 10x10 output.png
```

##### Criando composição
```console
convert -compose 'over' -composite -gravity 'center' 0_1_bg.jpg 0_1_original.jpg 0_1_converted.jpg
```
##### Criando imagens com texto
```console
convert -size 800x500 -font helvetica -pointsize 36 -background 'transparent' -fill white -gravity south caption:'teste teste' texto.png
convert -font helvetica -fill white -pointsize 36 -draw 'text 10,50 "Floriade 2002, Canberra, Australia"' input_file.jpg output_file.png
```
##### Montagem com fotos
```console
montage *.jpg -shadow -geometry +10+10 montagem.jpg
```


### MoviePy
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

### Bing Custom Search
1) Criar conta em https://portal.azure.com/
2) Criar uma subscription pay as you go
3) Criar o bing resource com Free Tier
4) Criar uma instancia do bing custom search em: https://www.customsearch.ai/applications


## INFORMAÇÕES ÚTEIS

### Problema com imagens em preto e branco

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
