from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy


if TYPE_CHECKING:
    from entropy.components.button import Button


class MenuButtonGroup:
    def __init__(self, buttons: list[Button]) -> None:
        self._focus_index = 0
        self._buttons = buttons

    @property
    def nb_buttons(self) -> int:
        return len(self._buttons)

    def _get_next_button(self) -> Button:
        self._focus_index += 1
        if self._focus_index > self.nb_buttons - 1:
            self._focus_index = 0

        return self._buttons[self._focus_index]

    def _get_prev_button(self) -> Button:
        self._focus_index -= 1
        if self._focus_index < 0:
            self._focus_index = self.nb_buttons - 1

        return self._buttons[self._focus_index]

    def add(self, button: Button) -> None:
        self._buttons.append(button)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                entropy.mouse.hide()
                button = self._get_prev_button()
                pg.mouse.set_pos(button.rect.center)
            elif event.key == pg.K_DOWN:
                entropy.mouse.hide()
                button = self._get_next_button()
                pg.mouse.set_pos(button.rect.center)
            elif event.key == pg.K_RETURN:
                for button in self._buttons:
                    if button.hover is True:
                        button.onclick()

    def update(self) -> None:
        for button in self._buttons:
            button.update()

    def draw(self, surface: pg.Surface) -> None:
        for button in self._buttons:
            button.draw(surface=surface)
