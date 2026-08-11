import pygame
from baseclass.intractive import IntractiveObject

class Checkpoint(IntractiveObject):


    def __init__(self,data):
        super().__init__(data)
        self.ishit = False

    # def draw(self,screen,camera):
    #     screen.blit(self.animation.image,camera.apply_pos(self.img_pos))
    #     pygame.draw.rect(screen,(255,255,0),camera.apply_rect(self.rect),1)

    def update(self):
        if self.animation.isfinished and self.ishit:
            self.animation.set_state('idle')
            self.ishit = False
        self.animation.update()

    def hit(self):
        if not self.ishit:
            self.animation.set_state('move')
        self.ishit = True
