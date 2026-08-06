
from utils.dependency import get_img

class Shadow():
    def __init__(self,target):
        self.target = target

        self.img = get_img(r"assets\Other\Shadow.png",(self.target.rect.w//1.5,10)).convert_alpha()
        self.w = self.img.get_width()
        self.rect = self.img.get_rect()
        self.rect.y = 100


    def draw(self,screen,camera):
        screen.blit(self.img,camera.apply_pos(self.rect.topleft))


    def update(self,colliders):

        self.rect.centerx= self.target.rect.centerx

        find_rect = None
        for collider in colliders:
            rect = collider.rect
            if rect.x < self.rect.center[0] < rect.right and rect.y > self.target.rect.y :
                if find_rect is None or find_rect.y > rect.y:
                    find_rect = rect

        if find_rect:
            self.rect.y = find_rect.y