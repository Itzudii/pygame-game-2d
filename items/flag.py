import pygame
from utils.dependency import get_frames
from animation import Animation

class Flag(pygame.sprite.Sprite):
    frames = None
    
    @classmethod
    def load_assets(cls):
        if cls.frames == None:
            cls.frames = dict()
            cls.frames['idle'] = get_frames(r'assets\Items\Checkpoints\Start\Start (Idle).png',1)
            cls.frames['move'] = get_frames(r'assets\Items\Checkpoints\Start\Start (Moving).png',17)

    def __init__(self,bottomleft,direction=1):
        super().__init__()
        Flag.load_assets()

        self.bottomleft = bottomleft
        self.ani = Animation(Flag.frames,direction)
        self.rect = self.ani.image.get_rect()
        self.ishit = False

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('idle')
            self.ishit = False
        self.ani.update()

    def hit(self):
        self.ishit = True

