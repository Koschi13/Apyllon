import vlc
import pafy

class Queue():
    def __init__(self, identifier):
        self.identifier = identifier
        self.media_list = vlc.MediaList()

    def add_local(self, filepath):
        self.media_list.add_media(filepath)

    def add_youtube(self, url):
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        self.media_list.add_media(bestaudio.url)
