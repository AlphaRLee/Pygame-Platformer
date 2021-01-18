import pygame
from colors import ALPHA

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, images):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, width, height)
        self.left_image = images["grass_floating_left"]
        self.right_image = images["grass_floating_right"]
        self.center_images = [images["grass_floating0"], images["grass_floating1"], images["grass_floating2"]]

        self.image = self.build_image()

    def build_image(self):
        scaled_width = self.rect.height # Inflate the image evenly
        image_width = 32

        blits_data = [
            (pygame.transform.scale(self.left_image, (scaled_width, self.rect.height)), (0, 0, scaled_width, self.rect.height)),
            (pygame.transform.scale(self.right_image, (scaled_width, self.rect.height)), (self.rect.width - scaled_width, 0, scaled_width, self.rect.height))
        ]

        # TODO: Fix assumption where width is always a multiple of scaled_width
        for i in range(1, self.rect.width // scaled_width - 1):
            img = pygame.transform.scale(self.center_images[(i - 1) % len(self.center_images)], (scaled_width, self.rect.height))
            x = i * scaled_width
            blits_data.append((img, (x, 0, scaled_width, self.rect.height)))

        output_image = pygame.Surface((self.rect.width, self.rect.height))
        output_image.blits(blits_data)
        output_image = output_image.convert_alpha()
        output_image.set_colorkey(ALPHA)
        return output_image
