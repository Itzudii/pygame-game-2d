import pygame
from animation import Animation
from pytmx_mapper.utils import get_transform_images

class Checkpoint(pygame.sprite.Sprite):
    frames = None
    assets = {} 
    
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
        self.img_pos = data.pos

        self.ishit = False

    def draw(self,screen,camera):
        screen.blit(self.ani.image,camera.apply_pos(self.img_pos))
        pygame.draw.rect(screen,(255,255,0),camera.apply_rect(self.rect),1)

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('idle')
            self.ishit = False
        self.ani.update()

    def hit(self):
        if not self.ishit:
            self.ani.set_state('move')
        self.ishit = True

    def __type__(self):
        return Checkpoint

class Start(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\Start\Start (Idle).png',1),
        'move':(r'assets\Items\Checkpoints\Start\Start (Moving) (64x64).png',17)
    } 

class End(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\End\End (Idle).png',1),
        'move':(r'assets\Items\Checkpoints\End\End (Pressed) (64x64).png',8)
    } 


class Flag(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (No Flag).png',1),
        'move':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Out) (64x64).png',26),
        'active':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Idle)(64x64).png',10)
    } 

    def update(self):
        if self.ani.isfinished and self.ishit:
            self.ani.set_state('active')
        self.ani.update()
        