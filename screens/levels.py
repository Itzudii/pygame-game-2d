import pygame
from settings import WINDOW_W,WINDOW_H
from savedata.save import Save
class Lvls():
    def __init__(self,app):
        self.xlimit = 8
        self.ylimit = 7
        self.btns = [(i,pygame.transform.scale_by(pygame.image.load(f'assets\Menu\Levels\{i:02d}.png'),2)) for i in range(1,51)]
        self.rects = []
        self.app = app
        self.current_lvl = None
        self.load()
        self.save = self.app.save.data
        
        

    def event_handle(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_lvl:
                self.app.game_screen(self.current_lvl)

    def key_handle(self,key):
        pass

    def load(self):
        idx = 0
        offset = 100
        gap = 10
        for y in range(self.ylimit):
            for x in range(self.xlimit):
                if idx >= 50:
                    break
                lvl,img = self.btns[idx]
                rect = img.get_rect()
                rect.topleft = ((x*rect.w)+offset+(gap*x),(y*rect.w)+offset+(gap*y))
                self.rects.append((idx,rect))
                idx+=1


    def draw(self,screen):
        for idx,rect in self.rects:
            lvl,img = self.btns[idx]
            iscompleted = self.save[str(lvl)]['completed']
            screen.blit(img,rect.topleft)
            pygame.draw.rect(screen,(255,0,0) if not iscompleted else (0,255,0),rect,1)

    def update(self):
        mouse = pygame.mouse.get_pos()
        iscollide = False
        for idx,rect in self.rects:
            if rect.collidepoint(mouse):
                self.current_lvl = idx+1
                iscollide = True
        if iscollide is False:
            self.current_lvl = None

        pass   
