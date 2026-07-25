import pygame
from enum import Enum
from utils.dependency import get_frames,get_img
from constant import TILESIZE
from player.effect import Appear,Disappear
import random

class State(Enum):
    IDLE = "idle"
    RUN = "run"
    WALLJUMP = "wallJUMP"
    JUMP = "jump"
    HURT = "hurt"
    FALL = "fall"
    DJUMP = "djump"

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


class Player(pygame.sprite.Sprite):
    frames = None
    scale_value = (TILESIZE,TILESIZE)
    appear = (TILESIZE*3,TILESIZE*3)
    
    
    @classmethod
    def load_assets(cls):
        if cls.frames == None:

            cls.frames = dict()
            cls.frames['idle'] = get_frames(r'assets\Main Characters\Ninja Frog\Idle (32x32).png',11,scale_factor=cls.scale_value)
            cls.frames['run'] = get_frames(r'assets\Main Characters\Ninja Frog\Run (32x32).png',12,scale_factor=cls.scale_value)
            cls.frames['wallJUMP'] = get_frames(r'assets\Main Characters\Ninja Frog\Wall Jump (32x32).png',5,scale_factor=cls.scale_value)
            cls.frames['jump'] = get_frames(r'assets\Main Characters\Ninja Frog\Jump (32x32).png',1,scale_factor=cls.scale_value)
            cls.frames['hurt'] = get_frames(r'assets\Main Characters\Ninja Frog\Hit (32x32).png',7,scale_factor=cls.scale_value)
            cls.frames['fall'] = get_frames(r'assets\Main Characters\Ninja Frog\Fall (32x32).png',1,scale_factor=cls.scale_value)
            cls.frames['djump'] = get_frames(r'assets\Main Characters\Ninja Frog\Double Jump (32x32).png',6,scale_factor=cls.scale_value)
            cls.frames['appear'] = get_frames(r'assets\Main Characters\Ninja Frog\Double Jump (32x32).png',6,scale_factor=cls.scale_value)
            cls.frames['desappear'] = get_frames(r'assets\Main Characters\Ninja Frog\Double Jump (32x32).png',6,scale_factor=cls.scale_value)

    def __init__(self,x,y):
        super().__init__()
        Player.load_assets()
        self.state = State.IDLE.value
    
        self.current = Player.frames[self.state]

        # animation
        self.animation_speed = .3
        self.idx = 0
        self.idx_f = 0
        self.isfinished = False

        self.direction = 1 # (-1,left)  (1,right)

        self.rect:pygame.Rect = self.current[1][0].get_rect()
        self.offset_x = TILESIZE//5
        self.rect.topleft = (x,y)
        self.rect.w -= self.offset_x*2
        self.speed = 3
        self.speed_dt = 0
        self.move = False

        self.iscollide_left = False
        self.iscollide_right = False

        # gravity and jump
        self.vel_y = 0
        self.gravity = .3
        self.jump_intensity = 10

        self.isjumped = False
        self.isfall = False
        self.isdoublej = False
        self.doublejumpuse = False
        
        self.is_hit = False
        self.isvisible = True
        self.hitground = False

        self.effects = pygame.sprite.Group()
        self.particals = pygame.sprite.Group()

        
    def animation_loop(self):
        self.idx_f += self.animation_speed
        self.idx = int(self.idx_f)

        if self.idx >= len(self.current[self.direction]):
            self.idx = 0
            self.idx_f = 0
            self.isfinished = True
        else:
            self.isfinished = False

    def draw(self,screen,camera):
        if self.isvisible and len(self.effects) == 0:
            screen.blit(self.current[self.direction][self.idx],(self.rect.x-self.offset_x,self.rect.y))
        # pygame.draw.rect(screen,(255,0,0),self.rect,1)

        for partical in self.particals:
            partical.draw(screen)

        for effect in self.effects:
            effect.draw(screen)

    def set_state(self,state):
        # print(state.value)
        if self.state != state.value:
            self.state = state.value
            self.idx = 0
            self.idx_f = 0
            self.current = Player.frames[self.state]

    def update_state(self):
        if self.is_hit:
            self.set_state(State.HURT)
            if self.isfinished:
                self.is_hit = False
        elif self.isdoublej:
            self.set_state(State.DJUMP)
            if self.isfinished:
                self.isdoublej = False
        elif self.isjumped:
            self.set_state(State.JUMP)
        elif self.isfall:
            if self.iscollide_left or self.iscollide_right:
                self.set_state(State.WALLJUMP)
                self.vel_y = 1
                self.doublejumpuse = False
            else:
                self.set_state(State.FALL)
        elif not self.move:
            self.set_state(State.IDLE)
        else:
            self.set_state(State.RUN)

    def movement_y(self):
        self.vel_y += self.gravity
        self.rect.y += round(self.vel_y)

    def collision_check_y_axis(self,level):
        
        foot = self.rect.move(0, 1)
        grounded = any(foot.colliderect(block) for block in level.landblocks)
        self.isjumped = self.vel_y < 0
        self.isfall = not grounded

        for block in level.landblocks:
            if self.rect.colliderect(block):
                if self.isjumped:
                    self.rect.top = block.bottom
                    self.isdoublej = False
                else:
                    self.rect.bottom = block.top
                    if not self.hitground:
                        self.hitground = True
                        for _ in range(5):
                            self.particals.add(DustF(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
                self.vel_y = 0
        if self.isfall:
            self.hitground = False
            # self.particals.add(DustJ(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))

            


    def movement_x(self):
        self.rect.x += self.speed_dt

    def summon_partical(self):
        if len(self.particals) < 5:
            if self.move and not self.isfall:
                self.particals.add(DustH(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
            if self.iscollide_left:
                self.particals.add(DustV(self.rect.x,self.rect.bottom,random.randint(20,30)))
            elif self.iscollide_right:
                self.particals.add(DustV(self.rect.right,self.rect.bottom,random.randint(20,30)))
                


    def collision_check_x_axis(self,level):
        self.iscollide_right = False
        self.iscollide_left = False

        for block in level.landblocks:
            if self.rect.colliderect(block):
                if self.speed_dt < 0:
                    self.rect.left = block.right
                    self.iscollide_left = True
                elif self.speed_dt > 0:
                    self.rect.right = block.left
                    self.iscollide_right = True
                

            
    def update(self,level):
        self.animation_loop()

        self.movement_y() #y-axis movement
        self.collision_check_y_axis(level) #y-axis collision

        self.movement_x() #x-axis movement
        self.collision_check_x_axis(level) #y-axis collision

        self.update_state() 
        self.summon_partical()

        self.effects.update()
        self.particals.update()

    def event_handle(self,event):
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jump()
                        self.particals.add(DustJ(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
                    if event.key == pygame.K_q:
                        self.is_hit = True
                    if event.key == pygame.K_a:
                        if self.isvisible:
                            self.desappearing()
                            print('disapper')
                        else:
                            self.appearing()
                            print('apper')

                        
    def appearing(self):
        self.effects.add(Appear(self.rect.centerx,self.rect.centery,self.direction))
        self.isvisible = True

    def desappearing(self):
        self.effects.add(Disappear(self.rect.centerx,self.rect.centery,self.direction))
        self.isvisible = False

                    
    def key_handle(self,key):
        if key[pygame.K_LEFT]:
            self.left()
        elif key[pygame.K_RIGHT]:
            self.right()
        else:
            self.ideal()

    def jump(self):
        if not self.isjumped and not self.isfall:
            self.vel_y = -self.jump_intensity
            self.isjumped = True
            self.doublejumpuse = False
        elif not self.isdoublej and not self.doublejumpuse:
            self.vel_y = -self.jump_intensity
            self.isdoublej = True
            self.doublejumpuse = True

    def left(self):
        self.speed_dt = -self.speed
        self.direction = -1
        self.move = True

    def right(self):
        self.speed_dt = self.speed
        self.direction = 1
        self.move = True

    def ideal(self):
        self.move = False
        self.speed_dt = 0
