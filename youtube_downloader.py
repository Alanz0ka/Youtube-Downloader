import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import os
import re
import threading

# Criação de um semáforo para limitar downloads simultâneos
max_simultaneous_downloads = 10
download_semaphore = threading.Semaphore(max_simultaneous_downloads)

# Função para validar URL
def validar_url(url):
    youtube_video_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_playlist_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(playlist\?list=|.+/p/)?([a-zA-Z0-9_-]+)')
    return youtube_video_regex.match(url) or youtube_playlist_regex.match(url)

# Função para download
def download_video(url, save_path, audio_quality, audio_format, status_label):
    with download_semaphore:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality,
            }],
            'progress_hooks': [lambda d: update_status(d, status_label)],
            'noprogress': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

# Função para baixar vídeos de uma playlist
def download_playlist(url, save_path, audio_quality, audio_format, status_label):
    with download_semaphore:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality,
            }],
            'progress_hooks': [lambda d: update_status(d, status_label)],
            'noprogress': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

# Função para atualizar o texto de status
def update_status(d, status_label):
    if d['status'] == 'downloading':
        status_label.config(text="Baixando...")
    elif d['status'] == 'finished':
        status_label.config(text="Convertendo...")

# Função chamada ao clicar no botão de download
def start_download():
    url = url_entry.get("1.0", tk.END).strip()
    
    if not url or not validar_url(url):
        messagebox.showwarning("Entrada inválida", "Por favor, insira uma URL válida do YouTube ou uma playlist.")
        return

    save_path = filedialog.askdirectory(title="Escolha o diretório para salvar")
    if not save_path:
        return

    audio_format = format_combobox.get()  # Obter formato selecionado
    audio_quality = quality_combobox.get() if audio_format == "mp3" else "192"  # Definir qualidade se MP3

    # Adicionar a URL na lista de downloads em andamento
    downloads_list.insert(tk.END, url)

    # Criar e iniciar uma thread para o download
    status_label.config(text="Iniciando download...")
    
    # Verificar se a URL é uma playlist ou um vídeo
    if "playlist" in url:
        threading.Thread(target=download_playlist_thread, args=(url, save_path, audio_quality, audio_format)).start()
    else:
        threading.Thread(target=download_video_thread, args=(url, save_path, audio_quality, audio_format)).start()

    # Limpar campos de entrada
    url_entry.delete("1.0", tk.END)
    format_combobox.set("mp3")  # Resetar para o formato padrão
    quality_combobox.set("192")  # Resetar para a qualidade padrão

# Função que executa o download de uma playlist em uma thread
def download_playlist_thread(url, save_path, audio_quality, audio_format):
    try:
        download_playlist(url, save_path, audio_quality, audio_format, status_label)
        messagebox.showinfo("Sucesso", "Todos os downloads da playlist foram concluídos com sucesso!")
        status_label.config(text="Pronto!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        status_label.config(text="Erro durante o download!")

# Função que executa o download em uma thread
def download_video_thread(url, save_path, audio_quality, audio_format):
    try:
        download_video(url, save_path, audio_quality, audio_format, status_label)
        messagebox.showinfo("Sucesso", "Download e conversão concluídos com sucesso!")
        status_label.config(text="Pronto!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        status_label.config(text="Erro durante o download!")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Downloader de Músicas do YouTube")

# Layout usando grid
url_label = tk.Label(root, text="Insira a URL do vídeo ou playlist:")
url_label.pack()

url_entry = tk.Text(root, height=2, width=50)
url_entry.pack()

# Combobox para seleção de formato de arquivo
format_label = tk.Label(root, text="Escolha o formato do arquivo:")
format_label.pack()

formats = ["mp3", "wav"]  # Formatos disponíveis
format_combobox = ttk.Combobox(root, values=formats)
format_combobox.set("mp3")  # Definir padrão
format_combobox.pack()

# Combobox para seleção de qualidade de áudio (visível apenas se mp3 for selecionado)
quality_label = tk.Label(root, text="Escolha a qualidade do áudio:")
quality_label.pack()

qualities = ["128", "192", "256", "320"]  # Qualidades disponíveis em kbps
quality_combobox = ttk.Combobox(root, values=qualities)
quality_combobox.set("192")  # Definir padrão
quality_combobox.pack()

# Função para mostrar/ocultar a seleção de qualidade
def toggle_quality_visibility(event):
    if format_combobox.get() == "mp3":
        quality_label.pack()
        quality_combobox.pack()
    else:
        quality_label.pack_forget()
        quality_combobox.pack_forget()

# Bind do evento de alteração de seleção do formato
format_combobox.bind("<<ComboboxSelected>>", toggle_quality_visibility)

download_button = tk.Button(root, text="Baixar e Converter", command=start_download)
download_button.pack()

# Label para exibir o status do download
status_label = tk.Label(root, text="", font=("Helvetica", 12))
status_label.pack(pady=10)

# Lista para exibir downloads em andamento
downloads_label = tk.Label(root, text="Downloads em andamento:")
downloads_label.pack()

downloads_list = tk.Listbox(root, width=60)
downloads_list.pack()

root.mainloop()
