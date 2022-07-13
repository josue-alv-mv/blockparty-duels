import pygame as pg
import time
import json
from player import Player

class LocalPlayer(Player):
    def __init__(
        self, animation_speed, rect_width, rect_height, speed, gravity_speed
    ):
        super().__init__(animation_speed, rect_width, rect_height, speed, gravity_speed)
        self.mov_keys = [pg.K_LEFT, pg.K_RIGHT, pg.K_a, pg.K_d]
        self.jump_keys = [pg.K_UP, pg.K_w]
        self.time_of_last_data_sync = -1

    def spawn(self, x, y):
        self.x = x
        self.y = y
        self.update_rect()

    def get_pressed_keys(self):
        all_pressed_keys = pg.key.get_pressed()
        pressed_keys = []

        if all_pressed_keys[pg.K_LEFT] or all_pressed_keys [pg.K_a]:
            pressed_keys.append("left")

        if all_pressed_keys[pg.K_RIGHT] or all_pressed_keys[pg.K_d]:
            pressed_keys.append("right")

        return pressed_keys

    def request_jump(self, collision_blocks):
        trusted_rect = self.rect.copy()
        trusted_rect.height += 2

        if trusted_rect.collidelistall(collision_blocks):
            self.vectory = -(2*self.gravity_speed)
            return True

    def send_json(self, network, flags=[]):
        data = { "x": round(self.x, 1), "y": round(self.y, 1) }

        if "jump" not in flags:
            data["pressed_keys"] = self.get_pressed_keys()

        if flags:
            data["flags"] = flags

        json_text = json.dumps(data, separators=(",", ":"))
        network.send(tag="player", message=json_text)
        self.time_of_last_data_sync = time.time()