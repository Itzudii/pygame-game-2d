import pygame
import sys
from settings import WINDOW_W,WINDOW_H
from screens.home import Home
from screens.game import Game
from screens.levels import Lvls
from savedata.save import Save

class App():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((WINDOW_W,WINDOW_H))
        self.isRunning = True
        self.dt = 0

        self.cur_screen = None
        self.save = Save('savedata/level.json')

        self.home_screen()

    def home_screen(self):
        self.cur_screen = Home(self)

    def lvl_screen(self):
        self.cur_screen = Lvls(self)

    def game_screen(self,lvl):
        self.cur_screen = Game(self,lvl)


    def run(self):
        while self.isRunning:
            self.screen.fill((33,31,48))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                self.cur_screen.event_handle(event)

            key = pygame.key.get_pressed()
            self.cur_screen.key_handle(key)

            self.cur_screen.update()

            self.cur_screen.draw(self.screen)

            pygame.display.flip()

            self.dt = self.clock.tick(60)//1000

        pygame.quit()
        sys.exit()
        
if __name__ == '__main__':
    app = App()
    app.run()