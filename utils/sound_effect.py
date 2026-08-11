import pygame
import time


class SoundEffect:

    def __init__(
        self,
        file,
        volume=1.0,
        speed=1.0,
        cooldown=0.0,
        loops=0,
        single=False
    ):
        self.sound = pygame.mixer.Sound(file)

        self.volume = volume
        self.speed = speed
        self.cooldown = cooldown
        self.loops = loops
        self.single = single

        self.last_play_time = -float("inf")

        self.channel = None
        self.playing = False

    def can_play(self):
        return (
            time.time() - self.last_play_time
            >= self.cooldown
        )

    def play(self):

        # Don't overlap if this is a single-instance sound
        if self.single and self.playing:
            return False

        # Cooldown
        if not self.can_play():
            return False

        self.sound.set_volume(self.volume)

        channel = self.sound.play(
            loops=self.loops
        )

        if channel is None:
            return False

        self.last_play_time = time.time()

        if self.single:
            self.channel = channel
            self.playing = True

        return True

    def stop(self):

        if self.channel:
            self.channel.stop()

        self.channel = None
        self.playing = False

    def reset(self):

        self.stop()
        self.last_play_time = -float("inf")

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))

    def set_speed(self, speed):
        self.speed = speed

    def set_cooldown(self, cooldown):
        self.cooldown = cooldown