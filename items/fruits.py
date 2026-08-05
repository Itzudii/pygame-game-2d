import pygame
from pytmx_mapper.utils import get_transform_images

from animation import Animation
class Fruit(pygame.sprite.Sprite):
    frames = None
    assets = {} 
    
    @classmethod
    def load_assets(cls,data):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = {1:get_transform_images(path, count,data.size,data.transform)}
            cls.frames['collect'] = {1:get_transform_images(r'assets\Items\Fruits\Collected.png',6,data.size,data.transform)}


    def __init__(self,data):
        cls = self.__class__
        cls.load_assets(data)
        super().__init__()
        self.ani = Animation(cls.frames)
        self.img_rect = self.ani.image.get_rect()
        self.img_rect.topleft = data.pos
        self.rects = [pygame.Rect(rect.x,rect.y,rect.w,rect.h) for rect in data.rects]
        self.rect = self.rects[0]
        self.ishit = False

    def draw(self,screen,camera):
        screen.blit(self.ani.image,camera.apply_pos(self.img_rect.topleft))

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.kill()
        self.ani.update()

    def hit(self):
        self.ani.set_state('collect')
        self.ishit = True

    def __type__(self):
        return Fruit

class Apple(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Apple.png',17)} 

class Bananas(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Bananas.png',17)} 

class Cherries(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Cherries.png',17)} 

class Kiwi(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Kiwi.png',17)} 

class Melon(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Melon.png',17)} 

class Orange(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Orange.png',17)} 

class Pineapple(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Pineapple.png',17)} 

class Strawberry(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Strawberry.png',17)} 


        