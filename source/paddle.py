import pygame
from settings import *


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        # Setup
        # image is mandatory attribute for pygame sprites.
        self.image = pygame.Surface((WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        self.image.fill('green')

        # Initial Parameters
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.speed = 10

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] and self.rect.left > 0:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):
        self.previous_rect = self.rect.copy()
        self.input()
        self.rect.x += self.direction.x * self.speed
