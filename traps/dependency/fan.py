import random
import pygame
from utils.dependency import get_img,TILESIZE
from utils.partical import Partical


# Height (in pixels) of the upward wind column above the fan
WIND_HEIGHT = TILESIZE * 5   # 5 tiles tall
# Upward force applied to the player while levitating
LIFT_FORCE   = 0.45          # counters gravity (gravity = 0.3)
# Maximum upward speed while levitating (caps so it feels floaty, not rocketlike)
MAX_LIFT_VEL = -3.5


class Dust(Partical):
    img = get_img(r"assets\Other\Dust Particle.png",(TILESIZE//3,TILESIZE//3))
    def __init__(self, wind_rect, lifespan):
        super().__init__(lifespan)
        self.img = self.__class__.img.convert_alpha()
        # Spawn anywhere across the wind column width, starting from the fan top
        self.x = random.randint(wind_rect.left, wind_rect.right)
        self.y = wind_rect.bottom          # start at the fan surface
        self.target_y = wind_rect.top      # rise to the top of the column
        self.speed = random.uniform(1.2, 2.5)

    def draw(self, screen, camera):
        screen.blit(self.img, camera.apply_pos((self.x, self.y)))

    def update(self):
        super().update()
        self.y -= self.speed   # rise upward
        # small horizontal drift for organic look
        self.x += random.uniform(-0.3, 0.3)

from baseclass.intractive import IntractiveObject
class FanObj(IntractiveObject):

    def __init__(self, data):
        super().__init__(data)
        self.isActive = False

        self.particals = pygame.sprite.Group()
        self.delay = 0

        # Wind column: tall rect directly above the fan
        self.wind_rect = pygame.Rect(
            self.rect.x,
            self.rect.top - WIND_HEIGHT,
            self.rect.w,
            WIND_HEIGHT
        )

        self.on()

    # ------------------------------------------------------------------

    def draw(self, screen, camera):
        screen.blit(self.animation.image, camera.apply_pos(self.img_pos))

        for particle in self.particals:
            particle.draw(screen, camera)

    def update(self):
        self.animation.update()

        if self.isActive:
            self.delay += 1
            if self.delay > 6:            # spawn particles faster than before
                self.particals.add(Dust(self.wind_rect, 80))
                self.delay = 0
            self.particals.update()

    # ------------------------------------------------------------------

    def levitate(self, player):
        """Apply upward wind force when the player is inside the wind column."""
        if not self.isActive:
            return False
        if self.wind_rect.colliderect(player.rect):
            # Push upward: subtract lift from vel_y (negative = upward)
            player.vel_y -= LIFT_FORCE
            # Clamp so player can't rocket up faster than MAX_LIFT_VEL
            if player.vel_y < MAX_LIFT_VEL:
                player.vel_y = MAX_LIFT_VEL
            # Allow double-jump to be refreshed while floating in wind
            player.doublejumpuse = False
            return True
        return False

    # ------------------------------------------------------------------

    def on(self):
        if not self.isActive:
            self.animation.set_state('active')
            self.isActive = True

    def off(self):
        if self.isActive:
            self.animation.set_state('idle')
            self.isActive = False

