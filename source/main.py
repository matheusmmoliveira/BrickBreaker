import time
import pygame
from settings import *
import sys


class Game:
    def __init__(self):
        # Initial setup
        pygame.init()
        pygame.display.set_caption('Quebração de bloco')
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Background
        self.background = self.create_background()

    def create_background(self):
        background_img = pygame.image.load(BASE_DIR / 'assets' / 'imgs' / 'background.png').convert()
        scaled_background = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        return scaled_background

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Draw frame
            self.canvas.blit(self.background, (0, 0))

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
