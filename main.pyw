import pygame as pg
import sys
import time
import threading
from canvas import Canvas
from network import Client, Server
from local_player import LocalPlayer
from opponent import Opponent
from image import Image
from platform import Platform
from text import Text
from text_field import TextField
from button import Button
from progress_bar import ProgressBar

class Game:
    def __init__(self):
        pg.init()
        self.name = "nordss.blockparty-duels"
        self.level_interval = 5
        self.canvas = Canvas(width=1280, height=720, caption="Blockparty Duels")
        self.player = LocalPlayer(
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
            images_folder_url="images/blocks/", hotspot="midbottom",
            x=self.canvas.centerx, y=self.canvas.height - 96
        )
        self.buttons = {
            "create_room": Button(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 15,
                width=180, height=60, text="Criar Partida"
            ),
            "join_room": Button(
                hotspot="midtop", x=self.canvas.centerx, y=self.canvas.centery + 15,
                width=180, height=60, text="Conectar-se"
            ),
            "join_room.back": Button(
                hotspot="midtop", x=self.canvas.centerx - 65, y=self.canvas.centery + 50,
                width=105, height=45, text="Voltar"
            ),
            "join_room.join": Button(
                hotspot="midtop", x=self.canvas.centerx + 65, y=self.canvas.centery + 50,
                width=105, height=45, text="Entrar"
            )
        }
        self.texts = {
            "join_room.main": Text(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 50,
                text="", font_size=48
            ),
            "create_room.main": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery,
                text="Aguardando um oponente...", font_size=48
            ),
            "match.main": Text(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 48,
                text="", font_size=48
            )
        }
        self.text_field = TextField(
            hotspot="center", x=self.canvas.centerx, y=self.canvas.centery, width=300,
            height=50, font_size=28, max_text_length=15, rect_alpha=96,
            keys=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        )
        self.progress_bar = ProgressBar(
            hotspot="center", x=self.canvas.centerx, y=self.canvas.centery, width=384,
            height=32, border_width=3, padding=3
        )
        self.player.spawn(640, 320)

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
            self.texts["create_room.main"].draw(self.canvas)
            self.canvas.update()

    def join_room_screen(self):
        self.network = Client()
        self.texts["join_room.main"].text = f"Endereço IP"

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN:
                    if event.unicode in self.text_field.keys:
                        self.text_field.on_press(event.unicode)

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["join_room.back"].focused:
                        self.login_screen()

                    elif self.buttons["join_room.join"].focused:
                        if self.network.connect(self.text_field.text):
                            self.network.send(tag="game-name", message=self.name)

                        else:
                            self.texts["join_room.main"].text = f"Erro de conexão :("

            for message in self.network.get():
                if message.tag == "game-name" and message.text == self.name:
                    self.match_screen()

            self.buttons["join_room.back"].update()
            self.buttons["join_room.join"].update()

            self.backgrounds["menu"].draw(self.canvas)
            self.texts["join_room.main"].draw(self.canvas)
            self.text_field.draw(self.canvas)
            self.buttons["join_room.back"].draw(self.canvas)
            self.buttons["join_room.join"].draw(self.canvas)
            self.canvas.update()

    def match_screen(self):
        if not self.network.is_host:
            self.network.send(tag="start", message="match")
            
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                        self.player.send_json(self.network)

                    if event.key == pg.K_UP:
                        if self.player.request_jump(collision_blocks=self.platform.active_slots):
                            self.player.send_json(self.network, flags=["jump"])

                elif event.type == pg.KEYUP:
                    if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                        self.player.send_json(self.network)

            for message in self.network.get():
                if message.tag == "player":
                    self.opponent.load_json(message.text)

                # host network events
                if self.network.is_host:
                    if message.tag == "start" and message.text == "match":
                        self.async_run(self.match_executor)

                # client network events
                else:
                    if message.tag == "platform":
                        self.platform.load_json(message.text)
                        self.async_run(self.match_executor)

            if time.time() - self.player.time_of_last_data_sync > 0.5:
                self.player.send_json(self.network)

            if not self.opponent.active:
                self.canvas.update()
                continue

            self.player.update(collision_blocks=self.platform.active_slots)
            self.opponent.update(collision_blocks=self.platform.active_slots)

            self.backgrounds["game"].draw(self.canvas)
            self.platform.draw(self.canvas)
            self.opponent.draw(self.canvas)
            self.player.draw(self.canvas)
            self.texts["match.main"].draw(self.canvas)
            self.progress_bar.draw(self.canvas)
            self.canvas.update()

    def match_executor(self):
        if self.network.is_host:
            self.platform.update()
            self.platform.send_json(self.network)

        self.texts["match.main"].text = "Prepare-se !"
        self.progress_bar.color = "white"
        self.progress_bar.wait(self.level_interval)
        self.texts["match.main"].text = self.platform.chosen_color
        self.progress_bar.color = self.get_rgb_from_chosen_color(self.platform.chosen_color)
        self.progress_bar.wait(self.platform.timeout)
        self.platform.destroy()
        self.texts["match.main"].text = ""
        self.progress_bar.color = "white"
        self.progress_bar.wait(self.level_interval)

        if self.network.is_host:
            self.platform.level += 1
            self.async_run(self.match_executor)

    def async_run(self, function):
        thread = threading.Thread(target=function, daemon=True)
        thread.start()

    def get_rgb_from_chosen_color(self, color):
        return {
            "Azul": (51,70,166),
            "Marrom": (177,106,71),
            "Cinza": (38,38,38),
            "Verde": (71,177,71),
            "Azul Claro": (72,236,237),
            "Cinza Claro": (116,116,116),
            "Verde Claro": (109,241,109),
            "Magenta": (175,95,255),
            "Laranja": (247,137,82),
            "Rosa": (240,99,239),
            "Roxo": (102,58,190),
            "Vermelho": (237,72,72),
            "Branco": (237,237,237),
            "Amarelo": (252,224,87)
        } [color]
        
game = Game()
game.run()