from source.settings import *
import pathlib
from source import settings
from source.entities.block import Block
from source.entities.paddle import Paddle
from source.entities.ball import Ball


class Level:
    def __init__(self, stage=1):
        self.screen = pygame.display.get_surface()
        self.stage = stage
        self.score = 0

        # Creating a dictionary of possible block textures using its name as key
        _files = pathlib.Path('assets/images/blocks').glob("*.png")
        self._textures = {file.stem: pygame.image.load(file).convert_alpha() for file in _files}

        # Sprite Group Setup
        self.world = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # Sprites
        self.paddle = Paddle(self.world)
        self.ball = Ball(self.world, initial_pos=self.paddle.rect.midtop)
        self.blocks = self.setup_blocks()

    def setup_blocks(self) -> pygame.sprite.Group:
        with open(f'assets/levels/{self.stage}.lvl', 'r') as level_file:
            block_map = [line.replace('\n', '') for line in level_file.readlines()]

        block_gap = 2
        blocks = pygame.sprite.Group()
        block_height = (settings.WINDOW_HEIGHT * 0.6) / len(block_map) - block_gap
        block_width = settings.WINDOW_WIDTH / len(block_map[0]) - block_gap
        for row_idx, row in enumerate(block_map):
            for col_idx, col in enumerate(row):
                if col != '*':
                    x = round(col_idx * (block_width + block_gap) + block_gap // 2)
                    y = round(row_idx * (block_height + block_gap) + block_gap // 2)
                    blocks.add(
                        Block(self.world, (block_width, block_height), int(col), (x, y), self._textures)
                    )

        return blocks

    def check_collisions(self):
        # Check collision between paddle and ball
        if self.paddle.rect.colliderect(self.ball):
            self.paddle_collision()

        # Check collision between ball and all bricks
        hit_bricks = pygame.sprite.spritecollide(self.ball, self.blocks, False)
        for hit_brick in hit_bricks:
            if hit_brick.rect.colliderect(self.ball.rect):
                self.brick_collision(hit_brick)

    def paddle_collision(self):
        offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / self.paddle.rect.width * 2
        offset = max(-0.9, min(offset, 0.9))
        # Upwards collision
        if self.ball.rect.bottom >= self.paddle.rect.top and self.ball.previous_rect.bottom <= self.paddle.previous_rect.top:
            self.ball.rect.bottom = self.paddle.rect.top
            self.ball.direction.y *= -1
            self.ball.direction.x += offset

    def brick_collision(self, brick):
        # Horizontal Collision
        # Right of the ball colliding into the left of another sprite
        if self.ball.rect.right >= brick.rect.left and self.ball.previous_rect.right <= brick.previous_rect.left:
            self.ball.rect.right = brick.rect.left - 1
            self.ball.direction.x *= -1
        # Left of the ball colliding into the right of another sprite
        if self.ball.rect.left <= brick.rect.right and self.ball.previous_rect.left >= brick.previous_rect.right:
            self.ball.rect.left = brick.rect.right + 1
            self.ball.direction.x *= -1

        # Vertical Collision
        # Top of the ball colliding into the bottom of another sprite
        if self.ball.rect.top <= brick.rect.bottom and self.ball.previous_rect.top >= brick.previous_rect.bottom:
            self.ball.rect.top = brick.rect.bottom + 1
            self.ball.direction.y *= -1
        # Bottom of the ball colliding into the top of another sprite
        if self.ball.rect.bottom >= brick.rect.top and self.ball.previous_rect.bottom <= brick.previous_rect.top:
            self.ball.rect.bottom = brick.rect.top - 1
            self.ball.direction.y *= -1

        # Deal damage to the block
        brick.damage()

    def run(self, dt):
        self.check_collisions()
        self.world.update(dt)
        self.world.draw(self.screen)
