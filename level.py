import pygame
from player.model import NinjaFrog,MaskDude,PinkMan,VirtualGuy
from items.checkpoints import Start,Flag,End
from items.fruits import Bananas,Apple,Orange,Kiwi,Cherries,Pineapple,Strawberry,Melon
from items.boxs import Box1,Box2,Box3
from settings import TILESIZE,WINDOW_W,WINDOW_H
from pytmx_mapper.map import TileMap
from pytmx_mapper.layers import Layer
from player.shadow import Shadow

from bg import Blue, Brown, Gray, Green, Pink, Purple, Yellow

from traps.arrow import Arrow,Trampoline
from traps.saw import Saw, BrownP, GrayP
from traps.fan import Fan
from traps.falling_p import FallingP
from traps.fire import Fire

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
                    "traps_layer":Layer.OBJECT,
                    "paths_layer":Layer.SHAPE,
                }
        self.map = TileMap('mapdata/map.tmx',layers,TILESIZE)
        self.map.resize_map((WINDOW_W,WINDOW_H))
        self.camera = self.map.camera

        self.checkpoints = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.boxs = pygame.sprite.Group()

        self.arrows = pygame.sprite.Group()
        self.saws = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.falling_platforms = pygame.sprite.Group()
        self.fans = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        

        self.player = None
        self.bg = None

    def load_obj_layer(self):
        for name,lst in self.map.objs['object_layer'].items():
            match (name):
                # checkpoints
                case 'start':self.checkpoints.add(*(Start(d) for d in lst)) 
                case 'flag':self.checkpoints.add(*(Flag(d) for d in lst)) 
                case 'end':self.checkpoints.add(*(End(d) for d in lst)) 

                # boxs
                case 'box1':self.boxs.add(*(Box1(d) for d in lst)) 
                case 'box2':self.boxs.add(*(Box2(d) for d in lst)) 
                case 'box3':self.boxs.add(*(Box3(d) for d in lst)) 

                # players
                case 'frog':self.player = NinjaFrog(*lst)
                case 'mask':self.player = MaskDude(*lst)
                case 'pink':self.player = PinkMan(*lst)
                case 'virtual':self.player = VirtualGuy(*lst)

                # BGs
                case 'blue':self.bg = Blue(self.map)
                case 'brown':self.bg = Brown(self.map)
                case 'gray':self.bg = Gray(self.map)
                case 'green':self.bg = Green(self.map)
                case 'pink':self.bg = Pink(self.map)
                case 'purple':self.bg = Purple(self.map)
                case 'yellow':self.bg = Yellow(self.map)

                # fruits
                case 'banana':self.fruits.add(*(Bananas(d) for d in lst)) 
                case 'apple':self.fruits.add(*(Apple(d) for d in lst)) 
                case 'orange':self.fruits.add(*(Orange(d) for d in lst)) 
                case 'kiwi':self.fruits.add(*(Kiwi(d) for d in lst)) 
                case 'cherrie':self.fruits.add(*(Cherries(d) for d in lst)) 
                case 'pineapple':self.fruits.add(*(Pineapple(d) for d in lst)) 
                case 'strawberry':self.fruits.add(*(Strawberry(d) for d in lst)) 
                case 'melon':self.fruits.add(*(Melon(d) for d in lst)) 


    def load_traps_layer(self):
        for name,lst in self.map.objs['traps_layer'].items():
            match (name):
                # checkpoints
                case 'arrow':self.arrows.add(*(Arrow(d) for d in lst)) 
                case 'trampoline':self.arrows.add(*(Trampoline(d) for d in lst)) 
                case 'saw':
                    for d in lst:
                        id = d.prop.get('path')
                        path = self.map.get_obj_by_id(id)
                        points = path.points
                        self.saws.add(Saw(d,points)) 
                case 'brown_platform':
                    for d in lst:
                        id = d.prop.get('path')
                        path = self.map.get_obj_by_id(id)
                        points = path.points
                        self.platforms.add(BrownP(d,points)) 
                case 'grey_platform':
                    for d in lst:
                        id = d.prop.get('path')
                        path = self.map.get_obj_by_id(id)
                        points = path.points
                        self.platforms.add(GrayP(d,points)) 
                case 'fan':self.fans.add(*(Fan(d) for d in lst)) 
                case 'falling_platform':self.falling_platforms.add(*(FallingP(d) for d in lst)) 
                case 'fire':self.fires.add(*(Fire(d) for d in lst)) 

    def load(self):
        self.map.load()

        self.load_obj_layer()
        self.load_traps_layer()

        self.colliders = self.map.colliders["collision_normal_tile"]

        # self.player = NinjaFrog((100,100))
        # self.bg = Yellow(self.map)
        self.shadow = Shadow(self.player)






    def event_handle(self,event):
        self.player.event_handle(event)
        pass

    def key_handle(self,key):
        self.player.key_handle(key)
        pass

    def draw(self,screen):
        self.bg.draw(screen,self.camera)

        self.map.draw_layers(screen)
        # self.map.draw_colliders(screen,"collision_normal_tile",(255,0,0))
    
        for flag in self.checkpoints:
            flag.draw(screen,self.camera)

        for box in self.boxs:
            box.draw(screen,self.camera)

        for fruit in self.fruits:
            fruit.draw(screen,self.camera)

        for arrow in self.arrows:
            arrow.draw(screen,self.camera)

        for saw in self.saws:
            saw.draw(screen,self.camera)

        for platform in self.platforms:
            platform.draw(screen,self.camera)

        for fan in self.fans:
            fan.draw(screen,self.camera)

        for falling_platform in self.falling_platforms:
            falling_platform.draw(screen,self.camera)

        for fire in self.fires:
            fire.draw(screen,self.camera)

        self.player.draw(screen,self.camera)

        self.shadow.draw(screen,self.camera)


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

        for arrow in self.arrows:
            if arrow.rect.colliderect(self.player.rect):
                arrow.hit()
                self.player.jump_with_int(10)
                self.player.reset_jump()
                #  increase points
        
        for platform in self.platforms:
            rect = self.player.rect.move(0,2)
            if platform.rect.colliderect(rect):
                self.player.rect.x += platform.path.dx

        for falling_platform in self.falling_platforms:
            rect = self.player.rect.move(0,2)
            if falling_platform.rect.colliderect(rect):
                falling_platform.hit()
                self.player.reset_jump()

        for fire in self.fires:
            rect = self.player.rect.move(0,2)
            if fire.rect.colliderect(rect):
                hit = fire.hit()
                if not hit:
                    pass # player got damage 
                    print('health -1')
                else:
                    pass # fire got damage 


        


    def update(self):
        self.bg.update()
        self.collisions()
        self.checkpoints.update()
        self.fruits.update()
        self.boxs.update()
        self.arrows.update()
        self.saws.update()
        self.platforms.update()
        self.fans.update()
        self.falling_platforms.update()
        self.fires.update()
        
        self.player.update(level=self)
        self.shadow.update(self.colliders)

        self.camera.focus(self.player)




















