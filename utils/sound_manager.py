import pygame
from utils.sound_effect import SoundEffect

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {}

    def add(
        self,
        name,
        file,
        volume=1.0,
        cooldown=0.0,
        speed=1.0,
        loops=0,
        single = False
    ):
        self.sounds[name] = SoundEffect(
            file=file,
            volume=volume,
            speed=speed,
            cooldown=cooldown,
            loops=loops,
            single=single
        )

    def play(self, name):
        sound = self.sounds.get(name)

        if sound:
            return sound.play()

        return False

    def stop(self, name):
        sound = self.sounds.get(name)

        if sound:
            sound.stop()

    def reset(self, name):
        sound = self.sounds.get(name)

        if sound:
            sound.reset()

    def set_volume(self, name, volume):
        sound = self.sounds.get(name)

        if sound:
            sound.set_volume(volume)

    def set_speed(self, name, speed):
        sound = self.sounds.get(name)

        if sound:
            sound.set_speed(speed)

    def set_cooldown(self, name, cooldown):
        sound = self.sounds.get(name)

        if sound:
            sound.set_cooldown(cooldown)