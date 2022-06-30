import pygame as pg
import os
import random

class Platform:
    def __init__(self, images_folder_url, hotspot, x, y):
        self.images = {}
        self.load_images(images_folder_url)
        self.color_list = list(self.images.keys())
        self.rect = self.get_rect(hotspot, x, y)
        self.slots = self.get_slots()

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

    def shuffle(self):
        random.shuffle(self.color_list)

    def draw(self, canvas):
        for index,color in enumerate(self.color_list):
            canvas.blit(self.images[color], self.slots[index])