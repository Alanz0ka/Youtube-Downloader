import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os
import re

# Função para validar URL
def validar_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return youtube_regex.match(url)

def download_video(url, save_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def start_download():
    url = url_entry.get("1.0", tk.END).strip()

    # Validação de URL
    if not url or not validar_url(url):
        messagebox.showwarning("Entrada inválida", "Por favor, insira uma URL válida do YouTube.")
        return

    save_path = filedialog.askdirectory(title="Escolha o diretório para salvar")
    if not save_path:
        return

    try:
        download_video(url, save_path)
        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Configuração da interface gráfica
root = tk.Tk()
root.title("Downloader de Músicas do YouTube")

url_label = tk.Label(root, text="Insira a URL do vídeo:")
url_label.pack()

url_entry = tk.Text(root, height=5, width=50)
url_entry.pack()

download_button = tk.Button(root, text="Baixar e Converter", command=start_download)
download_button.pack()

root.mainloop()
