import pygame
import pathlib
from source import settings


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # image is mandatory attribute for pygame sprites.
        self.textures = []
        for image in pathlib.Path('assets/images/paddle').glob('*.png'):
            texture = pygame.image.load(image)
            texture = pygame.transform.scale(texture, (settings.WINDOW_WIDTH // 10, settings.WINDOW_HEIGHT // 20))
            texture.set_colorkey((0, 0, 0))
            self.textures.append(texture)
        self.cur_img = 0
        self.image = self.textures[self.cur_img]

        # Initial Parameters
        self.rect = self.image.get_rect(midbottom=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.speed = 10

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < settings.WINDOW_WIDTH:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] and self.rect.left > 0:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.previous_rect = self.rect.copy()
        self.input()
        self.rect.x += self.direction.x * self.speed
        # Paddle Animation
        if self.cur_img > len(self.textures):
            self.cur_img = 0
        self.cur_img += 0.05
        self.image = self.textures[int(self.cur_img) % len(self.textures)]
