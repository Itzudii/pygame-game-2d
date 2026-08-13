import pygame
from enum import Enum
from utils.dependency import get_frames,get_img
from settings import TILESIZE
from player.effect import Appear,Disappear
from player.dust_partical import DustF,DustH,DustJ,DustV
import random
from utils.animation import Animation

class State(Enum):
    IDLE = "idle"
    RUN = "run"
    WALLJUMP = "wallJUMP"
    JUMP = "jump"
    HURT = "hurt"
    FALL = "fall"
    DJUMP = "djump"


class Player(pygame.sprite.Sprite):
    name = 'player'
    frames = None
    
    @classmethod
    def load_assets(cls):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = get_frames(path, count)

    def __init__(self,data):
        cls = self.__class__
        cls.load_assets()
        super().__init__()
    
        self.direction = 1 # (-1,left)  (1,right)
        self.animation = Animation(cls.frames)

        self.m_rect = data.rects[0]
        self.rect = pygame.Rect(self.m_rect.x,self.m_rect.y,self.m_rect.w,self.m_rect.h)

        self.speed = TILESIZE//6
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
        self.isvisible = False
        self.hitground = False

        # health
        self.max_health = 3
        self.health = self.max_health
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 90  # frames (~1.5s at 60fps)
        self.is_dead = False

        self.effects = pygame.sprite.Group()
        self.particals = pygame.sprite.Group()
        self.appearing()


    def draw(self,screen,camera):
        if self.isvisible and len(self.effects) == 0:
            screen.blit(self.animation.image,camera.apply_pos((self.rect.x-self.m_rect.dif_x,self.rect.y-self.m_rect.dif_y)))

        for partical in self.particals:
            partical.draw(screen,camera)

        for effect in self.effects:
            effect.draw(screen,camera)


    def update_state(self):
        if self.is_hit:
            self.animation.set_state(State.HURT.value)
            if self.animation.isfinished:
                self.is_hit = False
        elif self.isdoublej:
            self.animation.set_state(State.DJUMP.value)
            if self.animation.isfinished:
                self.isdoublej = False
        elif self.isjumped:
            self.animation.set_state(State.JUMP.value)
        elif self.isfall:
            if self.iscollide_left or self.iscollide_right:
                self.animation.set_state(State.WALLJUMP.value)
                self.vel_y = 1
                self.doublejumpuse = False
            else:
                self.animation.set_state(State.FALL.value)
        elif not self.move:
            self.animation.set_state(State.IDLE.value)
        else:
            self.animation.set_state(State.RUN.value)

    def movement_y(self):
        self.vel_y += self.gravity
        self.rect.y += round(self.vel_y)

    def collision_check_y_axis(self,level):
        foot = self.rect.move(0, 2)

        def collision_check_y_axis_objs(objs):
            resolved = False
            for obj in objs:
                if self.rect.colliderect(obj.rect):
                    if self.isjumped:
                        self.rect.top = obj.rect.bottom + 1
                        self.isdoublej = False
                    else:
                        self.rect.bottom = obj.rect.top
                        if not self.hitground:
                            self.hitground = True
                            for _ in range(5):
                                self.particals.add(DustF(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
                    self.vel_y = 0
                    resolved = True
            # Recheck grounded using updated position
            grounded = resolved or any(foot.colliderect(obj.rect) for obj in objs)
            return grounded

        self.isjumped = self.vel_y < 0
        grounded = (
            collision_check_y_axis_objs(level.colliders) |
            collision_check_y_axis_objs(level.boxs) |
            collision_check_y_axis_objs(level.platforms) |
            collision_check_y_axis_objs(level.falling_platforms) |
            collision_check_y_axis_objs(level.fires)
        )

        self.isfall = not grounded
        if self.isfall:
            self.hitground = False

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

        def tile_collision(block):
            if self.rect.colliderect(block):
                if self.speed_dt < 0:
                    self.rect.left = block.right
                    self.iscollide_left = True
                elif self.speed_dt > 0:
                    self.rect.right = block.left
                    self.iscollide_right = True

        for collider in level.colliders:
            tile_collision(collider.rect)

        for box in level.boxs:
            tile_collision(box.rect)

        for platform in level.platforms:
            tile_collision(platform.rect)

        for falling_platform in level.falling_platforms:
            tile_collision(falling_platform.rect)

        for fire in level.fires:
            tile_collision(fire.rect)

    def reset_jump(self):
        self.isjumped = False
        self.isdoublej = False
        self.doublejumpuse = False

    def update(self,level):
        self.animation.direction = self.direction
        self.animation.update()

        self.movement_y() #y-axis movement
        self.collision_check_y_axis(level) #y-axis collision

        self.movement_x() #x-axis movement
        self.collision_check_x_axis(level) #y-axis collision

        self.update_state() 
        self.summon_partical()

        self.effects.update()
        self.particals.update()

        # Invincibility countdown + blink

        if self.invincible and not self.is_dead:
            self.invincible_timer -= 1
            # blink every 6 frames
            self.isvisible = (self.invincible_timer // 6) % 2 == 0
            if self.invincible_timer <= 0:
                self.invincible = False
                self.isvisible = True


    def event_handle(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()
                self.particals.add(DustJ(self.rect.centerx,self.rect.bottom,random.randint(20,40),50))
            if event.key == pygame.K_q:
                self.take_damage()
            if event.key == pygame.K_a:
                if self.isvisible:
                    self.desappearing()
                else:
                    self.appearing()

                        
    def appearing(self):
        self.effects.add(Appear(self.rect.centerx,self.rect.centery,self.direction))
        self.isvisible = True

    def desappearing(self):
        self.effects.add(Disappear(self.rect.centerx,self.rect.centery,self.direction))
        self.isvisible = False

    def teleport(self,coord):
        if self.animation.finished and self.isvisible:
            self.desappearing()
            print('dis')
        elif self.animation.finished and not self.isvisible:
            print('apper')
            self.restore()
            self.rect.center = coord
            self.appearing()
        

                    
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

    def jump_with_int(self,intensity=0):
            if intensity>0:
                self.vel_y = -intensity
            else:
                self.vel_y = -self.jump_intensity

    def take_damage(self, amount=1):
        """Reduce player health; triggers hurt animation and invincibility frames."""
        if self.invincible or self.is_dead:
            return
        self.health = max(0, self.health - amount)
        self.is_hit = True
        self.invincible = True
        self.invincible_timer = self.invincible_duration
        if self.health <= 0:
            self.is_dead = True

    def restore(self):
        self.health = self.max_health
        self.is_dead = False

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


