import os
import re
import threading
import yt_dlp

class Downloader:
    def __init__(self):
        self.max_simultaneous_downloads = 10
        self.download_semaphore = threading.Semaphore(self.max_simultaneous_downloads)

    @staticmethod
    def validar_url(url):
        youtube_video_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_playlist_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(playlist\?list=|.+/p/)?([a-zA-Z0-9_-]+)')
        return youtube_video_regex.match(url) or youtube_playlist_regex.match(url)

    def download_video(self, url, save_path, audio_quality, audio_format, update_status):
        with self.download_semaphore:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': audio_quality,
                }],
                'progress_hooks': [lambda d: update_status(d)],
                'noprogress': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    def download_playlist(self, url, save_path, audio_quality, audio_format, update_status):
        with self.download_semaphore:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': audio_quality,
                }],
                'progress_hooks': [lambda d: update_status(d)],
                'noprogress': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
