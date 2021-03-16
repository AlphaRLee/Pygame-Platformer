import pygame
from rope.rope_holder import RopeHolder
from rope.swing_physics import SwingPhysics
from colors import ALPHA

class Rope(pygame.sprite.Sprite):
    def __init__(self, owner, offset, target, level, launch_speed=50, max_distance=800):
        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.rope_holder = RopeHolder(owner, offset)
        self.level = level

        self.launch_speed = launch_speed
        self.max_distance = max_distance
        self.distance = 0
        self.is_launching = True
        self.is_anchored = False
        self.anchor_point = None

        self.head_position = pygame.Vector2(self.rope_holder.x, self.rope_holder.y)
        self.head_sprite = pygame.sprite.Sprite()
        self.head_sprite.image = pygame.Surface((10, 10))
        self.head_sprite.image.fill((0, 0, 0))
        self.head_sprite.rect = self.head_sprite.image.get_rect()
        self.head_sprite.rect.x = int(self.head_position.x)
        self.head_sprite.rect.y = int(self.head_position.y)

        self.image = pygame.Surface((abs(self.head_position.x - self.rope_holder.x), abs(self.head_position.y - self.rope_holder.y)))
        self.rect = self.image.get_rect()

        self.launch_direction = pygame.Vector2(target[0] - self.rope_holder.x, target[1] - self.rope_holder.y).normalize()

        self.swing_physics = None
        self.can_swing = False

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
        if self.is_launching:
            self.launch()

        if self.swing_physics and self.can_swing:
            self.swing_physics.update()

        self.draw()

    def draw(self):
        x = min(self.rope_holder.x, self.head_position.x)
        y = min(self.rope_holder.y, self.head_position.y)
        width = abs(self.head_position.x - self.rope_holder.x)
        height = abs(self.head_position.y - self.rope_holder.y)
        self.image = pygame.Surface((width, height))
        self.image.fill(ALPHA)
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pygame.draw.line(self.image, (0, 0, 0), (self.rope_holder.x - x, self.rope_holder.y - y), (self.head_sprite.rect.x - x, self.head_sprite.rect.y - y), 2)

    def launch(self):
        if self.anchor_point:
            return

        self.head_position += self.launch_direction * self.launch_speed
        self.head_sprite.rect.x = int(self.head_position.x)
        self.head_sprite.rect.y = int(self.head_position.y)

        hit_platforms = pygame.sprite.spritecollide(self.head_sprite, self.level.platforms, dokill=False)
        for platform in hit_platforms:
            self.anchor_point = self.head_position
            self.is_launching = False
            self.is_anchored = True

        if self.is_anchored:
            self.swing_physics = SwingPhysics(self, self.rope_holder)
            self.rope_holder.on_anchor()
            self.can_swing = True
    
    def anchor_to_body(self) -> pygame.Vector2:
        return pygame.Vector2(self.rope_holder.x, self.rope_holder.y) - self.anchor_point

        

    