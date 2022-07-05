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
from skin_viewer import SkinViewer
from rect import Rect

class Game:
    def __init__(self):
        pg.init()
        self.name = "nordss.blockparty-duels"
        self.level_interval = 5
        self.canvas = Canvas(width=1280, height=720, caption="Blockparty Duels")
        self.player = LocalPlayer(
            animation_speed=90, rect_width=39, rect_height=76, speed=300, gravity_speed=600,
            on_floor_confidence=16 # calc = gravity_speed/fps - 1 (can stuck player if the framerate is lower than 35)
        )
        self.opponent = Opponent(
            animation_speed=90, rect_width=39, rect_height=76, speed=300, gravity_speed=600
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
            "home.create_room": Button(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 15,
                width=180, height=60, text="Criar Partida"
            ),
            "home.join_room": Button(
                hotspot="midtop", x=self.canvas.centerx, y=self.canvas.centery + 15,
                width=180, height=60, text="Conectar-se"
            ),
            "create_room.back":Button(
                hotspot="midtop", x=self.canvas.centerx, y=self.canvas.centery + 15,
                width=105, height=45, text="Voltar"
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
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 15,
                text="Aguardando um oponente...", font_size=48
            ),
            "choose_skin.choose": Text(
                hotspot="center", x=self.canvas.centerx, y=105,
                text="Escolha sua Skin", font_size=48
            ),
            "choose_skin.waiting": Text(
                hotspot="center", x=self.canvas.centerx, y=self.canvas.centery,
                text="Aguardando o criador da partida escolher a skin...", font_size=48
            ),
            "match.main": Text(
                hotspot="midbottom", x=self.canvas.centerx, y=self.canvas.centery - 48,
                text="", font_size=60
            ),
            "match.round": Text(
                hotspot="midtop", x=self.canvas.centerx, y=35, text="",
                font_size=28
            ),
            "match.timeout": Text(
                hotspot="midtop", x=self.canvas.centerx, y=67, text="",
                font_size=28
            ),
            "match.ping": Text(
                hotspot="midtop", x=self.canvas.centerx, y=99, text="Ping: ?",
                font_size=28
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
        self.skin_viewers = [
            SkinViewer(
                hotspot="midright", x=self.canvas.centerx - 15, y=self.canvas.centery, width=230,
                height=300, alpha=96, name="lonelybryxn",
                images_folder_url="images/lonelybryxn/"
            ),
            SkinViewer(
                hotspot="midleft", x=self.canvas.centerx + 15, y=self.canvas.centery, width=230,
                height=300, alpha=96, name="melyniu",
                images_folder_url="images/melyniu/"
            )
        ]
        self.rectangles = {
            "match.info_bg": Rect(
                hotspot="midtop", x=self.canvas.centerx, y=10, width=245, height=135, color="black",
                alpha=96
            )
        } 
        self.side_barriers = [
            pg.Rect(0, 0, self.platform.rect.left, self.canvas.height),
            pg.Rect(
                self.platform.rect.left + self.platform.rect.width, 0,
                self.canvas.width - self.platform.rect.right, self.canvas.height
            )
        ]
        self.events = {
            "ping_request": pg.USEREVENT
        }
        pg.time.set_timer(self.events["ping_request"], 5000)

    def run(self):
        self.home_screen()

    def home_screen(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["home.create_room"].focused:
                        self.create_room_screen()

                    elif self.buttons["home.join_room"].focused:
                        self.join_room_screen()

            self.buttons["home.create_room"].update()
            self.buttons["home.join_room"].update()

            self.backgrounds["menu"].draw(self.canvas)
            self.buttons["home.create_room"].draw(self.canvas)
            self.buttons["home.join_room"].draw(self.canvas)
            self.canvas.update()

    def create_room_screen(self):
        self.network = Server()
        self.network.listen()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.buttons["create_room.back"].focused:
                        self.network.close()
                        self.home_screen()

            for message in self.network.get():
                if message.tag == "game-name" and message.text == self.name:
                    self.network.send(tag="game-name", message=self.name)
                    self.choose_skin_screen()

            self.buttons["create_room.back"].update()

            self.backgrounds["menu"].draw(self.canvas)
            self.texts["create_room.main"].draw(self.canvas)
            self.buttons["create_room.back"].draw(self.canvas)
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
                        self.home_screen()

                    elif self.buttons["join_room.join"].focused:
                        if self.network.connect(self.text_field.text):
                            self.network.send(tag="game-name", message=self.name)

                        else:
                            self.texts["join_room.main"].text = f"Erro de conexão :("

            for message in self.network.get():
                if message.tag == "game-name" and message.text == self.name:
                    self.choose_skin_screen()

            self.buttons["join_room.back"].update()
            self.buttons["join_room.join"].update()

            self.backgrounds["menu"].draw(self.canvas)
            self.texts["join_room.main"].draw(self.canvas)
            self.text_field.draw(self.canvas)
            self.buttons["join_room.back"].draw(self.canvas)
            self.buttons["join_room.join"].draw(self.canvas)
            self.canvas.update()

    def choose_skin_screen(self):
        skin_selected = False

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                elif event.type == pg.MOUSEBUTTONDOWN and self.network.is_host:
                    for skin_viewer in self.skin_viewers:
                        if skin_viewer.focused and not skin_selected:
                            skin_selected = True
                            self.player.load_images(f"images/{skin_viewer.name}/")
                            self.opponent.load_images(f"images/{self.get_couple_name(skin_viewer.name)}/")
                            self.network.send(tag="skin", message=skin_viewer.name)
                            self.match_screen()

            for message in self.network.get():
                # client network events
                if not self.network.is_host:
                    if message.tag == "skin":
                        self.player.load_images(f"images/{self.get_couple_name(message.text)}/")
                        self.opponent.load_images(f"images/{message.text}/")
                        self.match_screen()

            self.backgrounds["menu"].draw(self.canvas)
            if self.network.is_host:
                self.texts["choose_skin.choose"].draw(self.canvas)
                [skin_viewer.update() for skin_viewer in self.skin_viewers if not skin_selected]
                [skin_viewer.draw(self.canvas) for skin_viewer in self.skin_viewers]
            else:
                self.texts["choose_skin.waiting"].draw(self.canvas)

            self.canvas.update()

    def match_screen(self):
        self.is_match_executor_running = False
        self.player.spawn(640, 360)
        if not self.network.is_host:
            self.network.send(tag="start", message="match_executor")
            
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

                elif event.type == self.events["ping_request"]:
                    self.network.send(tag="ping", message="request")
                    self.network.time_of_ping_request = time.time()

            for message in self.network.get():
                if message.tag == "player":
                    self.opponent.load_json(message.text)

                elif message.tag == "ping":
                    if message.text == "request":
                        self.network.send(tag="ping", message="response")

                    elif message.text == "response":
                        ping = int((time.time() - self.network.time_of_ping_request) * 1000)
                        self.texts["match.ping"].text = f"Ping: {ping} ms"

                # host network events
                if self.network.is_host:
                    if message.tag == "start" and message.text == "match_executor":
                        self.async_run(self.match_executor)

                # client network events
                else:
                    if message.tag == "platform":
                        self.platform.load_json(message.text)
                        self.async_run(self.match_executor)

            if not self.network.active and not self.is_match_executor_running:
                if self.network.is_host:
                    self.create_room_screen()
                else:
                    self.join_room_screen()

            if time.time() - self.player.time_of_last_data_sync > 0.5:
                self.player.send_json(self.network)

            if not self.opponent.active:
                self.canvas.update()
                continue

            self.player.update(collision_blocks=self.platform.active_slots + self.side_barriers)
            self.opponent.update(collision_blocks=self.platform.active_slots + self.side_barriers)

            self.backgrounds["game"].draw(self.canvas)
            self.platform.draw(self.canvas)
            self.opponent.draw(self.canvas)
            self.player.draw(self.canvas)
            self.texts["match.main"].draw(self.canvas)
            self.progress_bar.draw(self.canvas)
            self.rectangles["match.info_bg"].draw(self.canvas)
            self.texts["match.round"].draw(self.canvas)
            self.texts["match.timeout"].draw(self.canvas)
            self.texts["match.ping"].draw(self.canvas)
            self.canvas.update()

    def match_executor(self):
        self.is_match_executor_running = True

        if self.network.is_host:
            self.platform.update()
            self.platform.send_json(self.network)

        self.texts["match.round"].text = f"Rodada:  {self.platform.level}"
        self.texts["match.timeout"].text = f"Tempo limite:  {self.platform.timeout}s"

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

        # in order to close the thread safely - the player needs to wait until the end of the level
        if not self.network.active:
            self.is_match_executor_running = False
            return

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

    def get_couple_name(self, name):
        return {
            "lonelybryxn": "melyniu",
            "melyniu": "lonelybryxn"
        } [name]
        
game = Game()
game.run()