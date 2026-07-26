import pygame
from utils.dependency import get_frames
from animation import Animation
class Fruit(pygame.sprite.Sprite):
    frames = None
    assets = {} 
    
    @classmethod
    def load_assets(cls):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = get_frames(path, count,both= False)
            cls.frames['collect'] = get_frames(r'assets\Items\Fruits\Collected.png',6,both=False)


    def __init__(self,bottomleft):
        cls = self.__class__
        cls.load_assets()
        super().__init__()
        self.ani = Animation(cls.frames)
        self.rect = self.ani.image.get_rect()
        self.rect.bottomleft = bottomleft
        self.ishit = False

    def draw(self,screen):
        screen.blit(self.ani.image,self.rect.topleft)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.kill()
        self.ani.update()

    def hit(self):
        self.ani.set_state('collect')
        self.ishit = True

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


        