import pygame
from settings import WINDOW_H,WINDOW_W,TILESIZE
class BG():

    def __init__(self,map):
        cls = self.__class__
        self.bg = pygame.image.load(cls.Basepath).convert_alpha()
        self.map = map

        self.bg_img = pygame.transform.scale_by(self.bg,self.map.scale_factor)

        self.dt = 0

        self.w = self.bg_img.get_width()
        self.h = self.bg_img.get_height()

        self.no_of_blocks_w = (WINDOW_W // self.w) + 1
        self.no_of_blocks_h = (WINDOW_H // self.h) + 1

        self.w_x = (self.map.width * TILESIZE) - self.no_of_blocks_w * self.w
        self.h_y = (self.map.height * TILESIZE) - self.no_of_blocks_h * self.h


    def draw(self,screen,camera):

        ox = camera.offset.x
        oy = camera.offset.y

        cam_X = self.w-ox
        cam_Y = self.h-oy

        cam_X_w = self.w_x-ox
        cam_Y_h = self.h_y-oy

        x = cam_X%self.w
        y = cam_Y%self.h

        f_x = min(max(x,cam_X),cam_X_w)
        f_y = min(max(y,cam_Y),cam_Y_h)+self.dt
        # f_y = min(max(y,cam_Y),cam_Y_h)

        for j in range(self.no_of_blocks_h):
            for i in range(-1,self.no_of_blocks_w):
                screen.blit(self.bg_img,(f_x+(i*self.w),f_y+(j*self.h)))

        pygame.draw.rect(screen,(33,31,48),pygame.Rect(0,-self.h-oy,WINDOW_W,self.h))

        pygame.draw.rect(screen,(33,31,48),pygame.Rect(0,self.map.height_px-oy,WINDOW_W,self.h))

    def update(self):
        self.dt+=1
        if self.dt >= self.w:
            self.dt=0


class Blue(BG):
    Basepath = r'assets\Background\Blue.png'
    
class Brown(BG):
    Basepath = r'assets\Background\Brown.png'

class Gray(BG):
    Basepath = r'assets\Background\Gray.png'

class Green(BG):
    Basepath = r'assets\Background\Green.png'

class Pink(BG):
    Basepath = r'assets\Background\Pink.png'

class Purple(BG):
    Basepath = r'assets\Background\Purple.png'

class Yellow(BG):
    Basepath = r'assets\Background\Yellow.png'
