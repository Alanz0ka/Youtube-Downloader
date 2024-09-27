import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os
import re
import threading


def validar_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return youtube_regex.match(url)


def download_video(url, save_path, status_label):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [lambda d: update_status(d, status_label)],  # Atualiza status
        'noprogress': True  # Desativar barra de progresso do terminal
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def update_status(d, status_label):
    if d['status'] == 'downloading':
        status_label.config(text="Baixando...")  
    elif d['status'] == 'finished':
        status_label.config(text="Convertendo...")  

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

    # Criar e iniciar uma thread para o download
    status_label.config(text="Iniciando download...")  # Mensagem inicial
    threading.Thread(target=download_video_thread, args=(url, save_path)).start()

# Função que executa o download em uma thread
def download_video_thread(url, save_path):
    try:
        download_video(url, save_path, status_label)
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

download_button = tk.Button(root, text="Baixar e Converter", command=start_download)
download_button.pack()

# Label para exibir o status do download
status_label = tk.Label(root, text="", font=("Helvetica", 12))
status_label.pack(pady=10)

root.mainloop()
