import pygame
from maps import map1
from player.model import Player
from items.checkpoints import Start,End,Flag,Checkpoint
from items.fruits import Apple,Fruit
from items.boxs import Box
from constant import TILESIZE,BASESIZE
import json
from tmj.tiledraw import TileDraw

def get_obj(name:str):
    name_to_obj = {
        'apple':Apple,
        'box':Box,
        'flag':Flag,
        'end':End,
        'player':Player,
        'start':Start,
    }

    return name_to_obj.get(name)

class Level():
    tilesize=TILESIZE
    def __init__(self):
        self.map = TileDraw('tiled/map_final.tmj')
        self.landblocks = [pygame.Rect(pos[0],pos[1],TILESIZE,TILESIZE) for img,pos in self.map.collision_tiles]

        self.player = None
        self.checkpoints = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.boxs = pygame.sprite.Group()

        self.load_map()

    
    def load_map(self):

        def update_collision_rect(obj,rect):
            ratio = TILESIZE/BASESIZE
            obj.rect.x += int(rect['x'])*ratio
            obj.rect.y += int(rect['y'])*ratio
            obj.rect.w = int(rect['width'])*ratio
            obj.rect.h = int(rect['height'])*ratio
            return obj


        for gid,name,pos in self.map.objs:
            ref = get_obj(name)
            if ref:
                obj = ref((pos[0]*TILESIZE//16,pos[1]*TILESIZE//16))
                rect = self.map.get_collision_rect(gid)
                if rect:
                    obj = update_collision_rect(obj,rect)
                if isinstance(obj,Player):
                    self.player = obj
                elif isinstance(obj,Fruit):
                    self.fruits.add(obj)
                elif isinstance(obj,Checkpoint):
                    self.checkpoints.add(obj)
                elif isinstance(obj,Box):
                    self.boxs.add(obj)

    def event_handle(self,event):
        self.player.event_handle(event)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        self.map.draw_layers(screen)

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




















