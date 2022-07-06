import pygame as pg

class Text:
    def __init__(
        self, hotspot, x, y, text,
        font_name="fonts/main.ttf", font_size=24, font_color="white", anti_aliasing=True):
        
        self.hotspot = hotspot
        self.x = x
        self.y = y
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.anti_aliasing = anti_aliasing

    def draw(self, canvas):
        font = pg.font.Font(self.font_name, self.font_size)
        text_surf = font.render(self.text, self.anti_aliasing, self.font_color)
        text_rect = text_surf.get_rect()
        setattr(text_rect, self.hotspot, (self.x, self.y))
        canvas.blit(text_surf, text_rect)