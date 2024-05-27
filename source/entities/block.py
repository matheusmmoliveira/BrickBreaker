from source.settings import *


class Block(pygame.sprite.Sprite):
    _colorCode = {
        1: 'red',
        2: 'green',
        3: 'blue',
        4: 'yellow'
    }

    def __init__(self, groups, blk_size, blk_str, blk_pos, blk_textures):
        super().__init__(groups)
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
