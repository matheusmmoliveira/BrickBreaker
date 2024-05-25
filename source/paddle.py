import pygame
import pathlib


class Paddle(pygame.sprite.Sprite):
    def __init__(self, win_width, win_height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self._window_width = win_width
        self._window_height = win_height

        # image is mandatory attribute for pygame sprites.
        self.textures = []
        for image in pathlib.Path('assets/images/paddle').glob('*.png'):
            texture = pygame.image.load(image)
            texture = pygame.transform.scale(texture, (self._window_width // 10, self._window_height // 20))
            texture.set_colorkey((0, 0, 0))
            self.textures.append(texture)
        self.cur_img = 0
        self.image = self.textures[self.cur_img]

        # Initial Parameters
        self.rect = self.image.get_rect(midbottom=(self._window_width // 2, self._window_height - 20))
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.speed = 10

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < self._window_width:
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
