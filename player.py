import pygame as pg
import os
import time

class Player:
    def __init__(self, images_folder_url, animation_speed, rect_width, rect_height, speed, gravity_speed):
        self.images = []
        self.load_images(images_folder_url)
        self.animation_speed = animation_speed
        self.rect = pg.Rect(0, 0, rect_width, rect_height)
        self.speed = speed
        self.gravity_speed = gravity_speed
        self.vectory = 0
        self.animate = False
        self.mirrored = False
        self.time_of_last_update = None
        
    def load_images(self, images_folder_url):
        # tries to add from 1.png to x.png being x the number of files in the folder

        files = os.listdir(images_folder_url)

        for n in range(1, len(files) + 1):
            img_url = images_folder_url + f"{n}.png"
            img_surf = pg.image.load(img_url).convert_alpha()
            self.images.append(img_surf)

    def spawn(self, x, y):
        self.x = x
        self.y = y
        self.update_rect()

    def jump(self):
        self.vectory = -(2*self.gravity_speed)

    def update_rect(self):
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.time_of_last_update is None:
            self.time_of_last_update = time.time()
            return

        elapsed_time = time.time() - self.time_of_last_update

        # apply horizontal movement
        step_distance = self.speed * elapsed_time
        pressed_keys = pg.key.get_pressed()

        if pressed_keys[pg.K_LEFT]:
            self.x -= step_distance
            self.mirrored = True
            self.animate = True

        elif pressed_keys[pg.K_RIGHT]:
            self.x += step_distance
            self.mirrored = False
            self.animate = True

        else:
            self.animate = False

        # apply vertical movement
        self.y += elapsed_time * (self.gravity_speed + self.vectory)

        if self.vectory + 2*(self.gravity_speed * elapsed_time) <= 0:
            self.vectory += 2*(self.gravity_speed * elapsed_time)
        else:
            self.vectory = 0

        # update rect and time_of_last_update
        self.update_rect()
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