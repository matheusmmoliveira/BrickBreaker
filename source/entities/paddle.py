from source.settings import *
from source.utils import Animation, import_images


class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups, initial_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT*0.95)):
        # Call the parent class (Sprite) constructor
        super().__init__(groups)

        # Animation
        self.animation = Animation(import_images('paddle'), img_dur=20)
        self.image = self.animation.img()

        # Initial Parameters
        self.rect = self.image.get_frect(midbottom=initial_pos)
        self.previous_rect = self.rect.copy()

        # Movement
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 700

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = pygame.math.Vector2(0, 0)
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        elif keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction = input_vector.normalize() if input_vector else input_vector

    # movement: -1=left, 1=right
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt

    def check_collision(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        elif self.rect.left < 0:
            self.rect.x = 0

    def update(self, dt):
        self.previous_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_collision()

        self.animation.update()
        self.image = self.animation.img()
