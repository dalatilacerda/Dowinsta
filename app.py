from flask import Flask, request, jsonify
import instaloader
import re
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    # Verifica se o URL do vídeo foi enviado
    video_url = request.form.get('videoUrl')
    if not video_url:
        return jsonify({'error': 'URL do vídeo não foi fornecido'}), 400

    # Diretório de download (ajuste conforme necessário)
    download_dir = '/caminho/para/seu/diretorio/de/download'
    os.chdir(download_dir)

    # Inicializa o Instaloader
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        filename_pattern='{profile}_{mediaid}'
    )

    # Extrai o shortcode do URL do vídeo
    expr = r'\/p\/([^\/]*)\/'
    found = re.search(expr, video_url)

    if found:
        try:
            # Baixa o post com base no shortcode
            post = instaloader.Post.from_shortcode(loader.context, found.group(1))
            loader.download_post(post, target='.')
            return jsonify({'message': 'Download do vídeo concluído'}), 200
        except instaloader.exceptions.InstaloaderException as e:
            return jsonify({'error': f'Erro ao baixar o vídeo: {str(e)}'}), 500
    else:
        return jsonify({'error': 'URL do Instagram inválido ou shortcode não encontrado'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
