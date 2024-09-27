# README.md

# Downloader de Músicas do YouTube

Este projeto é uma aplicação simples em Python que permite o download de vídeos do YouTube e a conversão deles para o formato MP3. Ele utiliza a biblioteca yt-dlp para realizar o download e tkinter para a interface gráfica.

## Pré-requisitos

Antes de executar o projeto, você precisa ter os seguintes itens instalados:

- Python 3.x
- pip (gerenciador de pacotes do Python)
- ffmpeg

### Bibliotecas Necessárias

Instale as bibliotecas necessárias com o seguinte comando:

pip install yt-dlp

FFmpeg também deve estar instalado no seu sistema para permitir a conversão de vídeo para áudio. Você pode baixar o FFmpeg aqui: https://ffmpeg.org/download.html.

Lembre-se de após adicionar o ffmpeg ao path, reiniciar a máquina, caso contrário, não irá funcionar

## Como Usar

1. **Clone ou Baixe o Repositório**:
   Clone este repositório ou faça o download do arquivo Python.

   git clone https://github.com/Alanz0ka/Youtube-Downloader.git

2. **Execute o Script**:
   Navegue até o diretório do projeto e execute o script:

   python nome_do_arquivo.py

3. **Interface Gráfica**:
   - Insira a URL do vídeo do YouTube que você deseja baixar.
   - Clique no botão "Baixar e Converter".
   - Escolha o diretório onde deseja salvar o arquivo MP3.

4. **Conclusão**:
   Após o download, uma mensagem de sucesso será exibida. Se houver algum erro, uma mensagem de erro será mostrada.

## Estrutura do Código

- download_video(url, save_path): Função responsável por realizar o download e conversão do vídeo.
- start_download(): Função que lida com a entrada do usuário, inicia o download e exibe mensagens.
- Interface gráfica utilizando tkinter com campos para entrada de URL e botão de download.

## Exemplo de Uso

1. Abra a aplicação.
2. Insira a URL de um vídeo do YouTube, por exemplo: https://www.youtube.com/watch?v=EXEMPLO.
3. Selecione o diretório de destino.
4. O arquivo MP3 será salvo no diretório escolhido.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um "issue" ou enviar um "pull request".
