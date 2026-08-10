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
        self.m_rect = data.rects[0]
        self.rect = pygame.Rect(self.m_rect.x,self.m_rect.y,self.m_rect.w,self.m_rect.h)
        self.isActive = False
        self.ishit = False
        self.on()

    def draw(self,screen,camera):
        screen.blit(self.ani.image,camera.apply_pos((self.rect.x-self.m_rect.dif_x,self.rect.y-self.m_rect.dif_y)))
        pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)

    def update(self):
        if self.ishit:
            self.rect.y += 10
            if self.rect.y > 500:
                self.kill()
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
        self.ishit = True
        

    def __type__(self):
        return Box

class FallingP(Box):
    assets = {
            'idle':(r'assets\Traps\Falling Platforms\Off.png',1),
            'active':(r'assets\Traps\Falling Platforms\On (32x10).png',4),
        }
    