import pygame as pg

class Canvas:
    def __init__(self, width, height, caption="Untitled", icon_url=None):
        self.width = width
        self.height = height
        self.centerx = width//2
        self.centery = height//2
        self.surf = pg.display.set_mode((width, height), flags=pg.SCALED | pg.RESIZABLE, vsync=1)
        self.set_caption(caption)
        if icon_url is not None:
            self.set_icon(pg.image.load(icon_url).convert_alpha())

    def set_caption(self, caption):
        pg.display.set_caption(caption)

    def set_icon(self, icon):
        pg.display.set_icon(icon)

    def fill(self, color):
        self.surf.fill(color)

    def blit(self, source, dest):
        self.surf.blit(source, dest)
        
    def update(self):
        pg.display.update()