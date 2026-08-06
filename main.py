import pygame
import sys
from level import Level
from settings import WINDOW_W,WINDOW_H
class App():
    def __init__(self):
        pygame.init()
        self.level = Level()
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((WINDOW_W,WINDOW_H))
        self.isRunning = True
        self.dt = 0
        self.load()

    def load(self):
        self.level.load()

    def event_handling(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                    break
                self.level.event_handle(event)

    def key_handling(self):
        key = pygame.key.get_pressed()
        self.level.key_handle(key)

    
    def run(self):
        while self.isRunning:
            self.screen.fill((33,31,48))

            self.event_handling()
            
            self.key_handling()

            self.level.update()

            self.level.draw(self.screen)

            pygame.display.flip()

            self.dt = self.clock.tick(60)//1000

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()