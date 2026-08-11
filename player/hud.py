import pygame
from settings import WINDOW_W


class HealthBar:
    """
    Draws a polished HUD health bar in the top-left corner.

    Layout (per heart slot):
      [ ♥ icon ][ filled/empty bar segment ]

    Visual style:
      - Dark translucent panel background
      - Red filled segments with a lighter red highlight strip
      - Dimmed grey segments for lost health
      - Pixel-heart icons next to the bar
    """

    # Colours
    BG_COLOUR       = (20,  18,  35, 180)   # dark translucent panel (with alpha)
    BORDER_COLOUR   = (80,  60, 100)
    HEART_FULL      = (220,  50,  70)        # vibrant red
    HEART_LOST      = ( 70,  50,  65)        # muted dark purple-grey
    BAR_FULL        = (220,  55,  75)
    BAR_FULL_HI     = (255, 120, 130)        # highlight strip
    BAR_EMPTY       = ( 55,  42,  65)
    BAR_BORDER      = ( 40,  30,  50)
    TEXT_COLOUR     = (255, 230, 240)

    # Geometry
    MARGIN_X    = 16
    MARGIN_Y    = 14
    HEART_SIZE  = 16          # px (drawn with primitives)
    HEART_GAP   = 6           # gap between hearts
    BAR_W       = 80          # full-bar width (all segments)
    BAR_H       = 14
    PANEL_PAD   = 10          # internal padding inside the panel

    def __init__(self, player):
        self.player = player
        self._font = pygame.font.SysFont("segoeui", 13, bold=True)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _draw_heart(self, surf, cx, cy, filled):
        """Draw a simple pixel heart at (cx, cy) centred."""
        colour = self.HEART_FULL if filled else self.HEART_LOST
        r = self.HEART_SIZE // 2

        # Two circles for the top lobes
        lobe_r = r // 2 + 1
        pygame.draw.circle(surf, colour, (cx - lobe_r + 1, cy - 2), lobe_r)
        pygame.draw.circle(surf, colour, (cx + lobe_r - 1, cy - 2), lobe_r)

        # Bottom triangle for the point
        points = [
            (cx - r,     cy - 1),
            (cx + r,     cy - 1),
            (cx,         cy + r + 1),
        ]
        pygame.draw.polygon(surf, colour, points)

        # Tiny white sheen on filled hearts
        if filled:
            pygame.draw.circle(surf, (255, 200, 210), (cx - lobe_r + 2, cy - 3), max(1, lobe_r // 2))

    def _draw_bar(self, surf, x, y, max_hp, current_hp):
        """Draw the segmented health bar."""
        if max_hp == 0:
            return

        seg_gap = 3
        seg_w = (self.BAR_W - seg_gap * (max_hp - 1)) // max_hp
        seg_h = self.BAR_H

        for i in range(max_hp):
            sx = x + i * (seg_w + seg_gap)
            sy = y
            filled = i < current_hp

            # Outer border
            pygame.draw.rect(surf, self.BAR_BORDER, (sx - 1, sy - 1, seg_w + 2, seg_h + 2), border_radius=3)

            # Fill
            colour = self.BAR_FULL if filled else self.BAR_EMPTY
            pygame.draw.rect(surf, colour, (sx, sy, seg_w, seg_h), border_radius=2)

            # Highlight strip on filled segments
            if filled:
                hi_rect = (sx + 2, sy + 2, seg_w - 4, 3)
                pygame.draw.rect(surf, self.BAR_FULL_HI, hi_rect, border_radius=1)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def draw(self, screen):
        p = self.player
        max_hp = p.max_health
        cur_hp = p.health

        # Panel dimensions
        hearts_width = max_hp * self.HEART_SIZE + (max_hp - 1) * self.HEART_GAP
        panel_w = self.PANEL_PAD * 2 + hearts_width + 12 + self.BAR_W
        panel_h = self.PANEL_PAD * 2 + max(self.HEART_SIZE, self.BAR_H + 4)

        px = self.MARGIN_X
        py = self.MARGIN_Y

        # Translucent panel (requires a surface with per-pixel alpha)
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill(self.BG_COLOUR)
        screen.blit(panel, (px, py))

        # Panel border
        pygame.draw.rect(screen, self.BORDER_COLOUR,
                         (px, py, panel_w, panel_h), 1, border_radius=4)

        # Heart icons
        heart_y = py + panel_h // 2
        for i in range(max_hp):
            hx = px + self.PANEL_PAD + i * (self.HEART_SIZE + self.HEART_GAP) + self.HEART_SIZE // 2
            self._draw_heart(screen, hx, heart_y, i < cur_hp)

        # Bar
        bar_x = px + self.PANEL_PAD + hearts_width + 12
        bar_y = py + (panel_h - self.BAR_H) // 2
        self._draw_bar(screen, bar_x, bar_y, max_hp, cur_hp)

        # "HP" label
        label = self._font.render("HP", True, self.TEXT_COLOUR)
        screen.blit(label, (bar_x + self.BAR_W + 6, bar_y + 1))
