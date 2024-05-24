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
        self.lives = 3

        # Initial Position
        self.rect = self.image.get_rect(midbottom=paddle.rect.midtop)
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), -1)
        self.speed = 10

        # Active
        self.active = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.active:
            self.active = True

        # Cheat to retrieve the ball
        elif keys[pygame.K_DOWN]:
            self.active = False
            self.direction = pygame.math.Vector2(uniform(0, 0), -1)
            self.rect.midbottom = self.paddle.rect.midtop

    def screen_collision(self):
        # Left or Right corner of screen
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x *= -1
        # Left or Right part of the screen
        elif self.rect.right >= WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.direction.x *= -1
        # Top part of the screen
        elif self.rect.top <= 0:
            self.direction.y *= -1
        # Bottom part of screen. First pixel is top left of the screen.
        elif self.rect.top > WINDOW_HEIGHT:
            # self.lives -= 1
            if self.lives == 0:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            # Resets position and directions
            self.rect.midbottom = self.paddle.rect.midtop
            self.direction = pygame.math.Vector2(uniform(-3, 3), -1)
            self.active = False

    def paddle_collision(self):
        if self.rect.colliderect(self.paddle.rect):
            # Handling ball collision with side of the paddle
            if self.rect.centery > self.paddle.rect.centery*1.02:  # 2% more to compensate for sprite not being rect.
                self.rect.top = self.paddle.rect.bottom
            else:
                self.rect.bottom = self.paddle.rect.top

            # Handling ball collision with top of the paddle
            offset = (self.rect.centerx - self.paddle.rect.centerx) / (
                        self.paddle.rect.width / 0.75)  # not sure why 0.75
            # Offset in range [-0.4, 0.4]
            offset = max(-0.4, min(offset, 0.4))

            # Change ball direction to go upwards
            self.direction.y *= -1
            # Change ball direction based on the offset (where the ball hit the paddle)
            if abs(offset) > 0.38:  # If hit is near the edges
                self.direction.x = offset * 1.7  # Increase angle near edges
            else:
                self.direction.x = offset * 1.3

            # Get rid of the ball getting stuck bouncing on the sides off the paddle
            max_x_direction = 1
            self.direction.x = max(-max_x_direction, min(self.direction.x, max_x_direction))


    def brick_collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        for block in overlap_sprites:
            # Horizontal Collision
            # Right of the ball colliding into the left of another sprite
            if self.rect.right >= block.rect.left and self.previous_rect.right <= block.previous_rect.left:
                self.rect.right = block.rect.left - 1
                self.direction.x *= -1
            # Left of the ball colliding into the right of another sprite
            if self.rect.left <= block.rect.right and self.previous_rect.left >= block.previous_rect.right:
                self.rect.left = block.rect.right + 1
                self.direction.x *= -1

            # Vertical Collision
            # Top of the ball colliding into the bottom of another sprite
            if self.rect.top <= block.rect.bottom and self.previous_rect.top >= block.previous_rect.bottom:
                self.rect.top = block.rect.bottom + 1
                self.direction.y *= -1
            # Bottom of the ball colliding into the top of another sprite
            if self.rect.bottom >= block.rect.top and self.previous_rect.bottom <= block.previous_rect.top:
                self.rect.bottom = block.rect.top - 1
                self.direction.y *= -1

            # Deal damage to the block if it has a strength attribute
            if hasattr(block, 'strength'):
                block.damage()

    def update(self):
        self.input()
        if self.active:
            # Normalize the direction if it is moving diagonally (almost always the case)
            # Without normalizing it, the ball would move way faster when in long diagonals
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # Save last frame's rect position
            self.previous_rect = self.rect.copy()

            # Update position and check for collisions
            self.rect.topleft += self.direction * self.speed
            self.paddle_collision()
            self.brick_collision()
            self.screen_collision()
        else:
            self.rect.midbottom = self.paddle.rect.midtop
