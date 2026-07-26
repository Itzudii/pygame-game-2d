import pygame
from utils.dependency import get_frames
from animation import Animation

import random 
from utils.dependency import get_img

class Partical(pygame.sprite.Sprite):
    def __init__(self,lifespan):
        super().__init__()
        self.w = self.img.get_width()
        self.life = lifespan
        self.max_life = lifespan

    def update(self):
        self.life -= 1
        alpha = int(255 * (self.life / self.max_life))
        self.img.set_alpha(alpha)
        if self.life == 0:
            self.kill()





class Box(pygame.sprite.Sprite):
    frames = None
    assets = {
        'idle':(r'assets\Items\Boxes\Box1\Idle.png',1),
        'hit':(r'assets\Items\Boxes\Box1\Hit (28x24).png',3),
        'break':(r'assets\Items\Boxes\Box1\Break.png',4)
    }

    @classmethod
    def load_assets(cls):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = get_frames(path, count,both=False)

    def __init__(self,bottomleft):
        cls = self.__class__
        cls.load_assets()
        super().__init__()
        self.ani = Animation(cls.frames)
        self.break_frames = cls.frames['break'][1]
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
            self.ani.set_state('hit')
        self.ishit = True

    def get_break(self):
        pass


        