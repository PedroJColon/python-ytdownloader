import os
from pytube import YouTube


class Downloader():
    def __init__(self):
        super().__init__()
        self.video = None
        self.stream = None

    def download_video(self, url):
        if url == "":
            return

        self.video = YouTube(url)
        self.stream = self.video.streams.get_highest_resolution()
        self.stream.download()

    def download_audio(self, url, ext):
        if url == "":
            return

        self.video = YouTube(url)
        self.stream = self.video.streams.get_audio_only()
        downloaded_file = self.stream.download()
        downloaded_path = os.path.splitext(downloaded_file)
        audio_file = downloaded_path[0] + ext
        os.rename(downloaded_file, audio_file)
