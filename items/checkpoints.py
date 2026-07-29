import pygame
from utils.dependency import get_frames
from animation import Animation

class Checkpoint(pygame.sprite.Sprite):
    frames = None
    assets = {} 

    @classmethod
    def load_assets(cls):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = get_frames(path, count)

    def __init__(self,bottomleft,direction=1):
        cls = self.__class__
        cls.load_assets()
        super().__init__()
        self.ani = Animation(cls.frames,direction)
        self.img_rect = self.ani.image.get_rect()
        self.img_rect.bottomleft = bottomleft
        self.rect = self.img_rect.copy()
        self.ishit = False

    def draw(self,screen):
        screen.blit(self.ani.image,self.img_rect.topleft)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('idle')
            self.ishit = False
        self.ani.update()

    def hit(self):
        if not self.ishit:
            self.ani.set_state('move')
        self.ishit = True

    def __type__(self):
        return Checkpoint

class Start(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\Start\Start (Idle).png',1),
        'move':(r'assets\Items\Checkpoints\Start\Start (Moving) (64x64).png',17)
    } 

class End(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\End\End (Idle).png',1),
        'move':(r'assets\Items\Checkpoints\End\End (Pressed) (64x64).png',8)
    } 


class Flag(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (No Flag).png',1),
        'move':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Out) (64x64).png',26),
        'active':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Idle)(64x64).png',10)
    } 

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('active')
        self.ani.update()
        