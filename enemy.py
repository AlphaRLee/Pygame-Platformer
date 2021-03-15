'''
Enemy class
'''

import os
import pygame
from colors import ALPHA

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.width = 50
        self.height = 50

        self.walk_image_count = 6
        self.walk_images = []
        self.walk_frame = 0
        self.walk_image_duration = 4
        self.walk_speed = 4

        self.max_pace_counter = 150
        self.pace_counter = self.max_pace_counter // 4
        
        self.speed = { 'x': self.walk_speed, 'y': 0 }
    
        for i in range(self.walk_image_count):
            img = pygame.image.load(os.path.join('images', 'enemy_walk' + str(i) + '.png')).convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            img.set_colorkey(ALPHA)
            self.walk_images.append(img)

        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.speed['x']
        self.rect.y += self.speed['y']

        if self.speed['x'] != 0:
            self.animate_walking(to_left=self.speed['x'] < 0)
        else:
            self.walk_frame = 0

        self.pace_back_and_forth()

    def control(self, x, y):
        self.speed['x'] += x
        self.speed['y'] += y

    def pace_back_and_forth(self):
        self.pace_counter += 1
        self.pace_counter %= self.max_pace_counter
        if self.pace_counter == 0:
            self.control(self.walk_speed * 2, 0)
        elif self.pace_counter == self.max_pace_counter // 2:
            self.control(- self.walk_speed * 2, 0)

    def animate_walking(self, to_left=False):
        self.walk_frame += 1
        self.walk_frame %= self.walk_image_count * self.walk_image_duration
        self.image = self.walk_images[self.walk_frame // self.walk_image_duration]
        if to_left:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image.convert_alpha()
            self.image.set_colorkey(ALPHA) 
            

