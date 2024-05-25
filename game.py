import pygame
import sys
from source import level, paddle, ball


class BrickBreaker:
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FPS = 60

    def __init__(self):
        # Initial setup
        pygame.init()
        pygame.display.set_caption('Quebração de bloco')
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = self.FPS

        # Background
        self.background = pygame.image.load('assets/images/background.png').convert()
        self.background = pygame.transform.scale(self.background, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # Sprite Group Setup
        self.world = pygame.sprite.Group()

        # Setup all game objects
        self.level = level.Level(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.paddle = paddle.Paddle(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.ball = ball.Ball(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.paddle.rect.midtop, self.level.blocks, self.paddle)

        self.world.add(self.level.blocks, self.paddle, self.ball)

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(self.fps)

            # Update All Sprites
            self.world.update()
            self.world.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = BrickBreaker()
    game.run()
