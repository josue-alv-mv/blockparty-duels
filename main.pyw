import pygame as pg
import sys
import time
from canvas import Canvas
from network import Client, Server
from player import Player
from opponent import Opponent
from image import Image
from platform import Platform
from text import Text
from text_field import TextField
from button import Button

class Game:
    def __init__(self):
        pg.init()
        self.name = "nordss.blockparty-duels"
        self.canvas = Canvas(width=854, height=480, caption="Blockparty Duels")
        self.player = Player(
            images_folder_url="images/lonelybryxn/", animation_speed=90,
            rect_width=39, rect_height=76, speed=300, gravity_speed=600,
            on_floor_confidence=16 # calc = gravity_speed/fps - 1 (can stuck player if fps is lower than 35)
        )
        self.opponent = Opponent(
            images_folder_url="images/melyniu/", animation_speed=90,
            rect_width=39, rect_height=76, speed=300, gravity_speed=600
        )
        self.backgrounds = {
            "menu": Image(url="images/backgrounds/menu_bg.png", hotspot="topleft", x=0, y=0),
            "game": Image(url="images/backgrounds/game_bg.png", hotspot="topleft", x=0, y=0)
        } 
        self.platform = Platform(
            images_folder_url="images/blocks/", hotspot="center",
            x=self.canvas.centerx, y=self.canvas.centery + 200
        )
        self.buttons = {
            "create_room": Button(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 15,
                width=180, height=60, text="Create room"
            ),
            "join_room": Button(
                hotspot="midtop", x=self.canvas.centerx, y=self.canvas.centery + 15,
                width=180, height=60, text="Join room"
            ),
            "back_from_join_room": Button(
                hotspot="midtop", x=self.canvas.centerx - 65, y=self.canvas.centery + 50,
                width=105, height=45, text="Back"
            ),
            "join_from_join_room": Button(
                hotspot="midtop", x=self.canvas.centerx + 65, y=self.canvas.centery + 50,
                width=105, height=45, text="Join"
            )
        }
        self.texts = {
            "ip_address": Text(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 50,
                text="IP Address", font_size=48
            )
        }
        self.text_field = TextField(
            hotspot="center", x=self.canvas.centerx, y=self.canvas.centery, width=300,
            height=50, font_size=28, max_text_length=15, rect_alpha=96,
            keys=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        )
        self.player.spawn(640, 320)
        self.platform.shuffle()

    def run(self):
        self.login_screen()

    def login_screen(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["create_room"].focused:
                        self.create_room_screen()

                    elif self.buttons["join_room"].focused:
                        self.join_room_screen()

            self.buttons["create_room"].update()
            self.buttons["join_room"].update()

            self.backgrounds["menu"].draw(self.canvas)
            self.buttons["create_room"].draw(self.canvas)
            self.buttons["join_room"].draw(self.canvas)
            self.canvas.update()

    def create_room_screen(self):
        self.network = Server()
        self.network.listen()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            for message in self.network.get():
                if message.tag == "game-name" and message.text == self.name:
                    self.network.send(tag="game-name", message=self.name)
                    self.match_screen()

            self.backgrounds["menu"].draw(self.canvas)
            self.canvas.update()

    def join_room_screen(self):
        self.network = Client()
        self.texts["ip_address"].text = f"IP Address"

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.unicode in self.text_field.keys:
                        self.text_field.on_press(event.unicode)

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["back_from_join_room"].focused:
                        self.login_screen()

                    elif self.buttons["join_from_join_room"].focused:
                        if self.network.connect(self.text_field.text):
                            self.network.send(tag="game-name", message=self.name)

                        else:
                            self.texts["ip_address"].text = f"Connection error :("

            for message in self.network.get():
                if message.tag == "game-name" and message.text == self.name:
                    self.match_screen()

            self.buttons["back_from_join_room"].update()
            self.buttons["join_from_join_room"].update()

            self.backgrounds["menu"].draw(self.canvas)
            self.texts["ip_address"].draw(self.canvas)
            self.text_field.draw(self.canvas)
            self.buttons["back_from_join_room"].draw(self.canvas)
            self.buttons["join_from_join_room"].draw(self.canvas)
            self.canvas.update()

    def match_screen(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                        self.player.send_json(self.network)

                    if event.key == pg.K_UP:
                        if self.player.request_jump(collision_blocks=self.platform.slots):
                            self.player.send_json(self.network, flags=["jump"])

                elif event.type == pg.KEYUP:
                    if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                        self.player.send_json(self.network)

            for message in self.network.get():
                if message.tag == "get" and message.text == "player_json":
                    self.player.send_json(self.network)

                elif message.tag == "player":
                    self.opponent.load_json(message.text)

            if not self.opponent.active:
                self.network.send(tag="get", message="player_json")
                self.canvas.update()
                continue

            if time.time() - self.player.time_of_last_data_sync > 1:
                self.player.send_json(self.network)

            self.player.update(collision_blocks=self.platform.slots)
            self.opponent.update(collision_blocks=self.platform.slots)

            if self.player.y > self.canvas.height:
                self.player.x = 640
                self.player.y = 320
                self.player.update_rect()

            self.backgrounds["game"].draw(self.canvas)
            self.platform.draw(self.canvas)
            self.opponent.draw(self.canvas)
            self.player.draw(self.canvas)
            self.canvas.update()

game = Game()
game.run()