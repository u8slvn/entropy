import pygame

from entropy.misc.window import Window


class ReScaler:
    def __init__(self, window: Window):
        self.window = window

    def re_scale(self, image: pygame.Surface) -> pygame.Surface:
        print(image.get_rect().x)
        print(image.get_rect().y)
        print(image.get_rect().width)
        print(image.get_rect().height)
        return image
