import pygame as pg

class Rect:
    def __init__(self, hotspot, x, y, width, height, color, alpha=255):
        self.surf = pg.Surface((width,height))
        self.surf.fill(color)
        self.surf.set_alpha(alpha)
        self.rect = pg.Rect(0, 0, width, height)
        setattr(self.rect, hotspot, (x,y))

    def draw(self, canvas):
        canvas.blit(self.surf, self.rect)