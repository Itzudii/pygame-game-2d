import pygame
from pytmx_mapper.map import TileMap
from pytmx_mapper.layers import Layer

from settings import TILESIZE,WINDOW_W,WINDOW_H

from player.baseclass import NinjaFrog,MaskDude,PinkMan,VirtualGuy
from player.hud import HealthBar
from player.shadow import Shadow

from items.checkpoints.start import Start
from items.checkpoints.end import End
from items.checkpoints.flag import Flag

from items.fruits.baseclass import Bananas,Apple,Orange,Kiwi,Cherries,Pineapple,Strawberry,Melon
from items.boxs.baseclass import Box1,Box2,Box3
from background.baseclass import Blue, Brown, Gray, Green, Pink, Purple, Yellow

from traps.arrow import Arrow
from traps.trampoline import Trampoline
from traps.brown import BrownP
from traps.gray import GrayP

from traps.saw import Saw
from traps.fan import Fan
from traps.falling_p import FallingP
from traps.fire import Fire
from traps.spike import Spike

from utils.sound_manager import SoundManager

class Level():
    def __init__(self,map_name):
        layers = {
                    "normal_tile":Layer.NORMAL,
                    "background_tile":Layer.NORMAL,
                    "collision_normal_tile":Layer.COLLIDE, 
                    "decoration_object_layer":Layer.DECORATION, 
                    "decoration_object_layer_foreground":Layer.DECORATION,
                    "object_layer":Layer.OBJECT,
                    "traps_layer":Layer.OBJECT,
                    "paths_layer":Layer.SHAPE,
                    "buttons":Layer.OBJECT,
                }
        self.map = TileMap(map_name,layers,TILESIZE)
        self.map.resize_map((WINDOW_W,WINDOW_H))
        self.camera = self.map.camera

        self.boxs = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()

        self.saws = pygame.sprite.Group()
        self.fans = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.falling_platforms = pygame.sprite.Group()
        
        self.player = None
        self.start = None
        self.end = None
        self.bg = None

        self.collide_flags_lst = []
        self.save_checkpoints_lst = []

        self.sound = SoundManager()
        self.iscompleted = False

    def load_obj_layer(self):
        for name,lst in self.map.objs['object_layer'].items():
            match (name):
                # checkpoints
                case 'start':self.start = Start(*lst)
                case 'flag':self.checkpoints.add(*(Flag(d) for d in lst)) 
                case 'end':self.end = End(*lst)

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

    def save_checkpoints(self,flag):
        if flag not in self.collide_flags_lst:
            self.collide_flags_lst.append(flag)
            self.save_checkpoints_lst.append(self.player.rect.center)
            self.sound.play('checkpoint')

    def load_traps_layer(self):
        def get_points(d):
            id = d.prop.get('path')
            path = self.map.get_obj_by_id(id)
            return path.points

        for name,lst in self.map.objs['traps_layer'].items():
            match (name):
                # checkpoints
                case 'fan':self.fans.add(*(Fan(d) for d in lst)) 
                case 'fire':self.fires.add(*(Fire(d) for d in lst)) 
                case 'spike':self.spikes.add(*(Spike(d) for d in lst)) 
                case 'arrow':self.arrows.add(*(Arrow(d) for d in lst)) 
                case 'saw':self.saws.add(*(Saw(d,get_points(d)) for d in lst)) 
                case 'trampoline':self.arrows.add(*(Trampoline(d) for d in lst)) 
                case 'falling_platform':self.falling_platforms.add(*(FallingP(d) for d in lst)) 
                case 'grey_platform':self.platforms.add(*(GrayP(d,get_points(d)) for d in lst)) 
                case 'brown_platform':self.platforms.add(*(BrownP(d,get_points(d)) for d in lst)) 

    def load(self):
        self.map.load()

        self.load_obj_layer()
        self.load_traps_layer()

        self.colliders = self.map.colliders["collision_normal_tile"]
        if self.player:
            self.save_checkpoints_lst.append(self.player.rect.center)

            self.shadow = Shadow(self.player)
            self.health = HealthBar(self.player)


        # self.sound.add('checkpoint','sound/checkpoint.mp3')
        # self.sound.add('collect','sound/collect.mp3')
        # self.sound.add('wind','sound/wind.mp3',volume=0.5,loops=-1,single=True)
        # self.sound.add('spring','sound/spring.mp3')
        # self.sound.add('cart','sound/gear.mp3',loops=-1,single=True)

    def event_handle(self,event):
        if self.player:
            self.player.event_handle(event)
        pass

    def key_handle(self,key):
        if self.player:
            self.player.key_handle(key)
        pass

    def draw(self,screen):
        self.bg.draw(screen,self.camera)

        self.map.draw_layers(screen)
    
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

        for spike in self.spikes:
            spike.draw(screen,self.camera)
        if self.player:
            self.start.draw(screen,self.camera)
            self.end.draw(screen,self.camera)
            self.player.draw(screen,self.camera)

            self.shadow.draw(screen,self.camera)
            self.health.draw(screen)


    def collisions(self):
        
        if self.start.rect.colliderect(self.player.rect) and self.player.move:
            self.start.hit()

        if self.end.rect.colliderect(self.player.rect) and self.player.move:
            self.end.hit()
            self.iscompleted = True
            # self.save_checkpoints(flag)

        for flag in self.checkpoints:
            if flag.rect.colliderect(self.player.rect) and self.player.move:
                flag.hit()
                self.save_checkpoints(flag)
                
                # save coord

        for fruit in self.fruits:
            if fruit.rect.colliderect(self.player.rect):
                fruit.hit()
                self.sound.play('collect')

                #  increase points

        for box in self.boxs:
            if box.rect.colliderect(self.player.rect):
                box.get_break()

        for arrow in self.arrows:
            if arrow.rect.colliderect(self.player.rect):
                arrow.hit()
                self.player.jump_with_int(10)
                self.player.reset_jump()
                self.sound.play('spring')

        for spike in self.spikes:
            if spike.rect.colliderect(self.player.rect):
                self.player.take_damage()
        
        i = False 
        for platform in self.platforms:
            rect = self.player.rect.move(0,2)
            if platform.rect.colliderect(rect):
                self.player.rect.x += platform.path.dx
                self.sound.play('cart')
                i = True
        if not i:
            self.sound.stop('cart')
                
        for falling_platform in self.falling_platforms:
            rect = self.player.rect.move(0,2)
            if falling_platform.rect.colliderect(rect):
                falling_platform.hit()
                self.player.reset_jump()

        # --- Saw: always spinning, damages on any body contact ---
        for saw in self.saws:
            if saw.isActive and saw.rect.colliderect(self.player.rect):
                self.player.take_damage()

        # --- Fire: damages only when the flame is active (not during off phase) ---
        for fire in self.fires:
            rect = self.player.rect.move(0,2)
            if fire.isActive and fire.rect.colliderect(rect):
                self.player.take_damage()

        # --- Fan: levitate the player when inside the wind column above the fan ---
        i = False
        for fan in self.fans:
            islevitate = fan.levitate(self.player)
            if islevitate:
                self.sound.play('wind')
                i = True
        if not i:
            self.sound.stop('wind')
            

    def update(self):
        self.bg.update()
        self.checkpoints.update()
        self.fruits.update()
        self.boxs.update()
        self.arrows.update()
        self.saws.update()
        self.platforms.update()
        self.fans.update()
        self.falling_platforms.update()
        self.fires.update()
        
        if self.player:
            self.collisions()
            self.start.update()
            self.end.update()
            self.player.update(level=self)
            self.shadow.update(self.colliders)

            self.camera.focus(self.player)

            if self.player.is_dead:
                self.player.teleport(self.save_checkpoints_lst[-1])
                # self.player.restore()




















