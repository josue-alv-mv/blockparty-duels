import pygame as pg
import time
import pyperclip

class TextField:
    def __init__(
        self, hotspot, x, y, width, height, font_size, max_text_length, rect_alpha,
        border_color="white", border_width=2, font_name="fonts/main.ttf", font_color="white",
        anti_aliasing=True, keys=[]):

        self.hotspot = hotspot
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.max_text_length = max_text_length
        self.rect_alpha = rect_alpha
        self.border_width = border_width
        self.border_color = border_color
        self.anti_aliasing = anti_aliasing
        self.cursor_rect = pg.Rect(0, 0, 1, int(self.height/1.5))
        self.text = ""
        self.keys = ["\x08", "\x16"] + keys

    def draw(self, canvas):
        # create rectangles
        rect_surf = pg.Surface((self.width, self.height))
        rect_surf.set_alpha(self.rect_alpha)
        rect = rect_surf.get_rect()
        setattr(rect, self.hotspot, (self.x, self.y))

        # draw rectangle and border
        canvas.blit(rect_surf, rect)
        pg.draw.rect(canvas.surf, self.border_color, rect, self.border_width)

        # draw text
        font = pg.font.Font(self.font_name, self.font_size)
        text_surf = font.render(self.text, self.anti_aliasing, self.font_color)
        text_rect = text_surf.get_rect(center=rect.center)
        canvas.blit(text_surf, text_rect)

        # draw cursor
        if time.time() % 1 < 0.5:
            if self.text == "":
                self.cursor_rect.center = rect.center
            else:
                self.cursor_rect.center = (text_rect.midright[0] + 2, text_rect.midright[1])

            pg.draw.rect(canvas.surf, self.font_color, self.cursor_rect)
    
    def on_press(self, unicode):
        if unicode == "\x08":
            self.text = self.text[:-1]

        elif unicode == "\x16":
            self.text += self.get_clipboard_text()

        else:
            self.text += unicode

        self.text = self.text[:self.max_text_length]

    def get_clipboard_text(self):
        return "".join( [char for char in pyperclip.paste() if char in self.keys] )