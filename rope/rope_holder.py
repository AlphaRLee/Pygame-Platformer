import pygame

class RopeHolder:
    def __init__(self, owner, offset):
        self.owner = owner
        self.offset = offset
        self.move_to_owner()

    @property
    def mass(self):
        return self.owner.mass

    @property
    def speed(self):
        return (self.owner.speed['x'], self.owner.speed['y'])

    def on_anchor(self):
        self.owner.has_gravity = False

    def move_to_owner(self):
        self.x = self.owner.x + self.offset[0]
        self.y = self.owner.y + self.offset[1]

    def rope_set_position(self, x, y):
        self.owner.set_speed(x - self.x, y - self.y)
        