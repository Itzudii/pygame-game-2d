import pygame
class BG():
    Basepath = 'assets/tileset/Background'
    layers = [
        pygame.image.load(Basepath+'/Forbidden_Graveyard_2D_Platformer_Tileset_Background00.png'),
        pygame.image.load(Basepath+'/Forbidden_Graveyard_2D_Platformer_Tileset_Background01.png'),
    ]
    def __init__(self):
        self.layer1 = BG.layers[0]
        self.layer2 = BG.layers[1]

    def draw(self,screen):
        screen.blit(self.layer1,(0,0))
        screen.blit(self.layer2,(0,0))

    def update(self,screen):
        self.draw(screen)