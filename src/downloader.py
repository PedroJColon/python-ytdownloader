import os
from enum import Enum
from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoUnavailable


# Created so user can be updated on the status of the video, whether it succeeded or is unavailable
class Status(Enum):
    SUCCESS = 0
    UNAVAILABLE = 1
    NO_URL = 2
    NONE = 3


class Downloader():
    def __init__(self):
        super().__init__()
        self.video = None
        self.playlist = None
        self.stream = None
        self.percent_downloaded = 0

    def download_video(self, url) -> Status:
        if url == "":
            return Status.NO_URL

        try:
            self.video = YouTube(url)
        except VideoUnavailable:
            return Status.UNAVAILABLE
        else:
            self.stream = self.video.streams.get_highest_resolution()
            self.stream.download()

        return Status.SUCCESS

    def download_audio(self, url, ext) -> Status:
        if url == "":
            return Status.NO_URL

        try:
            self.video = YouTube(url)
        except VideoUnavailable:
            return Status.UNAVAILABLE
        else:
            self.stream = self.video.streams.get_audio_only()
            downloaded_file = self.stream.download()
            # Once downloaded, we want to reformat the file to be a audio file. Below is the steps taken.
            downloaded_path = os.path.splitext(downloaded_file)
            audio_file = downloaded_path[0] + ext
            os.rename(downloaded_file, audio_file)

        return Status.SUCCESS

    def download_playlist(self, url) -> Status:
        if url == "":
            return Status.NO_URL

        download_status = Status.NONE
        video_list = Playlist(url)
        for link in video_list.video_urls:
            download_status = self.download_video(link)

        return download_status
