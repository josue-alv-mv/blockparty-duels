import pygame as pg
import time

class ProgressBar:
    def __init__(self, hotspot, x, y, width, height, border_width, padding):
        self.hotspot = hotspot
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_width = border_width
        self.padding = padding
        self.color = "white"
        self.border_color = "white"
        self.bg_alpha = 64
        self.progress = 0

    def wait(self, duration):
        start_time = time.time()

        while time.time() - start_time < duration:
            elapsed_time = time.time() - start_time
            self.progress = 1 - (elapsed_time / duration)
            time.sleep(0.01)

    def draw(self, canvas):
        border_rect = pg.Rect(0, 0, self.width, self.height)
        setattr(border_rect, self.hotspot, (self.x, self.y))

        rect = pg.Rect(
            0, 0, border_rect.width - 2*(self.border_width + self.padding),
            border_rect.height - 2*(self.border_width + self.padding)
        )
        rect.width *= self.progress
        rect.midleft = (border_rect.left + self.border_width + self.padding, border_rect.centery)

        transparent_bg = pg.Surface((border_rect.width, border_rect.height))
        transparent_bg.set_alpha(self.bg_alpha)

        canvas.blit(transparent_bg, border_rect)
        pg.draw.rect(canvas.surf, self.border_color, border_rect, width=self.border_width)
        pg.draw.rect(canvas.surf, self.color, rect)