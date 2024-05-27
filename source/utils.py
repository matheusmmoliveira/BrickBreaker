import pygame
import pathlib


BASE_IMAGE_PATH = 'assets/images/'


def import_image(path):
    img = pygame.image.load(pathlib.Path(BASE_IMAGE_PATH + path)).convert()
    img.set_colorkey((0, 0, 0))
    return img


def import_images(path):
    images = []
    for img in sorted(pathlib.Path(BASE_IMAGE_PATH + path).glob('*.png')):
        images.append(import_image(path + '/' + img.name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
