import instaloader
import re
import os
import sys

# Verificar se a URL foi informada corretamente
try:
    url = sys.argv[1]
except IndexError:
    print("Forma de uso:\n\n", sys.argv[0], "URL\n\nInforme uma URL válida\n\n")
    sys.exit()

# Diretório de download
downloadDir = '/home/fabio/Downloads'
os.chdir(downloadDir)

# Inicializar Instaloader
loader = instaloader.Instaloader(
    download_pictures=True, 
    download_videos=True, 
    download_video_thumbnails=False, 
    download_geotags=False,
    download_comments=False, 
    save_metadata=False, 
    compress_json=False,
    filename_pattern='{profile}_{mediaid}'
)

# Extrair "shortcode" da URL
expr = r'\/p\/([^\/]*)\/'
found = re.search(expr, url)

if found:
    print("Baixando post com shortcode:", found.group(1))
    try:
        post = instaloader.Post.from_shortcode(loader.context, found.group(1))
        loader.download_post(post, target='.')
        print("Download concluído.")
    except instaloader.exceptions.InstaloaderException as e:
        print(f"Erro ao baixar o post: {str(e)}")
else:
    print("URL do Instagram inválida ou shortcode não encontrado.")
