import pygame
import settings
from paddle import Paddle
from ball import Ball
from level import Level
import sys


class BrickBreaker:
    def __init__(self):
        # Initial setup
        pygame.init()
        pygame.display.set_caption('Quebração de bloco')
        self.canvas = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.fps = settings.FPS

        # Background
        self.background = pygame.image.load(settings.BASE_DIR / 'assets' / 'imgs' / 'background.png').convert()
        self.background = pygame.transform.scale(self.background, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        # Sprite Group Setup
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # Setup First Level
        level = Level()
        level.setup_level([self.all_sprites, self.blocks])

        # Setup Sprites in the Canvas
        self.paddle = Paddle(self.all_sprites)
        self.ball = Ball(self.all_sprites, self.paddle, self.blocks)

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
