import random 
import pygame
from utils.dependency import get_img
class Partical(pygame.sprite.Sprite):
    frame = get_img(r"assets\Other\Dust Particle.png",(10,10))
    def __init__(self,lifespan):
        super().__init__()
        self.frame = Partical.frame.convert_alpha()
        self.w = self.frame.get_width()
        self.life = lifespan
        self.max_life = lifespan

    def update(self):
        self.life -= 1
        alpha = int(255 * (self.life / self.max_life))
        self.frame.set_alpha(alpha)
        if self.life == 0:
            self.kill()



class DustH(Partical):
    def __init__(self,x,y,lifespan,h):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.df = lifespan/h

    def draw(self,screen):
        screen.blit(self.frame,(self.x-self.w//2,self.y-self.w//2))

    def update(self):
        super().update()
        if self.life >= self.max_life/2:
            self.y -= self.df
        else:
            self.y += self.df

class DustJ(Partical):
    def __init__(self,x,y,lifespan,h):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.df = lifespan/h

    def draw(self,screen):
        screen.blit(self.frame,(self.x-self.w//2,self.y-self.w//2))

    def update(self):
        super().update()
    
        self.y -= 1
        

class DustF(Partical):
    def __init__(self,x,y,lifespan,h):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.df = lifespan/h
        self.speed = random.choice((2,-2))

    def draw(self,screen):
        screen.blit(self.frame,(self.x-self.w//2,self.y-self.w//2))

    def update(self):
        super().update()
        if self.life >= self.max_life/2:
            self.y -= self.df
        else:
            self.y += self.df

        self.x += self.speed
            
class DustV(Partical):
    def __init__(self,x,y,lifespan):
        super().__init__(lifespan)
        self.x = x
        self.y = y
        self.vel_y = 0
        self.gravity = .3

        self.direction = random.choice((1,-1))
        self.vel_x = self.x
        self.speed = random.random()

    def draw(self,screen):
        screen.blit(self.frame,(self.x-self.w//2,self.y-self.w//2))

    def update(self):
        super().update()
        self.vel_y += self.gravity
        self.y += self.vel_y

        if self.direction == -1:
            self.vel_x += self.speed
            self.x = round(self.vel_x)
        elif self.direction == 1:
            self.vel_x -= self.speed
            self.x = round(self.vel_x)
