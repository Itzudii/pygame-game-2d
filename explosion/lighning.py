import pygame
from animation import Animation
import time

class Lightning(pygame.sprite.Sprite):
    def __init__(self,x,y,completion_seconds:float):
        super().__init__()
        self.beginning_frames = [pygame.image.load(f'assets\explosion\PNG\Lightning\Lightning_beginning{i}.png') for i in range(1,6)]
        self.beginning_part_frames = [pygame.image.load(f'assets\explosion\PNG\Lightning\Lightning_beginning{i}_part.png') for i in range(3,6)]
        self.cycle_frames = [pygame.image.load(f'assets\explosion\PNG\Lightning\Lightning_cycle{i}.png') for i in range(3,7)]
        self.cycle_spot_frames = [pygame.image.load(f'assets\explosion\PNG\Lightning\Lightning_spot{i}.png') for i in range(3,5)]
        self.end_frames = [pygame.image.load(f'assets\explosion\PNG\Lightning\Lightning_end{i}.png') for i in range(3,4)]
        self.ani1 = Animation(self.beginning_frames,1,False)
        self.ani2 = Animation(self.beginning_part_frames,1,False)
        self.ani3 = Animation(self.cycle_frames,1,True)
        self.ani4 = Animation(self.cycle_spot_frames,1,True)
        self.ani5 = Animation(self.end_frames,1,False)
        self.rect = self.cycle_frames[0].get_rect()
        self.t1 = time.perf_counter()
        self.x = x
        self.y = y
        self.phase = 1
        self.ct = completion_seconds

    def update(self,screen):
        if self.phase == 1:
            screen.blit(self.ani1.image,(self.x,self.y))
            self.ani1.update()
            if self.ani1.finished:
                self.phase = 2
            if self.ani1.index >2:
                screen.blit(self.ani2.image,(self.x,self.y))
                self.ani2.update()
                if self.ani2.finished:
                    self.phase = 2
        elif self.phase == 2:
            screen.blit(self.ani3.image,(self.x,self.y))
            self.ani3.update()
            if self.ani3.finished:
                self.phase = 3

            screen.blit(self.ani4.image,(self.x,self.y+self.rect.h-39))
            self.ani4.update()
            if self.ani4.finished:
                self.phase = 3
            if time.perf_counter()-self.t1 >= self.ct:
                self.ani3.end()
                self.ani4.end()
        elif self.phase == 3:
            screen.blit(self.ani5.image,(self.x,self.y))
            self.ani5.update()
            if self.ani5.finished:
                self.phase = 0
                self.kill()


        
        