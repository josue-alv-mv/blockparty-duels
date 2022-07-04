import pygame as pg
from player import Player

class SkinViewer:
    def __init__(
        self, hotspot, x, y, width, height, alpha, name, images_folder_url
    ):
        self.rect = pg.Rect(0, 0, width, height)
        setattr(self.rect, hotspot, (x,y))
        self.rect_surf = pg.Surface((width, height))
        self.alpha = alpha
        self.name = name
        self.player = Player(
            animation_speed=45, rect_width=39, rect_height=76, speed=0, gravity_speed=0
        )
        self.player.load_images(images_folder_url)
        self.player.x, self.player.y = self.rect.center
        self.player.get_pressed_keys = self.get_pressed_keys
        self.focused = False

    def update(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.focused = True
            self.rect_surf.fill("white")
            self.rect_surf.set_alpha(self.alpha)

        else:
            self.focused = False
            self.rect_surf.fill("black")
            self.rect_surf.set_alpha(self.alpha)
        

    def draw(self, canvas):
        self.player.update(collision_blocks=[])

        canvas.blit(self.rect_surf, self.rect)
        pg.draw.rect(canvas.surf, "white", self.rect, 2)
        self.player.draw(canvas)

    def get_pressed_keys(self):
        return []