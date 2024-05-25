import pygame
import pathlib


class Level:
    def __init__(self, win_width, win_height):
        self.level = 1
        self.blocks = pygame.sprite.Group()
        self._window_width = win_width
        self._window_height = win_height
        self._block_gap = 2

        # Creating a dictionary of possible block textures using its name as key
        _files = pathlib.Path('assets/images/blocks').glob("*.png")
        self._textures = {file.stem: pygame.image.load(file).convert_alpha() for file in _files}

        self._load_level_map()

    def _load_level_map(self):
        with open(f'assets/levels/{self.level}.lvl', 'r') as level_file:
            block_map = [line.replace('\n', '') for line in level_file.readlines()]

        block_height = (self._window_height * 0.6) / len(block_map) - self._block_gap
        block_width = self._window_width / len(block_map[0]) - self._block_gap
        for row_idx, row in enumerate(block_map):
            for col_idx, col in enumerate(row):
                if col != '*':
                    x = round(col_idx * (block_width + self._block_gap) + self._block_gap // 2)
                    y = round(row_idx * (block_height + self._block_gap) + self._block_gap // 2)
                    self.blocks.add(Block((block_width, block_height), int(col), (x, y), self._textures))

    def next_lvl(self):
        self.level += 1
        self._load_level_map()


class Block(pygame.sprite.Sprite):
    _colorCode = {
        1: 'red',
        2: 'green',
        3: 'blue',
        4: 'yellow'
    }

    def __init__(self, blk_size, blk_str, blk_pos, blk_textures):
        pygame.sprite.Sprite.__init__(self)
        self.block_size = blk_size
        self.strength = blk_str
        self.texture = blk_textures

        self.image = pygame.transform.scale(self.texture[self._colorCode[self.strength]], self.block_size)
        self.rect = self.image.get_rect(topleft=blk_pos)
        self.previous_rect = self.rect.copy()

    def damage(self):
        self.strength -= 1
        if self.strength == 0:
            self.kill()
        else:
            self.image = pygame.transform.scale(self.texture[self._colorCode[self.strength]], self.block_size)
