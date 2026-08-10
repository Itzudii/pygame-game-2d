import pygame
from animation import Animation
from pytmx_mapper.utils import get_transform_images

class Box(pygame.sprite.Sprite):
    frames = None

    @classmethod
    def load_assets(cls,data):
        if cls.frames is None:
            cls.frames = {}
            for state, (path, count) in cls.assets.items():
                cls.frames[state] = {1:get_transform_images(path, count,data.size,data.transform)}

    def __init__(self,data):
        cls = self.__class__
        cls.load_assets(data)
        super().__init__()

        self.ani = Animation(cls.frames)
        # self.ani.animation_speed = 
        self.m_rect = data.rects[0]
        self.rect = pygame.Rect(self.m_rect.x,self.m_rect.y,self.m_rect.w,self.m_rect.h)
        self.isActive = False
        self.ishit = False
        self.on()
        self.timer = 0

    def draw(self,screen,camera):
        screen.blit(self.ani.image,camera.apply_pos((self.rect.x-self.m_rect.dif_x,self.rect.y-self.m_rect.dif_y)))
        pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.off()
            self.ishit = False
        

        self.timer +=1
        if self.timer >= 100:
            if self.isActive :
                self.off()
                self.isActive = False
            else:
                self.on ()
                self.isActive = True
            self.timer = 0

        self.ani.update()
        
    def on(self):
        if not self.isActive:
            self.ani.set_state('active')
            self.isActive = True

    def off(self):
        if self.isActive:
            self.ani.set_state('idle')
            self.isActive = False

    def hit(self):
        if not self.isActive:
            self.ani.set_state('hit')
            self.ishit = True
            return True
        return False
        

    def __type__(self):
        return Box

class Fire(Box):
    assets = {
            'idle':(r'assets\Traps\Fire\Off.png',1),
            'active':(r'assets\Traps\Fire\On (16x32).png',3),
            'hit':(r'assets\Traps\Fire\Hit (16x32).png',4),
        }
    