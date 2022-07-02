import pygame as pg
import time
import json
from player import Player

class LocalPlayer(Player):
    def __init__(
        self, images_folder_url, animation_speed, rect_width,
        rect_height, speed, gravity_speed, on_floor_confidence
    ):
        super().__init__(
            images_folder_url, animation_speed, rect_width, rect_height, speed, gravity_speed
        )
        self.on_floor_confidence = on_floor_confidence
        self.time_of_last_data_sync = -1

    def spawn(self, x, y):
        self.x = x
        self.y = y
        self.update_rect()

    def get_pressed_keys(self):
        all_pressed_keys = pg.key.get_pressed()
        pressed_keys = []

        if all_pressed_keys[pg.K_LEFT]:
            pressed_keys.append("left")

        if all_pressed_keys[pg.K_RIGHT]:
            pressed_keys.append("right")

        return pressed_keys

    def request_jump(self, collision_blocks):
        trusted_rect = self.rect.copy()
        trusted_rect.height += self.on_floor_confidence

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