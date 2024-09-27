import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from downloader import Downloader

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Downloader de Músicas do YouTube")
        self.downloader = Downloader()

        self.create_widgets()

    def create_widgets(self):
        url_label = tk.Label(self.root, text="Insira a URL do vídeo ou playlist:")
        url_label.pack()

        self.url_entry = tk.Text(self.root, height=2, width=50)
        self.url_entry.pack()

        format_label = tk.Label(self.root, text="Escolha o formato do arquivo:")
        format_label.pack()

        formats = ["mp3", "wav"]
        self.format_combobox = ttk.Combobox(self.root, values=formats)
        self.format_combobox.set("mp3")
        self.format_combobox.pack()

        quality_label = tk.Label(self.root, text="Escolha a qualidade do áudio:")
        quality_label.pack()

        self.qualities = ["128", "192", "256", "320"]
        self.quality_combobox = ttk.Combobox(self.root, values=self.qualities)
        self.quality_combobox.set("192")
        self.quality_combobox.pack()

        self.toggle_quality_visibility()

        self.download_button = tk.Button(self.root, text="Baixar e Converter", command=self.start_download)
        self.download_button.pack()

        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        downloads_label = tk.Label(self.root, text="Downloads em andamento:")
        downloads_label.pack()

        self.downloads_list = tk.Listbox(self.root, width=60)
        self.downloads_list.pack()

    def toggle_quality_visibility(self):
        if self.format_combobox.get() == "mp3":
            self.quality_combobox.pack()
        else:
            self.quality_combobox.pack_forget()

        self.format_combobox.bind("<<ComboboxSelected>>", lambda event: self.toggle_quality_visibility())

    def update_status(self, d):
        if d['status'] == 'downloading':
            self.status_label.config(text="Baixando...")
        elif d['status'] == 'finished':
            self.status_label.config(text="Convertendo...")

    def start_download(self):
        url = self.url_entry.get("1.0", tk.END).strip()

        if not url or not self.downloader.validar_url(url):
            messagebox.showwarning("Entrada inválida", "Por favor, insira uma URL válida do YouTube ou uma playlist.")
            return

        save_path = filedialog.askdirectory(title="Escolha o diretório para salvar")
        if not save_path:
            return

        audio_format = self.format_combobox.get()
        audio_quality = self.quality_combobox.get() if audio_format == "mp3" else "192"

        self.downloads_list.insert(tk.END, url)
        self.status_label.config(text="Iniciando download...")

        if "playlist" in url:
            threading.Thread(target=self.download_playlist_thread, args=(url, save_path, audio_quality, audio_format)).start()
        else:
            threading.Thread(target=self.download_video_thread, args=(url, save_path, audio_quality, audio_format)).start()

        self.url_entry.delete("1.0", tk.END)
        self.format_combobox.set("mp3")
        self.quality_combobox.set("192")

    def download_playlist_thread(self, url, save_path, audio_quality, audio_format):
        try:
            self.downloader.download_playlist(url, save_path, audio_quality, audio_format, self.update_status)
            messagebox.showinfo("Sucesso", "Todos os downloads da playlist foram concluídos com sucesso!")
            self.status_label.config(text="Pronto!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.status_label.config(text="Erro durante o download!")

    def download_video_thread(self, url, save_path, audio_quality, audio_format):
        try:
            self.downloader.download_video(url, save_path, audio_quality, audio_format, self.update_status)
            messagebox.showinfo("Sucesso", "Download e conversão concluídos com sucesso!")
            self.status_label.config(text="Pronto!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.status_label.config(text="Erro durante o download!")
