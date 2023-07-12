from __future__ import annotations

from abc import ABC, abstractmethod

import pygame.event

import entropy
from entropy.colors import BLACK, WHITE
from entropy.components import Component
from entropy.components.button import Button


class MainMenu(Component):
    def __init__(self):
        self._no_save = True
        self.btn_margin = 30
        self.btn = Button(
            text="hello",
            font=entropy.assets.fonts.get("LanaPixel", 20),
            color=BLACK,
            color_hover=WHITE,
            image=entropy.assets.images.get("main-menu-btn"),
            image_hover=entropy.assets.images.get("main-menu-btn-hover"),
            x=600,
            y=600,
        )
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.btn)
        # self.buttons.add(Bite())

    # def setup(self):
    #     self.continue_btn.set_visibility(not self._no_save)
    #
    #     y = 0
    #     for button in self.buttons:
    #         if not button.visible:
    #             continue
    #         button.update_position(y=y)
    #         y += button.image.get_height() + self.btn_margin

    def handle_event(self, event: pygame.event.Event) -> None:
        # for button in self.buttons:
        #     if not button.visible:
        #         continue
        #     button.handle_event(event=event)
        ...

    def draw(self, display: pygame.Surface) -> None:
        # for button in self.buttons:
        #     if not button.visible:
        #         continue
        #     button.draw(display)
        self.buttons.update()
        self.buttons.draw(display)


class MainMenuButton(Component, ABC):
    font_size = 40
    label_margin = 60
    label: str

    def __init__(self) -> None:
        self.visible = True
        self.hover = False
        self.image = entropy.assets.images.get("main-menu-btn")
        self.image_hover = entropy.assets.images.get("main-menu-btn-hover")
        self.font = entropy.assets.fonts.get("LanaPixel", self.font_size)
        self.display = pygame.Surface(self.image.get_size())
        self.rect = self.display.get_rect()
        self.rect.topleft = (0, 0)

    def set_visibility(self, value: bool):
        self.visible = value

    def update_position(self, x: int | None = None, y: int | None = None):
        self.rect.topleft = (x or self.rect.x, y or self.rect.y)

    @abstractmethod
    def on_click(self) -> None:
        ...

    def update(self) -> None:
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, display: pygame.Surface) -> None:
        if self.hover:
            self.display.blit(self.image_hover, (0, 0))
            text = self.font.draw(self.label, True, WHITE)
        else:
            self.display.blit(self.image, (0, 0))
            text = self.font.draw(self.label, True, BLACK)

        self.display.blit(
            text,
            (
                self.display.get_width() - text.get_width() - self.label_margin,
                (self.display.get_height() - text.get_height()) // 2,
            ),
        )

        display.blit(self.display, (self.rect.x, self.rect.y))


class NewGameButton(MainMenuButton):
    label = "NEW GAME"

    def on_click(self) -> None:
        pass


class ContinueButton(MainMenuButton):
    label = "CONTINUE"

    def on_click(self) -> None:
        pass


class SettingsButton(MainMenuButton):
    label = "SETTINGS"

    def on_click(self) -> None:
        pass


class QuitButton(MainMenuButton):
    label = "QUIT"

    def on_click(self) -> None:
        pass
