import pygame as pg

class Image:
    def __init__(self, url, hotspot, x, y):
        self.surf = pg.image.load(url).convert_alpha()
        self.rect = self.surf.get_rect()
        setattr(self.rect, hotspot, (x,y))

    def draw(self, canvas):
        canvas.blit(self.surf, self.rect)