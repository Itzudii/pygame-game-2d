import pygame
from maps import map1
from player.model import Player
from constant import TILESIZE,WINDOW_W,WINDOW_H

class Level():
    tilesize=TILESIZE
    def __init__(self):
        self.player = None
        self.landblocks = []
        self.objects = pygame.sprite.Group()
        self.load_map()

    def load_map(self):
        for row,lst in enumerate(map1):
            for col,tile in enumerate(lst):
                if tile == '#':
                    self.landblocks.append(pygame.Rect(col*Level.tilesize,row*Level.tilesize,Level.tilesize,Level.tilesize))
                elif tile == 'P':
                    self.player = Player(col*Level.tilesize,row*Level.tilesize)
                    self.objects.add(self.player)
                    print(col*Level.tilesize,row*Level.tilesize)
                elif tile == 'P':
                    self.player = Player(col*Level.tilesize,row*Level.tilesize)
                    self.objects.add(self.player)
                    print(col*Level.tilesize,row*Level.tilesize)

    def event_handle(self,event):
        self.player.event_handle(event)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        for block in self.landblocks:
            pygame.draw.rect(screen,(255,0,0),block,1)

        for object in self.objects:
            object.draw(screen,"")

    def update(self):
        self.objects.update(level=self)
        # self.camera.update(self.player)




















