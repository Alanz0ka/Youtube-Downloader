# Downloader de Músicas do YouTube

Este projeto é uma aplicação simples em Python que permite o download de vídeos do YouTube e a conversão deles para o formato MP3 ou WAV. Ele utiliza a biblioteca yt-dlp para realizar o download e tkinter para a interface gráfica.

## Pré-requisitos

Antes de executar o projeto, você precisa ter os seguintes itens instalados:

- Python 3.x
- pip (gerenciador de pacotes do Python)
- ffmpeg

### Bibliotecas Necessárias

As bibliotecas necessárias estão listadas em `requirements.txt`. Para instalá-las, você pode usar o seguinte comando:

```bash
pip install -r requirements.txt
```

FFmpeg também deve estar instalado no seu sistema para permitir a conversão de vídeo para áudio. Você pode baixar o FFmpeg aqui: [FFmpeg Download](https://ffmpeg.org/download.html).

Lembre-se de, após adicionar o ffmpeg ao PATH, reiniciar a máquina; caso contrário, não irá funcionar.

## Como Usar

1. **Criar um Ambiente Virtual (opcional, mas recomendado)**:
   Você pode usar o `virtualenv` para criar um ambiente virtual:

   ```bash
   pip install virtualenv
   virtualenv venv
   source venv/bin/activate  
   # No Windows, use: 
   venv/Scripts/activate
   ```

2. **Instalar Dependências**:
   Com o ambiente virtual ativado, instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. **Clone ou Baixe o Repositório**:
   Clone este repositório ou faça o download do arquivo Python.

   ```bash
   git clone https://github.com/Alanz0ka/Youtube-Downloader.git
   ```

4. **Execute o Script**:
   Navegue até o diretório do projeto e execute o script:

   ```bash
   python main.py
   ```

5. **Interface Gráfica**:
   - Insira a URL do vídeo ou playlist do YouTube que você deseja baixar.
   - Escolha o formato do arquivo (MP3 ou WAV).
   - Se selecionar MP3, escolha a qualidade do áudio.
   - Clique no botão "Baixar e Converter".
   - Escolha o diretório onde deseja salvar o arquivo.

6. **Conclusão**:
   Após o download, uma mensagem de sucesso será exibida. Se houver algum erro, uma mensagem de erro será mostrada.

## Estrutura do Código

- `validar_url(url)`: Função responsável por validar se a URL é de um vídeo ou playlist do YouTube.
- `download_video(url, save_path, audio_quality, audio_format, status_label)`: Função responsável por realizar o download e conversão do vídeo.
- `download_playlist(url, save_path, audio_quality, audio_format, status_label)`: Função para baixar vídeos de uma playlist.
- `update_status(d, status_label)`: Função para atualizar o texto de status durante o download.
- `start_download()`: Função chamada ao clicar no botão de download, gerenciando a entrada do usuário e iniciando o download em uma thread.

## Exemplo de Uso

1. Abra a aplicação.
2. Insira a URL de um vídeo do YouTube ou uma playlist, por exemplo: `https://www.youtube.com/watch?v=EXEMPLO`.
3. Selecione o formato e a qualidade desejada.
4. O arquivo será salvo no diretório escolhido.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um "issue" ou enviar um "pull request".
