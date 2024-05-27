import time

from source.settings import *
from source.level import Level
from source.entities import ball, paddle


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Quebração de bloco')
        self.clock = pygame.time.Clock()

        # Background
        self.background = pygame.image.load('assets/images/background.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Setup First Level Stage
        self.current_stage = Level()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
