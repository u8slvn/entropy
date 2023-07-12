import pygame

import entropy
from entropy.misc.assets import Image


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        color_hover: tuple[int, int, int],
        bg_image: Image,
        bg_image_hover: Image,
        x: int,
        y: int,
    ):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.color_hover = color_hover
        self._bg_image = bg_image
        self._bg_image_hover = bg_image_hover
        self._image = bg_image
        self.hover = False
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.x_percent = x / entropy.game.max_resolution.width
        self.y_percent = y / entropy.game.max_resolution.height

        self.re_scale()

    @property
    def image(self) -> pygame.Surface:
        return self._image.surface

    def re_scale(self):
        screen_rect = entropy.game.screen.get_rect()
        self.rect.x = self.x_percent * screen_rect.width
        self.rect.width = self._image.scale_percent_w * screen_rect.width
        self.rect.y = self.y_percent * screen_rect.height
        self.rect.height = self._image.scale_percent_h * screen_rect.height

    def update(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self._image = self._bg_image_hover
        else:
            self._image = self._bg_image
