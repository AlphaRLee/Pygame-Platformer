'''
Player class
'''

import os
import pygame
import level

class Player(pygame.sprite.Sprite):
    def __init__(self, level=None):
        pygame.sprite.Sprite.__init__(self)

        self.walk_image_count = 4
        self.walk_images = []
        self.walk_frame = 0
        self.walk_image_duration = 4

        self.speed = { 'x': 0, 'y': 0 }
    
        self.walk_speed = 10

        height_to_width = 46 / 86   # Pixel dimensions
        for i in range(self.walk_image_count):
            img = pygame.image.load(os.path.join('images', 'player_walk' + str(i) + '.gif')).convert()
            img = pygame.transform.scale(img, (int(100 * height_to_width), 100))
            self.walk_images.append(img)

        self.image = self.walk_images[0]
        self.rect = self.image.get_rect()
        self.prev_rect = self.rect.copy()

        self.health = 5
        self.invincible_counter = 0

        self.level = level

    def update(self):
        self.move()
        self.apply_gravity()
        self.handle_hit_platform()
        self.decrement_invicible_counter()
        self.handle_hit_enemy()

    def move(self):
        self.prev_rect.x = self.rect.x
        self.prev_rect.y = self.rect.y
        self.rect.x = int(self.rect.x + self.speed['x'])
        self.rect.y = int(self.rect.y + self.speed['y'])

        if self.speed['x'] != 0:
            self.__animate_walking(to_left=self.speed['x'] < 0)
        else:
            self.walk_frame = 0

    def set_speed(self, x, y):
        self.speed['x'] = x
        self.speed['y'] = y

    def add_speed(self, x, y):
        self.speed['x'] += x
        self.speed['y'] += y

    def apply_gravity(self):
        self.add_speed(0, 2)

    def jump(self):
        if self.is_jumping:
            return
        self.set_speed(self.speed['x'], - 25)
        self.is_jumping = True

    def handle_hit_platform(self):
        if not self.level or not self.level.platforms:
            return
        
        hit_platforms = pygame.sprite.spritecollide(self, self.level.platforms, dokill=False)
        for platform in hit_platforms:
            if self.prev_rect.bottom <= platform.rect.y:
                self.set_speed(self.speed['x'], 0)
                self.rect.y = platform.rect.y - self.rect.height
                self.is_jumping = False

    # Check if the player had hit any enemies
    def handle_hit_enemy(self):
        if not self.level or not self.level.enemies or self.invincible_counter > 0:
            return
        
        if pygame.sprite.spritecollideany(self, self.level.enemies):
            self.take_damage(1)

    def decrement_invicible_counter(self):
        if self.invincible_counter > 0: 
            self.invincible_counter -= 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health > 0:
            invincible_counter_on_hit = 10
            if self.invincible_counter < invincible_counter_on_hit:
                self.invincible_counter = invincible_counter_on_hit
            
            # TODO: Animate player getting hurt, knocked backwards,
            print("Ouch! You have " + str(self.health) + " HP left")
        else:
            self.health = 0  # Explicitly set to zero (disallow negative HP)
            print("Uh oh, you died!")

    def __animate_walking(self, to_left=False):
        self.walk_frame += 1

        # Reset walk_frame every walk_image_count * walk_image_duration frames (i.e. every 4*4 = 16 frames)
        self.walk_frame %= self.walk_image_count * self.walk_image_duration
        # Every walk animation lasts for several frame. Do integer division to select the correct frame
        self.image = self.walk_images[self.walk_frame // self.walk_image_duration]
        if to_left:
            self.image = pygame.transform.flip(self.image, True, False)

