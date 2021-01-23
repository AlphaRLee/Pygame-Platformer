'''
Physics calculator for swinging rope
Modeled after pendulum physics
'''

import math
import pygame
from physics import DT, GRAVITY

class SwingPhysics:
    # Initialize a new SwingPhysics calculator
    # rope: A rope object
    # body: The swinging body attached to the end of the rope
    def __init__(self, rope, rope_holder):
        self.rope = rope
        self.rope_holder = rope_holder

        self.down_vector = pygame.Vector2(0, 1)
        self.theta_velocity = 0
        self.calculate_theta()
    
    # Calculate theta (angle from anchor point to body) in radians
    def calculate_theta(self):
        self.rope_length, self.theta = self.rope.anchor_to_body().as_polar()
        
        # Convert azimuth (-180 to 180, 0 = x-axis, +y = down) to theta (-180 to 180, 0 = down, +theta = to the right)
        # 0 -> +90
        # 90 -> 0
        # 180 -> -90
        self.theta = 90 - self.theta
        if self.theta > 180:
            self.theta -= 360
        self.theta = math.radians(self.theta)

    def calculate_theta_velocity(self):
        self.gravity_force = - self.rope_holder.mass * GRAVITY
        self.theta_velocity += self.gravity_force * math.sin(self.theta) / self.rope_length * DT

    def update(self):
        self.calculate_theta()
        self.calculate_theta_velocity()
        self.update_theta()
        self.update_rope_holder_position()

    def update_theta(self):
        self.theta += self.theta_velocity

    def update_rope_holder_position(self):
        x = self.rope.anchor_point.x + self.rope_length * math.sin(self.theta)
        y = self.rope.anchor_point.y + self.rope_length * math.cos(self.theta)
        self.rope_holder.rope_set_position(x, y)
