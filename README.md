# video-creator
Projeto para criação automática de videos

## Links úteis
https://google-api-client-libraries.appspot.com/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html
https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md

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