import pygame
from utils.dependency import get_frames
from animation import Animation

import random 
from utils.partical import Partical


class Fragment(Partical):
    def __init__(self,img,x,y,lifespan,h):
        super().__init__(lifespan)
        self.img = img.convert_alpha()
        self.w = self.img.get_width()
        self.x = x
        self.y = y
        self.df = lifespan/h
        self.speed = random.choice((2,-2))
        
    def draw(self,screen):
        screen.blit(self.img,(self.x-self.w//2,self.y-self.w//2))

    def update(self):
        super().update()
        if self.life >= self.max_life/2:
            self.y -= self.df
        else:
            self.y += self.df

        self.x += self.speed

    







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
        self.img_rect = self.ani.image.get_rect()
        self.img_rect.bottomleft = bottomleft
        self.rect = self.img_rect.copy()
        self.ishit = False
        self.fragments = pygame.sprite.Group()

    def draw(self,screen):
        screen.blit(self.ani.image,self.img_rect.topleft)
        pygame.draw.rect(screen,(255,0,0),self.rect,1)

        for frag in self.fragments:
            frag.draw(screen)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('idle')
            self.ishit = False
        self.ani.update()

        self.fragments.update()

    def hit(self):
        if not self.ishit:
            self.ani.set_state('hit')
        self.ishit = True

    def get_break(self):
        if len(self.fragments) < 4:
            idx = random.randint(0,3)
            temp = Fragment(self.break_frames[idx],random.randint(self.rect.left,self.rect.right),random.randint(self.rect.top,self.rect.bottom),20,50)
            self.fragments.add(temp)

    def __type__(self):
        return Box

        