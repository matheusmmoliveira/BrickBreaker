from source.settings import *
from source.level import Level

TRAINING_SPEED = 120


class BrickBreakerGameAI:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Quebração de bloco')
        # Background
        self.background = pygame.image.load('assets/images/background.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Setup First Level Stage
        self.current_stage = Level()

    def step(self, action):
        pygame.display.update()
        self.screen.blit(self.background, (0, 0))
        self.clock.tick(TRAINING_SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        reward, game_over, score = self.current_stage.run(action)

        return reward, game_over, score

    def reset(self):
        del self.current_stage
        self.current_stage = Level()


if __name__ == '__main__':
    game = BrickBreakerGameAI()
    manual_input = 0
    game.current_stage.ball.active = False
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game.reset()
            game.current_stage.ball.active = False
        elif keys[pygame.K_SPACE]:
            game.current_stage.ball.active = True
        elif keys[pygame.K_LEFT]:
            manual_input = 1
        elif keys[pygame.K_RIGHT]:
            manual_input = 2
        else:
            manual_input = 0
        game.step(manual_input)
