from ursina import *

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music = None

        self.mappa_blocchi_suoni = {'Grass_Block': 'footstep_grass','Snowy_Grass_Block': 'footstep_snow','Water_Block': 'footstep_water',
                                    'Dirt_Path_Block': 'footstep_dirt',
}

    def load_sound(self, name, path, loop=False, volume=1):
        self.sounds[name] = Audio(path, loop=loop, autoplay=False, volume=volume)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Suono '{name}' non trovato.")

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()

    def play_music(self, path, loop=True, volume=0.5):
        if self.music:
            self.music.stop()
        self.music = Audio(path, loop=loop, autoplay=True, volume=volume)

    def stop_music(self):
        if self.music:
            self.music.stop()
