import pygame
import sys
from source import level, paddle, ball, settings

class BrickBreaker:
    def __init__(self):
        # Initial setup
        pygame.init()
        pygame.display.set_caption('Quebração de bloco')
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = settings.FPS

        # Background
        self.background = pygame.image.load('assets/images/background.png').convert()
        self.background = pygame.transform.scale(self.background, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))

        # Sprite Group Setup
        self.world = pygame.sprite.Group()

        # Setup all game objects
        self.level = level.Level()
        self.paddle = paddle.Paddle()
        self.ball = ball.Ball(self.paddle.rect.midtop, self.level.blocks, self.paddle)

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
