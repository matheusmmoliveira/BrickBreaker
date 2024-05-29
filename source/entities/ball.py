from random import uniform
from source.settings import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, collisions_sprites: pygame.sprite.Group, initial_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.95)):
        # Call the parent class (Sprite) constructor
        super().__init__(groups)

        # image is a mandatory attribute for pygame sprites.
        self.image = pygame.image.load('assets/images/ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Initial Configuration
        self.collisions_sprites = collisions_sprites
        self.rect = self.image.get_frect(midbottom=initial_pos)
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(uniform(-1, 1), -1)
        self.speed = 12

        # Active
        self.active = True

    def move(self):
        # Normal vector for keep momentum in diagonals
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * self.speed

    def check_collisions(self):
        # Check collisions with any other sprite
        for sprite in self.collisions_sprites:
            if self.rect.bottom >= sprite.rect.top and self.previous_rect.bottom >= sprite.previous_rect.top:
                self.rect.bottom = sprite.rect.top
                self.direction.y *= -1
        # Check collisions with screen boundaries
        # Left side or right side of the screen
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.direction.x *= -1
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
        # Top of the screen
        if self.rect.top <= 0:
            self.direction.y *= -1
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= WINDOW_HEIGHT:
                self.rect.bottom = WINDOW_HEIGHT
        # Falls off the bottom of the screen
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.active = False
            self.kill()

    def update(self):
        self.previous_rect = self.rect.copy()  # Save last frame's rect position
        self.move()
        self.check_collisions()
