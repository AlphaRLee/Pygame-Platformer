import pygame

class RopeHolder:
    # def __init__(self, owner, offset):
    def __init__(self, owner, offset, temp_screen):  # FIXME: Delete
        self.temp_screen = temp_screen  # FIXME: Delete
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
        scale = 10
        pygame.draw.line(self.temp_screen, (0, 0, 0), 
                         (self.x, self.y), 
                         (self.x + int((x - self.x) * scale), self.y + int((y - self.y) * scale)), 1) # FIXME: Delete
        self.owner.set_speed(x - self.x, y - self.y)
        