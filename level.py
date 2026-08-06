import pygame
from player.model import Player
from items.checkpoints import Start,Flag,End
from items.fruits import Bananas,Apple,Orange,Kiwi,Cherries,Pineapple,Strawberry,Melon
from items.boxs import Box1,Box2,Box3
from settings import TILESIZE,WINDOW_W,WINDOW_H
from pytmx_mapper.map import TileMap
from pytmx_mapper.layers import Layer

from bg import Blue, Brown, Gray, Green, Pink, Purple, Yellow

bg= r'assets\Background\Blue.png'
class Level():
    tilesize=TILESIZE
    def __init__(self):
        layers = {
                    "normal_tile":Layer.NORMAL,
                    "background_tile":Layer.NORMAL,
                    "collision_normal_tile":Layer.COLLIDE, 
                    "decoration_object_layer":Layer.DECORATION, 
                    "decoration_object_layer_foreground":Layer.DECORATION,
                    "object_layer":Layer.OBJECT,
                }
        self.map = TileMap('mapdata/map.tmx',layers,TILESIZE)
        self.map.resize_map((WINDOW_W,WINDOW_H))
        self.camera = self.map.camera

        self.checkpoints = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.boxs = pygame.sprite.Group()

    def load(self):
        self.map.load()
        self.colliders = self.map.colliders["collision_normal_tile"]
        self.player = Player((100,100))
        self.bg = Brown(self.map)

        for name,lst in self.map.objs['object_layer'].items():
            match (name):
                case 'start':self.checkpoints.add(*(Start(d) for d in lst)) 
                case 'flag':self.checkpoints.add(*(Flag(d) for d in lst)) 
                case 'end':self.checkpoints.add(*(End(d) for d in lst)) 

                case 'box1':self.boxs.add(*(Box1(d) for d in lst)) 
                case 'box2':self.boxs.add(*(Box2(d) for d in lst)) 
                case 'box3':self.boxs.add(*(Box3(d) for d in lst)) 

                case 'banana':self.fruits.add(*(Bananas(d) for d in lst)) 
                case 'apple':self.fruits.add(*(Apple(d) for d in lst)) 
                case 'orange':self.fruits.add(*(Orange(d) for d in lst)) 
                case 'kiwi':self.fruits.add(*(Kiwi(d) for d in lst)) 
                case 'cherrie':self.fruits.add(*(Cherries(d) for d in lst)) 
                case 'pineapple':self.fruits.add(*(Pineapple(d) for d in lst)) 
                case 'strawberry':self.fruits.add(*(Strawberry(d) for d in lst)) 
                case 'melon':self.fruits.add(*(Melon(d) for d in lst)) 


    def event_handle(self,event):
        self.player.event_handle(event)
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     print(pos)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        self.bg.draw(screen,self.camera)

        self.map.draw_layers(screen)
        self.map.draw_colliders(screen,"collision_normal_tile",(255,0,0))
    
        for flag in self.checkpoints:
            flag.draw(screen,self.camera)

        for box in self.boxs:
            box.draw(screen,self.camera)

        for fruit in self.fruits:
            fruit.draw(screen,self.camera)

        self.player.draw(screen,self.camera)


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
        self.bg.update()
        self.collisions()
        self.checkpoints.update()
        self.fruits.update()
        self.boxs.update()
        
        self.player.update(level=self)
        self.camera.focus(self.player)




















