import pygame
from utils.dependency import get_img
import math

class PointPath:
    def __init__(self, points, speed=2):
        self.points = points
        self.speed = speed

        self.index = 0
        self.x, self.y = self.points[0]

        self.dx = 0
        self.dy = 0

    def update(self):
        target_x, target_y = self.points[self.index]

        dx = target_x - self.x
        dy = target_y - self.y

        distance = (dx * dx + dy * dy) ** 0.5

        if distance <= self.speed:
            # Reached the point
            self.x = target_x
            self.y = target_y

            # Go to next point
            self.index = (self.index + 1) % len(self.points)
            # self.direction = self.x

        else:
            # Move toward target
            self.dx = (dx / distance) * self.speed
            self.dy  = (dy / distance) * self.speed


            self.x += self.dx
            self.y += self.dy

    @property
    def pos(self):
        return self.x, self.y

class Chain():
    def __init__(self,points,src):
        self.points = points
        self.img = get_img(src)
        self.len = len(self.points)
        self.idx = 0
        self.dw = self.img.get_width()//2
        self.dh = self.img.get_height()//2
        self.spacing = self.dw*8

    
    def draw(self,screen,camera):

        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]

            dx = x2 - x1
            dy = y2 - y1

            distance = math.hypot(dx, dy)

            if distance == 0:
                continue

            # Direction of the line
            ux = dx / distance
            uy = dy / distance

            # Draw image every 16px
            for d in range(0, int(distance) + 1, self.spacing):
                x = x1 + ux * d
                y = y1 + uy * d

                screen.blit(
                    self.img,
                    camera.apply_pos((x-self.dw, y-self.dh))
                )

from baseclass.intractive import IntractiveObject  
class MovingObject(IntractiveObject):

    def __init__(self,data,points):
        cls = self.__class__
        super().__init__(data)
        self.path = PointPath(points)
        self.chain = Chain(points,cls.chain_src)
        self.isActive = False
        self.on()

    def draw(self,screen,camera):
        screen.blit(self.animation.image,camera.apply_pos((self.rect.x-self.m_rect.dif_x,self.rect.y-self.m_rect.dif_y)))
        pygame.draw.rect(screen,(255,0,0),camera.apply_rect(self.rect),1)
        self.chain.draw(screen,camera)

    def update(self):
        pos = self.path.pos
    
        self.rect.center = pos
        self.img_pos = pos
        self.animation.update()
        if self.isActive:
            self.path.update()

    def on(self):
        if not self.isActive:
            self.animation.set_state('active')
            self.isActive = True

    def off(self):
        if self.isActive:
            self.animation.set_state('idle')
            self.isActive = False
