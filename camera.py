import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset = pygame.Vector2()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, target):
        # Center camera on player
        self.offset.x = target.rect.centerx - self.screen_width // 2
        self.offset.y = target.rect.centery - self.screen_height // 2

    def apply_rect(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    

    def apply_pos(self, pos):
        return (
            pos[0] - self.offset.x,
            pos[1] - self.offset.y
        )
