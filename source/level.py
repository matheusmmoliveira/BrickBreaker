import pygame
from settings import *
from texture import BlockTextureMapper


class Level:
    def __init__(self):
        self.level = 1
        self.block_map = self._load_level_map()

        self.gap = 2
        self.block_height = (WINDOW_HEIGHT * 0.6) / len(self.block_map) - self.gap
        self.block_width = WINDOW_WIDTH / len(self.block_map[0]) - self.gap
        self.textures = BlockTextureMapper()

    def _load_level_map(self):
        with open(BASE_DIR / 'assets' / 'levels' / f'{self.level}.lvl', 'r') as level_file:
            return [line.replace('\n', '') for line in level_file.readlines()]

    def setup_level(self, groups):
        for row_idx, row in enumerate(self.block_map):
            for col_idx, col in enumerate(row):
                if col != '*':
                    x = round(col_idx * (self.block_width + self.gap) + self.gap // 2)
                    y = round(row_idx * (self.block_height + self.gap) + self.gap // 2)
                    Block(groups, (self.block_width, self.block_height), int(col), (x, y), self.textures)


class Block(pygame.sprite.Sprite):
    color_legend = {
        1: 'red',
        2: 'green',
        3: 'blue',
        4: 'yellow'
    }

    def __init__(self, groups, block_size, block_type, pos, textures):
        super().__init__(groups)
        self.texture = textures
        self.block_size = block_size
        self.image = self.texture.get_block_texture(self.color_legend[block_type], block_size)
        self.rect = self.image.get_rect(topleft=pos)
        self.previous_rect = self.rect.copy()

        self.strength = block_type

    def damage(self):
        self.strength -= 1
        if self.strength == 0:
            self.kill()
        else:
            self.image = self.texture.get_block_texture(self.color_legend[self.strength], self.block_size)

