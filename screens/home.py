import pygame
from settings import WINDOW_W,WINDOW_H

class Home():
    def __init__(self,app):
        self.playbtn = pygame.transform.scale_by(pygame.image.load(r'assets\Menu\Buttons\Play.png'),2)
        self.rect = self.playbtn.get_rect()
        self.rect.centerx = WINDOW_W//2
        self.rect.centery = WINDOW_H//1.5
        self.app = app

    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.app.lvl_screen()

    def key_handle(self,key):
        pass

    def draw(self,screen):
        screen.blit(self.playbtn,self.rect.topleft)

    def update(self):
        pass   

