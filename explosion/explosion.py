# https://craftpix.net/freebies/11-free-pixel-art-explosion-sprites/

import pygame
from utils.animation import Animation

class Explosion(pygame.sprite.Sprite):
    def __init__(self,lst,x,y):
        super().__init__()
        self.frames = [pygame.image.load(url) for url in lst]
        self.ani = Animation(self.frames,1,False)
        self.x = x-(self.frames[0].get_width()//2)
        self.y = y-(self.frames[0].get_height()//2)

    def update(self,screen):
        screen.blit(self.ani.image,(self.x,self.y))
        self.ani.update()
        if self.ani.finished:
            self.kill()

class Wave(pygame.sprite.Sprite):
    def __init__(self,lst,x,y):
        super().__init__()
        self.frames = [pygame.image.load(url) for url in lst]
        self.ani = Animation(self.frames,1,True)
        self.x = x-(self.frames[0].get_width()//2)
        self.y = y-(self.frames[0].get_height()//2)


    def update(self,screen):
        screen.blit(self.ani.image,(self.x,self.y))
        self.ani.update()


