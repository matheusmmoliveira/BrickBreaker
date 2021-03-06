import pygame
from settings import *
from random import uniform


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle, blocks):
        super().__init__(groups)
        # Setup
        # image is mandatory attribute for pygame sprites.
        self.image = pygame.image.load(BASE_DIR / 'assets' / 'imgs' / 'ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.paddle = paddle
        self.blocks = blocks

        # Initial Position
        self.rect = self.image.get_rect(midbottom=paddle.rect.midtop)
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(uniform(-5, 5), -1)
        self.speed = 10

        # Active
        self.active = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.active = True
        elif keys[pygame.K_DOWN]:
            self.active = False
            self.direction = pygame.math.Vector2(uniform(-5, 5), -1)

    def screen_collision(self):
        # Left part of the screen
        if self.rect.left <= 0:
            self.direction.x *= -1
        # Right part of the screen
        elif self.rect.right >= WINDOW_WIDTH:
            self.direction.x *= -1
        # Top part of the screen
        elif self.rect.top <= 0:
            self.direction.y *= -1
        # Bottom part of screen.
        elif self.rect.bottom > WINDOW_HEIGHT:
            self.direction.y *= -1
            self.active = False

    def collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.paddle.rect):
            overlap_sprites.append(self.paddle)

        if overlap_sprites:
            for sprite in overlap_sprites:
                # Horizontal Collision
                # Right of the ball colliding into the left of another sprite
                if self.rect.right >= sprite.rect.left and self.previous_rect.right <= sprite.previous_rect.left:
                    self.rect.right = sprite.rect.left - 1
                    self.direction.x *= -1
                # Left of the ball collinding into the right of another sprite
                if self.rect.left <= sprite.rect.right and self.previous_rect.left >= sprite.previous_rect.right:
                    self.rect.left = sprite.rect.right + 1
                    self.direction.x *= -1
                # Vertical Collision
                # Top of the ball collinding into the bottom of another sprite
                if self.rect.top <= sprite.rect.bottom and self.previous_rect.top >= sprite.previous_rect.bottom:
                    self.rect.top = sprite.rect.bottom + 1
                    self.direction.y *= -1
                # Bottom of the ball collinding into the top of another sprite
                if self.rect.bottom >= sprite.rect.top and self.previous_rect.bottom <= sprite.previous_rect.top:
                    self.rect.bottom = sprite.rect.top - 1
                    self.direction.y *= -1

                # Check if sprite is a block with attribute strenght. Getattr calls Hasattr.
                if getattr(sprite, 'strength', None):
                    sprite.damage()

    def update(self):
        self.input()
        if self.active:
            # Normalize the direction if it is moving diagonally (almost always the case)
            # Withot normalizing it, the ball would move way faster when in long diagonals
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # Save last frame's rect position
            self.previous_rect = self.rect.copy()

            # Update position and check for collisions
            self.rect.topleft += self.direction * self.speed
            self.screen_collision()
            self.collision()
        else:
            self.rect.midbottom = self.paddle.rect.midtop
