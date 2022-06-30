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
            rect_width=34,
            rect_height=89,
            speed=300,
            gravity_speed=600
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
        self.player.spawn(576, 250)
        self.platform.shuffle()
        self.running = True

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.player.jump()

            self.player.update()

            self.background.draw(self.canvas)
            self.player.draw(self.canvas)
            self.platform.draw(self.canvas)
            self.canvas.update()

game = Game()
game.run()