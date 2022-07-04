import json
from player import Player

class Opponent(Player):
    def __init__(self, animation_speed, rect_width, rect_height, speed, gravity_speed):
        super().__init__(animation_speed, rect_width, rect_height, speed, gravity_speed)
        self.pressed_keys = []
        self.active = False

    def get_pressed_keys(self):
        return self.pressed_keys

    def jump(self):
        self.vectory = -(2*self.gravity_speed)

    def load_json(self, json_text):
        data = json.loads(json_text)
        self.x = data["x"]
        self.y = data["y"]
        
        if "pressed_keys" in data:
            self.pressed_keys = data["pressed_keys"]

        if "flags" in data:
            if "jump" in data["flags"]:
                self.jump()

        self.update_rect()
        self.active = True