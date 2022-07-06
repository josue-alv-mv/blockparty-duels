import pygame as pg
import os
import time
import math

class Player:
    def __init__(
        self, animation_speed, rect_width, rect_height, speed, gravity_speed
    ):
        self.animation_speed = animation_speed
        self.rect = pg.Rect(0, 0, rect_width, rect_height)
        self.speed = speed
        self.gravity_speed = gravity_speed
        self.vectory = 0
        self.animate = False
        self.mirrored = False
        self.time_of_last_update = None
        self.default = { "animation_speed": animation_speed }

    def load_images(self, images_folder_url):
        # tries to add from 1.png to x.png being x the number of files in the folder
        self.images = []
        files = os.listdir(images_folder_url)

        for n in range(1, len(files) + 1):
            img_url = images_folder_url + f"{n}.png"
            img_surf = pg.image.load(img_url).convert_alpha()
            self.images.append(img_surf)

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def update(self, collision_blocks):
        if self.time_of_last_update is None or time.time() - self.time_of_last_update >= 0.1:
            self.time_of_last_update = time.time()
            return

        elapsed_time = time.time() - self.time_of_last_update

        # apply horizontal movement
        old_x = self.x
        step_distance = self.speed * elapsed_time
        pressed_keys = self.get_pressed_keys()

        if pressed_keys in [ [], ["left", "right"] ]:
            self.animate = False

        elif pressed_keys == ["left"]:
            self.x -= step_distance
            self.mirrored = True
            self.animate = True

        elif pressed_keys == ["right"]:
            self.x += step_distance
            self.mirrored = False
            self.animate = True

        self.update_rect()
        if self.rect.collidelistall(collision_blocks):
            self.x = old_x
            self.update_rect()

        # apply vertical movement
        old_y = self.y
        self.y += elapsed_time * (self.gravity_speed + self.vectory)

        if self.vectory + 3*(self.gravity_speed * elapsed_time) <= 0:
            self.vectory += 3*(self.gravity_speed * elapsed_time)
            self.animation_speed = self.default["animation_speed"] // 2
            self.animate = True
        else:
            self.vectory = 0
            self.animation_speed = self.default["animation_speed"]

        self.update_rect()
        if self.rect.collidelistall(collision_blocks):
            # self.y = old_y
            colliding_rect = collision_blocks[self.rect.collidelist(collision_blocks)]
            if self.rect.bottom < colliding_rect.bottom:
                self.y = math.floor(colliding_rect.top - (self.rect.height / 2))
                self.update_rect()

        # finish
        self.time_of_last_update = time.time()

    def draw(self, canvas):
        if self.animate:
            animation_duration = len(self.images) / self.animation_speed
            frame = int( (time.time() % animation_duration) * (len(self.images) / animation_duration) )
        else:
            frame = 0

        surf = self.images[frame]
        rect = surf.get_rect(center = self.rect.center)
        if self.mirrored:
            surf = pg.transform.flip(surf, flip_x=True, flip_y=False)

        canvas.blit(surf, rect)