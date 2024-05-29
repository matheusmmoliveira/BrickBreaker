from source.settings import *
from source.utils import Animation, import_images


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, initial_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT*0.95)):
        # Call the parent class (Sprite) constructor
        super().__init__(groups)

        # Animation
        self.animation = Animation(import_images('paddle'), img_dur=40)
        self.image = self.animation.img()

        # Initial Parameters
        self.rect = self.image.get_frect(midbottom=initial_pos)
        self.previous_rect = self.rect.copy()

        # Movement
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 15

    def move(self):
        self.rect.x += self.direction.x * self.speed

    def check_collision(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        elif self.rect.left < 0:
            self.rect.x = 0

    def update(self):
        self.animation.update()
        self.image = self.animation.img()
        self.previous_rect = self.rect.copy()
        self.move()
        self.check_collision()


