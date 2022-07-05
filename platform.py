from email import message
import pygame as pg
import os
import random
import json

class Platform:
    def __init__(self, images_folder_url, hotspot, x, y):
        self.images = {}
        self.load_images(images_folder_url)
        self.color_list = list(self.images.keys())
        self.rect = self.get_rect(hotspot, x, y)
        self.slots = self.get_slots()
        self.active_slots = self.slots.copy()
        self.timeout_list = [10, 9, 8, 7, 6, 5, 4.5, 4, 3.5, 3, 2.5, 2]
        self.level = 1
        self.timeout = None
        self.chosen_color = None

    def load_images(self, images_folder_url):
        for file in os.listdir(images_folder_url):
            img_name = os.path.splitext(file)[0]
            img_url = images_folder_url + file
            img_surf = pg.image.load(img_url).convert_alpha()
            self.images[img_name] = img_surf

    def get_rect(self, hotspot, x, y):
        first_image_width = list(self.images.values())[0].get_width()
        first_image_height = list(self.images.values())[0].get_height()

        for image in self.images.values():
            if (image.get_width() != first_image_width) or (image.get_height() != first_image_height):
                raise Exception("All the blocks needs to have the same width an height!")

        rect = pg.Rect(0, 0, first_image_width*len(self.images), first_image_height)
        setattr(rect, hotspot, (x,y))
        return rect

    def get_slots(self):
        block_width = self.rect.width // len(self.images)
        block_height = self.rect.height
        return [
            pg.Rect(col*block_width + self.rect.x, self.rect.y, block_width, block_height)
            for col,_ in enumerate(self.images)
        ]

    def destroy(self):
        self.active_slots = [self.slots[self.color_list.index(self.chosen_color)]]

    def update(self):
        random.shuffle(self.color_list)
        self.chosen_color = random.choice(self.color_list)
        if self.level <= len(self.timeout_list): self.timeout = self.timeout_list[self.level - 1]
        else: self.timeout = self.timeout_list[-1]
        self.active_slots = self.slots.copy()

    def draw(self, canvas):
        for index,color in enumerate(self.color_list):
            if self.slots[index] in self.active_slots:
                canvas.blit(self.images[color], self.slots[index])

    def send_json(self, network):
        data = {
            "level": self.level,
            "color_list": self.color_list,
            "chosen_color": self.chosen_color,
            "timeout": self.timeout
        }
        json_text = json.dumps(data, separators=(",", ":"))
        network.send(tag="platform", message=json_text)

    def load_json(self, json_text):
        data = json.loads(json_text)
        self.level = data["level"]
        self.color_list = data["color_list"]
        self.chosen_color = data["chosen_color"]
        self.timeout = data["timeout"]
        self.active_slots = self.slots.copy()