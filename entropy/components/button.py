import pygame

from entropy.misc.assets import Image
from entropy.misc.rect import Rect


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
        self._rect = Rect.from_image(x=x, y=y, image=bg_image)

    @property
    def image(self) -> pygame.Surface:
        return self._image.surface

    @property
    def rect(self) -> pygame.Rect:
        return self._rect.rect

    def update(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self._image = self._bg_image_hover
        else:
            self._image = self._bg_image
