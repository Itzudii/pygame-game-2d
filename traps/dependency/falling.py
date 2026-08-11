import pygame
from baseclass.intractive import IntractiveObject

class Platform(IntractiveObject):
    
    def __init__(self,data):
        super().__init__(data)
        self.isActive = False
        self.ishit = False
        self.on()

    # def draw(self,screen,camera):
    #     screen.blit(self.animation.image,camera.apply_pos((self.rect.x-self.m_rect.dif_x,self.rect.y-self.m_rect.dif_y)))
    #     pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)

    def update(self):
        if self.ishit:
            self.rect.y += 10
            if self.rect.y > 500:
                self.kill()
        self.animation.update()

    def on(self):
        if not self.isActive:
            self.animation.set_state('active')
            self.isActive = True

    def off(self):
        if self.isActive:
            self.animation.set_state('idle')
            self.isActive = False

    def hit(self):
        self.ishit = True

