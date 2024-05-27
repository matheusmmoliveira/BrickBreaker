from random import uniform
from source.settings import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, initial_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.95)):
        # Call the parent class (Sprite) constructor
        super().__init__(groups)

        # image is mandatory attribute for pygame sprites.
        self.image = pygame.image.load('assets/images/ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Initial Configuration
        self.rect = self.image.get_frect(midbottom=initial_pos)
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(uniform(-1, 1), -1)
        self.speed = 500

        # Active
        self.active = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.active:
            self.active = True

    def move(self, dt):
        if self.active:
            # Normal vector for keep momentum in diagonals
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.rect.center += self.direction * self.speed * dt
            self.collisions()

    def collisions(self):
        # Check for collision with screen boundaries
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.direction.x *= -1
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
        if self.rect.top <= 0:
            self.direction.y *= -1
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= WINDOW_HEIGHT:
                self.rect.bottom = WINDOW_HEIGHT
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

    def update(self, dt):
        self.previous_rect = self.rect.copy()  # Save last frame's rect position
        self.input()
        self.move(dt)
