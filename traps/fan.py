import random
import pygame
from animation import Animation
from pytmx_mapper.utils import get_transform_images
from utils.dependency import get_img,TILESIZE
from utils.partical import Partical
import math


class Dust(Partical):
    img = get_img(r"assets\Other\Dust Particle.png",(TILESIZE//3,TILESIZE//3))
    def __init__(self,rect,lifespan,h):
        super().__init__(lifespan)
        self.img = self.__class__.img.convert_alpha()
        self.x = random.randint(rect.left,rect.right)
        self.y = rect.y
        self.df = lifespan/h

    def draw(self,screen,camera):
        screen.blit(self.img,camera.apply_pos((self.x,self.y)))

    def update(self):
        super().update()
        self.y -= self.df
            

class Box(pygame.sprite.Sprite):
    frames = None

    @classmethod
    def load_assets(cls,data):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = {1:get_transform_images(path, count,data.size,data.transform)}

    def __init__(self,data):
        cls = self.__class__
        cls.load_assets(data)
        super().__init__()
        self.ani = Animation(cls.frames)
        self.m_rect = data.rects[0]
        self.rect = pygame.Rect(self.m_rect.x,self.m_rect.y,self.m_rect.w,self.m_rect.h)
        self.img_pos = data.pos
        self.isActive = False

        self.particals = pygame.sprite.Group()
        self.delay = 0

        self.on()


    def draw(self,screen,camera):
        screen.blit(self.ani.image,camera.apply_pos(self.img_pos))
        pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)

        for particle in self.particals:
            particle.draw(screen,camera)

    def update(self):
        self.ani.update()

        if self.isActive:
            self.delay +=1
            if self.delay > 10:
                self.particals.add(Dust(self.rect,200,100))
                self.delay = 0

            self.particals.update()

    def on(self):
        if not self.isActive:
            self.ani.set_state('active')
            self.isActive = True

    def off(self):
        if self.isActive:
            self.ani.set_state('idle')
            self.isActive = False

    def __type__(self):
        return Box

class Fan(Box):
    assets = {
            'idle':(r'assets\Traps\Fan\Off.png',1),
            'active':(r'assets\Traps\Fan\On (24x8).png',4),
        }

    