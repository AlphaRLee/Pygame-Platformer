'''
Player class
'''

import os
import pygame
import level
from physics import DT, GRAVITY
from rope.rope import Rope

class Player(pygame.sprite.Sprite):
    # def __init__(self, level=None):
    def __init__(self, level=None, temp_screen=None):  # FIXME: Delete
        pygame.sprite.Sprite.__init__(self)

        self.ROPE_RELEASE_KEY = 'ROPE_RELEASE'

        self.temp_screen = temp_screen  # FIXME: Delete
        self.mass = 10

        self.walk_image_count = 4
        self.walk_images = []
        self.walk_frame = 0
        self.walk_image_duration = 4

        self.speed = { 'x': 0, 'y': 0 }

        # Environment speed is defined by speed not dierctly under player's control (e.g. momentum from releasing the rope)
        # TODO: Integrate gravity into this to be cohesive
        self.env_speeds = {}

        self.has_gravity = True
    
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

        self.rope = None
        self.rope_offset = pygame.Vector2(self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2)

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, val):
        self.rect.x = val

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, val):
        self.rect.y = val

    def add(self, groups):
        super().add(groups)
        self.add_children(groups)

    def remove(self, groups):
        super().remove(groups)
        self.remove_children(groups)

    def add_children(self, groups):
        self.head_sprite.add(groups)

    def remove_children(self, groups):
        self.head_sprite.remove(groups)

    def update(self):
        self.update_prev_rect()
        self.add_to_position(self.speed['x'], self.speed['y'])
        self.apply_env_speeds()
        self.apply_gravity()
        self.handle_hit_platforms()
        self.decrement_invicible_counter()
        self.handle_hit_enemy()
        self.update_rope_offset()

    def update_prev_rect(self):
        self.prev_rect.x = self.rect.x
        self.prev_rect.y = self.rect.y

    def set_position(self, x, y):
        self.rect.x = int(x)
        self.rect.y = int(y)

        if self.speed['x'] != 0:
            self.animate_walking(to_left=self.speed['x'] < 0)
        else:
            self.walk_frame = 0

    def add_to_position(self, x, y):
        self.set_position(self.rect.x + x, self.rect.y + y)

    def set_speed(self, x, y):
        self.speed['x'] = x
        self.speed['y'] = y

    def add_speed(self, x, y):
        self.speed['x'] += x
        self.speed['y'] += y

    def get_env_speed(self, env_key):
        if env_key in self.env_speeds:
            return self.env_speeds[env_key]
        else:
            return None

    # Add an environment speed.
    def set_env_speed(self, env_key, x, y):
        self.env_speeds[env_key] = {'x': x, 'y': y}

    # Delete an environment speed. Does nothing if key is not found
    def remove_env_speed(self, env_key):
        if env_key in self.env_speeds:
            del self.env_speeds[env_key]

    def apply_env_speeds(self):
        total_speed = {'x': 0, 'y': 0}
        for speed in self.env_speeds.values():
            total_speed['x'] += speed['x']
            total_speed['y'] += speed['y']
        self.add_to_position(total_speed['x'], total_speed['y'])

    def apply_gravity(self):
        if self.has_gravity:
            self.add_speed(0, self.mass * GRAVITY * DT)

    def update_rope_offset(self):
        if not self.rope:
            return
        self.rope.rope_holder.move_to_owner()

    def jump(self, jump_speed=-25, check_is_jumping=True):
        if check_is_jumping and self.is_jumping:
            return
        self.set_speed(self.speed['x'], jump_speed)
        self.is_jumping = True

    def launch_rope(self, target):
        # self.rope = Rope(self, (self.rect.width, self.rect.height // 2), target, self.level)
        self.rope = Rope(self, (self.rect.width, self.rect.height // 2), target, self.level, temp_screen=self.temp_screen)  # FIXME: delete
        self.set_speed(0, 0)  # TODO: Calculate the tangent speed to rope
        return self.rope

    def remove_rope(self):
        self.rope = None
        self.has_gravity = True
        self.set_env_speed(self.ROPE_RELEASE_KEY, self.speed['x'], self.speed['y'])
        self.set_speed(0, 0)

    def handle_hit_platforms(self):
        if not self.level or not self.level.platforms:
            return
        
        hit_platforms = pygame.sprite.spritecollide(self, self.level.platforms, dokill=False)
        for platform in hit_platforms:
            self.on_hit_platform(platform)

    def on_hit_platform(self, platform):
        if self.prev_rect.y + self.prev_rect.height > platform.rect.y:
            return

        self.set_speed(self.speed['x'], 0)
        self.rect.y = platform.rect.y - self.rect.height
        self.is_jumping = False
        self.reduce_rope_release_speed()

    # Kill any momentum gained from releasing the rope        
    # Y speed is always set to zero
    # If x speed is currently less than remove_threshold, the rope speed is removed altogether
    def reduce_rope_release_speed(self, remove_threshold=1, reduce_factor=0.7):
        rope_release_speed = self.get_env_speed(self.ROPE_RELEASE_KEY)
        if not rope_release_speed:
            return

        if abs(rope_release_speed['x']) < remove_threshold:
            self.remove_env_speed(self.ROPE_RELEASE_KEY)

        self.set_env_speed(self.ROPE_RELEASE_KEY, rope_release_speed['x'] * reduce_factor, 0)

    # Check if the player had hit any enemies
    def handle_hit_enemy(self):
        if not self.level or not self.level.enemies or self.invincible_counter > 0:
            return
        
        for enemy in pygame.sprite.spritecollide(self, self.level.enemies, dokill=False):
            if self.rect.y + self.rect.height <= enemy.rect.y + 10:
                enemy.kill()
                self.jump(jump_speed=-20, check_is_jumping=False)
            else:
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

    def animate_walking(self, to_left=False):
        self.walk_frame += 1

        # Reset walk_frame every walk_image_count * walk_image_duration frames (i.e. every 4*4 = 16 frames)
        self.walk_frame %= self.walk_image_count * self.walk_image_duration
        # Every walk animation lasts for several frame. Do integer division to select the correct frame
        self.image = self.walk_images[self.walk_frame // self.walk_image_duration]
        if to_left:
            self.image = pygame.transform.flip(self.image, True, False)

