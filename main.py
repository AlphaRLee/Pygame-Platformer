"""Main file"""
import sys
import os
import json  # Used to import levels.json
import pygame
from player import Player
from level import Level
from platform import Platform
from colors import ALPHA
from physics import FPS

"""
SETUP
"""    
def load_platform_images():
    platform_images = {}
    image_names = ["grass_floating_left", "grass_floating_right"]
    for i in range(3):
        image_names.append("grass_floating" + str(i))

    for image_name in image_names:
        img = pygame.image.load(os.path.join("images", image_name + ".png"))
        img = img.convert_alpha()
        img.set_colorkey(ALPHA)
        platform_images[image_name] = img
    return platform_images

def load_levels(levels_file):
    with open(levels_file) as f:
        return json.load(f)


clock = pygame.time.Clock()
pygame.init()

screen_width, screen_height = 960, 720
world = pygame.display.set_mode((screen_width, screen_height))
world.set_alpha(0)  # Set the world screen to treat alpha as 0 (fully transparent)
backdrop = pygame.image.load(os.path.join('images', 'stage.png')).convert_alpha()
backdrop = pygame.transform.scale(backdrop, (screen_width, screen_height))
backdrop_box = world.get_rect()

platform_images = load_platform_images()
levels_data = load_levels("levels.json")

level = Level(levels_data[0])
platforms = level.spawn_platforms(platform_images)
enemies = level.spawn_enemies()

player = Player(level)
player.rect.x = 200
player.rect.y = 500
players = pygame.sprite.Group()
players.add(player)

ropes = pygame.sprite.Group()


def main():
    # Paint the backdrop image onto the backdrop box
    # This should belong in the draw section, but it's convenient to blit the backdrop here 
    # because the udpate section can cheat and draw on the screen if needed (for debugging)
    world.blit(backdrop, backdrop_box)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            on_key_down(event.key)
        if event.type == pygame.KEYUP:
            on_key_up(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            on_mouse_down()
        if event.type == pygame.MOUSEBUTTONUP:
            on_mouse_up()

    player.update()
    enemies.update()  # Invoke the update() on every enemy
    ropes.update()

    players.draw(world)
    platforms.draw(world)
    enemies.draw(world)
    ropes.draw(world)
    pygame.display.flip()
    clock.tick(FPS)


def quit():
    pygame.quit()
    sys.exit()

def on_key_down(key):
    if key == ord('q'):
        quit()

    if key == pygame.K_LEFT or key == ord('a'):
        player.walk(-player.walk_speed)
    if key == pygame.K_RIGHT or key == ord('d'):
        player.walk(player.walk_speed)
    if key == pygame.K_UP or key == ord('w'):
        player.jump()

def on_key_up(key):
    if key == pygame.K_LEFT or key == ord('a'):
        player.walk(player.walk_speed)
    if key == pygame.K_RIGHT or key == ord('d'):
        player.walk(-player.walk_speed)

def on_mouse_down():
    ropes.add(player.launch_rope(pygame.mouse.get_pos()))

def on_mouse_up():
    if player.rope:
        ropes.remove(player.rope)
        player.remove_rope()


while True:
    main()
