import pygame
from level import Level
from settings import WINDOW_W,WINDOW_H

class Game():
    def __init__(self,app,lvl):
        self.app = app
        self.level = Level(f'mapdata/lvl_{lvl}.tmx')
        self.level.load()
        self.lvl = lvl

    def event_handle(self,event):
        self.level.event_handle(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.lvl_screen()

    def key_handle(self,key):
        self.level.key_handle(key)

    def draw(self,screen):
        self.level.draw(screen)

    def update(self):
        self.level.update() 
        if self.level.iscompleted:
            self.app.save.is_complete(str(self.lvl))
            self.app.lvl_screen()

