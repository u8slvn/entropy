from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg


if TYPE_CHECKING:
    from entropy.components.button import Button
    from entropy.misc.action import Actions
    from entropy.misc.mouse import Mouse


class MenuButtonGroup:
    def __init__(self, buttons: list[Button]) -> None:
        self._focus_index = 0
        self._buttons = buttons

    def _get_next_button(self) -> Button:
        self._focus_index = (self._focus_index + 1) % len(self._buttons)
        return self._buttons[self._focus_index]

    def _get_prev_button(self) -> Button:
        self._focus_index = (self._focus_index - 1) % len(self._buttons)
        return self._buttons[self._focus_index]

    def add(self, button: Button) -> None:
        self._buttons.append(button)

    def update(self, actions: Actions, mouse: Mouse) -> None:
        if actions.UP:
            mouse.hide()
            button = self._get_prev_button()
            pg.mouse.set_pos(button.rect.center)
        elif actions.DOWN:
            mouse.hide()
            button = self._get_next_button()
            pg.mouse.set_pos(button.rect.center)
        elif actions.ENTER:
            for button in self._buttons:
                if button.hover is True:
                    button.onclick()

        for button in self._buttons:
            button.update(mouse=mouse)

    def draw(self, surface: pg.Surface) -> None:
        for button in self._buttons:
            button.draw(surface=surface)
