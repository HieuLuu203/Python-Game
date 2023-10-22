"""
Vật cản
"""

import pygame

# Lớp cha
class Draw(pygame.sprite.Sprite):
    """lớp cha cho các lớp con vật cản"""

    def __init__(self, image, pos, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


#Các lớp con
class Platform(Draw):
    """ô gạch"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Spike(Draw):
    """gai nhọn"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Orb(Draw):
    """quang cầu"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)


class Trick(Draw):
    """ô lừa"""

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

    def enter(self, image):
        self.image = image


class End(Draw):
    "kết thúc màn chơi"

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)
