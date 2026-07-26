import pygame
from maps import map1
from player.model import Player
from items.checkpoints import Start,End,Flag
from items.fruits import Apple
from items.boxs import Box
from constant import TILESIZE,WINDOW_W,WINDOW_H

class Level():
    tilesize=TILESIZE
    def __init__(self):
        self.player = None
        self.landblocks = []
        self.checkpoints = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.boxs = pygame.sprite.Group()
    
        self.load_map()

    def load_map(self):
        for row,lst in enumerate(map1):
            for col,tile in enumerate(lst):
                if tile == '#':
                    self.landblocks.append(pygame.Rect(col*Level.tilesize,row*Level.tilesize,Level.tilesize,Level.tilesize))
                elif tile == 'P':
                    self.player = Player(col*Level.tilesize,row*Level.tilesize)
                elif tile == 'S':
                    temp = Start((col*Level.tilesize,(row+1)*Level.tilesize))
                    self.checkpoints.add(temp)
                elif tile == 'B':
                    temp = Box((col*Level.tilesize,(row+1)*Level.tilesize))
                    self.boxs.add(temp)
                elif tile == 'F':
                    temp = Flag((col*Level.tilesize,(row+1)*Level.tilesize))
                    self.checkpoints.add(temp)
                elif tile == 'A':
                    temp = Apple((col*Level.tilesize,(row+1)*Level.tilesize))
                    self.fruits.add(temp)

    def event_handle(self,event):
        self.player.event_handle(event)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        for block in self.landblocks:
            pygame.draw.rect(screen,(255,0,0),block,1)

        for flag in self.checkpoints:
            flag.draw(screen)

        for box in self.boxs:
            box.draw(screen)

        for fruit in self.fruits:
            fruit.draw(screen)

        self.player.draw(screen,"")

    def collisions(self):
        
        for flag in self.checkpoints:
            if flag.rect.colliderect(self.player.rect) and self.player.move:
                flag.hit()
                # save coord

        for fruit in self.fruits:
            if fruit.rect.colliderect(self.player.rect):
                fruit.hit()
                #  increase points

        for box in self.boxs:
            if box.rect.colliderect(self.player.rect):
                box.get_break()
                #  increase points


    def update(self):
        self.collisions()
        self.checkpoints.update()
        self.fruits.update()
        self.boxs.update()
        self.player.update(level=self)
        # self.camera.update(self.player)




















