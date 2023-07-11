import pygame

import entropy


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        color_hover: tuple[int, int, int],
        image: pygame.Surface,
        image_hover: pygame.Surface,
        x: int,
        y: int,
    ):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.color_hover = color_hover
        self.original_image = image
        self.original_image_hover = image_hover
        self._image = self.original_image
        self._image_hover = self.original_image_hover
        self.image = self.original_image
        self.hover = False
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.x_percent = x / entropy.game.dimension[0]
        self.y_percent = y / entropy.game.dimension[1]
        self.width_percent = self.rect.width / entropy.game.dimension[0]
        self.height_percent = self.rect.height / entropy.game.dimension[1]

        self.re_scale()

    def re_scale(self):
        screen_rect = entropy.window.screen.get_rect()
        self.rect.x = self.x_percent * screen_rect.width
        self.rect.width = self.width_percent * screen_rect.width
        self.rect.y = self.y_percent * screen_rect.height
        self.rect.height = self.height_percent * screen_rect.height
        self._image = self.image = pygame.transform.scale(
            self.original_image, (self.rect.width, self.rect.height)
        )
        self._image_hover = self._image_hover = pygame.transform.scale(
            self.original_image_hover, (self.rect.width, self.rect.height)
        )

    def update(self) -> None:
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self._image_hover
        else:
            self.image = self._image
