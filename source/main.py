import pygame
from settings import *
from paddle import Paddle
from ball import Ball
from level import Level
import sys


class BrickBreaker:
    def __init__(self):
        # Initial setup
        pygame.init()
        pygame.display.set_caption('Quebração de bloco')
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.fps = FPS

        # Background
        self.background = pygame.image.load(BASE_DIR / 'assets' / 'imgs' / 'background.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Sprite Group Setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        # Setup First Level
        level = Level()
        level.setup_level([self.all_sprites, self.block_sprites])
        # Setup Sprites in the Canvas
        self.paddle = Paddle(self.all_sprites)
        self.ball = Ball(self.all_sprites, self.paddle, self.block_sprites)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update the game
            self.all_sprites.update()
            # Draw frame
            self.canvas.blit(self.background, (0, 0))
            self.all_sprites.draw(self.canvas)

            pygame.display.update()


if __name__ == '__main__':
    game = BrickBreaker()
    game.run()
