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
    # rope_holder: The swinging body attached to the end of the rope
    def __init__(self, rope, rope_holder):
        self.rope = rope
        self.rope_holder = rope_holder

        self.down_vector = pygame.Vector2(0, 1)
        self.calculate_theta()
        self.calculate_instant_theta_velocity()


    # Calculate theta (angle from anchor point to body) in radians
    def calculate_theta(self):
        self.rope_length, azimuth = self.rope.anchor_to_body().as_polar()
    
        # Convert azimuth (-180 to 180, 0 = x-axis, +y = down) to theta (-180 to 180, 0 = down, +theta = to the right)
        # 0 -> +90
        # 90 -> 0
        # 180 -> -90
        self.theta = 90 - azimuth
        if self.theta > 180:
            self.theta -= 360
        self.theta = math.radians(self.theta)
        


    def calculate_theta_velocity(self):
        self.gravity_force = - self.rope_holder.mass * GRAVITY
        inc_theta_v = self.gravity_force * math.sin(self.theta) / self.rope_length * DT * 0.2
        self.theta_velocity += inc_theta_v

    # Calculate the theta v at the exact instant, not an iteration over time
    def calculate_instant_theta_velocity(self):
        speed = pygame.Vector2(self.rope_holder.speed)
        anchor_to_body_direction = self.rope.anchor_to_body().normalize()
        parallel_speed = speed.dot(anchor_to_body_direction) * anchor_to_body_direction  # Project the speed along the anchor_to_body direction
        theta_v_magnitude = (speed - parallel_speed).magnitude() / self.rope_length
        # FIXME: this line is broken, it keeps sending me to the right without it and opposite direction with speed.x. Line is still "loose" with -1 * theta, but travelling opposite directions will make a problem
        self.theta_velocity = math.copysign(theta_v_magnitude, - self.theta)  # Get the right direction by copying the speed's X component sign into the magnitude

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
