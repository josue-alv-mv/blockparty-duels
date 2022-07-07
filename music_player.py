from email import message
import pygame as pg
import os
import random

class MusicPlayer:
    def __init__(self, musics_folder_url):
        self.musics_folder_url = musics_folder_url
        self.musics = [music for music in os.listdir(musics_folder_url)]
        self.current_music = None
        pg.mixer.music.set_endevent(pg.USEREVENT)
        
    def play_random(self):
        self.current_music = random.choice(
            [music for music in self.musics if music != self.current_music]
        )
        pg.mixer.music.load(self.musics_folder_url + self.current_music)
        pg.mixer.music.play()

    def play_music(self, name):
        self.current_music = name
        pg.mixer.music.load(self.musics_folder_url + self.current_music)
        pg.mixer.music.play()

    def pause(self):
        pg.mixer.music.pause()

    def unpause(self):
        pg.mixer.music.unpause()

    def get_current_music_without_extension(self):
        return self.current_music.split(".")[0] if self.current_music is not None else "?"

    def send_json(self, network):
        network.send(tag="music", message=self.current_music)