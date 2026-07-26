import pygame
from utils.dependency import get_frames
from animation import Animation

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self,frames,bottomleft,direction=1):
        super().__init__()
        self.ani = Animation(frames,direction)
        self.rect = self.ani.image.get_rect()
        self.rect.bottomleft = bottomleft
        self.ishit = False

    def draw(self,screen):
        screen.blit(self.ani.image,self.rect.topleft)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('idle')
            self.ishit = False
        self.ani.update()

    def hit(self):
        if not self.ishit:
            self.ani.set_state('move')
        self.ishit = True

class Start(Checkpoint):
    frames = None
    @classmethod
    def load_assets(cls):
        if cls.frames == None:
            cls.frames = dict()
            cls.frames['idle'] = get_frames(r'assets\Items\Checkpoints\Start\Start (Idle).png',1)
            cls.frames['move'] = get_frames(r'assets\Items\Checkpoints\Start\Start (Moving) (64x64).png',17)

    def __init__(self,bottomleft,direction=1):
        Start.load_assets()
        super().__init__(Start.frames,bottomleft,direction)

class End(Checkpoint):
    frames = None
    @classmethod
    def load_assets(cls):
        if cls.frames == None:
            cls.frames = dict()
            cls.frames['idle'] = get_frames(r'assets\Items\Checkpoints\End\End (Idle).png',1)
            cls.frames['move'] = get_frames(r'assets\Items\Checkpoints\End\End (Pressed) (64x64).png',8)

    def __init__(self,bottomleft,direction=1):
        End.load_assets()
        super().__init__(End.frames,bottomleft,direction)


class Flag(Checkpoint):
    frames = None
    @classmethod
    def load_assets(cls):
        if cls.frames == None:
            cls.frames = dict()
            cls.frames['idle'] = get_frames(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (No Flag).png',1)
            cls.frames['move'] = get_frames(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Out) (64x64).png',26)
            cls.frames['active'] = get_frames(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Idle)(64x64).png',10)

    def __init__(self,bottomleft,direction=1):
        Flag.load_assets()
        super().__init__(Flag.frames,bottomleft,direction)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('active')
        self.ani.update()
        