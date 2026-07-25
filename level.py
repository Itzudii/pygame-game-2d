import pygame
from maps import map1
from player.model import Player
from items.flag import Flag
from constant import TILESIZE,WINDOW_W,WINDOW_H

class Level():
    tilesize=TILESIZE
    def __init__(self):
        self.player = None
        self.landblocks = []
        self.flags = pygame.sprite.Group()
        self.load_map()

    def load_map(self):
        for row,lst in enumerate(map1):
            for col,tile in enumerate(lst):
                if tile == '#':
                    self.landblocks.append(pygame.Rect(col*Level.tilesize,row*Level.tilesize,Level.tilesize,Level.tilesize))
                elif tile == 'P':
                    self.player = Player(col*Level.tilesize,row*Level.tilesize)
                elif tile == 'S':
                    temp = Flag((col*Level.tilesize,(row+1)*Level.tilesize))
                    self.flags.add(temp)

    def event_handle(self,event):
        self.player.event_handle(event)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        for block in self.landblocks:
            pygame.draw.rect(screen,(255,0,0),block,1)

        for flag in self.flags:
            flag.draw(screen)

        self.player.draw(screen,"")

    def collisions(self):
        
        for flag in self.flags:
            if flag.rect.colliderect(self.player.rect) and self.player.move:
                flag.hit()
                print('hit')



    def update(self):
        self.collisions()
        self.flags.update()
        self.player.update(level=self)
        # self.camera.update(self.player)




















