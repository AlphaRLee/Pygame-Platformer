import pygame
from platform import Platform
from enemy import Enemy

class Level:
    # TODO: Implement features
    #   platforms
    #   enemies spawn 
    
    def __init__(self, level_data):
        self.id = level_data['id']
        self.platforms_data = level_data['platforms']
        self.enemies_data = level_data['enemies']
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def spawn_platforms(self, platform_images):
        for platform_data in self.platforms_data:
            platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'], platform_images)
            self.platforms.add(platform)

        return self.platforms

    def spawn_enemies(self):
        for enemy_data in self.enemies_data:
            enemy = Enemy(enemy_data['x'], enemy_data['y'])
            self.enemies.add(enemy)

        return self.enemies
