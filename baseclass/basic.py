import pygame
from pytmx_mapper.utils import get_transform_images

class BasicObject(pygame.sprite.Sprite):
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
        self.image = cls.frames['idle'][1][0]
        self.m_rect = data.rects[0]
        self.rect = pygame.Rect(self.m_rect.x,self.m_rect.y,self.m_rect.w,self.m_rect.h)
        self.img_pos = data.pos

    def draw(self,screen,camera):
        screen.blit(self.image,camera.apply_pos(self.img_pos))
        pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)

