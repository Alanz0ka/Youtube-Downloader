import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import os
import re
import threading

# Função para validar URL
def validar_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return youtube_regex.match(url)

# Função de download
def download_video(url, save_path, audio_format, status_label):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, f'%(title)s.{audio_format}'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192',
        }],
        'progress_hooks': [lambda d: update_status(d, status_label)],  # Atualiza status
        'noprogress': True  # Desativar barra de progresso do terminal
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Função para atualizar o texto de status
def update_status(d, status_label):
    if d['status'] == 'downloading':
        status_label.config(text="Baixando...")  # Atualiza o status para Baixando...
    elif d['status'] == 'finished':
        status_label.config(text="Convertendo...")  # Atualiza o status para Convertendo...

# Função chamada ao clicar no botão de download
def start_download():
    url = url_entry.get("1.0", tk.END).strip()

    # Validação de URL
    if not url or not validar_url(url):
        messagebox.showwarning("Entrada inválida", "Por favor, insira uma URL válida do YouTube.")
        return

    save_path = filedialog.askdirectory(title="Escolha o diretório para salvar")
    if not save_path:
        return

    audio_format = format_combobox.get().lower()  # Obter formato selecionado

    # Criar e iniciar uma thread para o download
    status_label.config(text="Iniciando download...")  # Mensagem inicial
    threading.Thread(target=download_video_thread, args=(url, save_path, audio_format)).start()

# Função que executa o download em uma thread
def download_video_thread(url, save_path, audio_format):
    try:
        download_video(url, save_path, audio_format, status_label)
        messagebox.showinfo("Sucesso", "Download e conversão concluídos com sucesso!")
        status_label.config(text="Pronto!")  # Mensagem final
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        status_label.config(text="Erro durante o download!")  # Mensagem de erro

# Configuração da interface gráfica
root = tk.Tk()
root.title("Downloader de Músicas do YouTube")

# Layout usando grid
url_label = tk.Label(root, text="Insira a URL do vídeo:")
url_label.pack()

url_entry = tk.Text(root, height=2, width=50)
url_entry.pack()

# Combobox para seleção de formato de áudio
format_label = tk.Label(root, text="Escolha o formato de áudio:")
format_label.pack()

formats = ["mp3", "wav", "aac", "flac"]  # Formatos disponíveis
format_combobox = ttk.Combobox(root, values=formats)
format_combobox.set("mp3")  # Definir padrão
format_combobox.pack()

download_button = tk.Button(root, text="Baixar e Converter", command=start_download)
download_button.pack()

# Label para exibir o status do download
status_label = tk.Label(root, text="", font=("Helvetica", 12))
status_label.pack(pady=10)

root.mainloop()
