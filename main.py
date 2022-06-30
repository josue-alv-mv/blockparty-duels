import pygame as pg
from canvas import Canvas
from player import Player
from image import Image

class Game:
    def __init__(self):
        self.canvas = Canvas(width=1280, height=720, caption="Festa de Blocos - Neszinha Edition")
        self.player = Player(
            animations_folder_url="images/girl/",
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
        self.player.spawn(576, 250)
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
            self.canvas.update()

game = Game()
game.run()