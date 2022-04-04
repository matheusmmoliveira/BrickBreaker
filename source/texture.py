import pygame
from settings import *
import os


class BlockTextureMapper:
    def __init__(self):
        blk_dir = os.path.join(BASE_DIR, 'assets', 'imgs', 'blocks')
        self.block_textures = {file.replace('.png', ''): pygame.image.load(os.path.join(blk_dir, file)).convert_alpha()
                               for file in os.listdir(blk_dir)}

    def get_block_texture(self, color, size):
        return pygame.transform.scale(self.block_textures[color], size)
