import pygame as pg
from canvas import Canvas
from player import Player
from image import Image
from platform import Platform

class Game:
    def __init__(self):
        self.canvas = Canvas(width=1280, height=720, caption="Blockparty Duels")
        self.player = Player(
            images_folder_url="images/melyniu/",
            animation_speed=90,
            rect_width=39,
            rect_height=76, #106 total height
            speed=300,
            gravity_speed=600,
            on_floor_confidence=16 # calc = gravity_speed/fps - 1 (can stuck player if fps is lower than 35)
        )
        self.background = Image(
            url="images/background.png",
            hotspot="topleft", x=0, y=0
        )
        self.platform = Platform(
            images_folder_url="images/blocks/",
            hotspot="center",
            x=self.canvas.centerx,
            y=self.canvas.centery + 200
        )
        self.player.spawn(640, 320)
        self.platform.shuffle()
        self.running = True

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.player.request_jump(collision_blocks=self.platform.slots)

            self.player.update(collision_blocks=self.platform.slots)
            if self.player.y > self.canvas.height:
                self.player.x = 640
                self.player.y = 320
                self.player.update_rect()

            self.background.draw(self.canvas)
            self.platform.draw(self.canvas)
            self.player.draw(self.canvas)
            self.canvas.update()

game = Game()
game.run()