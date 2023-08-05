from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from entropy import mouse


if TYPE_CHECKING:
    from entropy.gui.components.button import Button
    from entropy.gui.input.keyboard_events import KeyboardEvents
    from entropy.gui.input.mouse_events import MouseEvents


class MenuButtonGroup:
    _init_focus = -1

    def __init__(self, buttons: list[Button]) -> None:
        self._focus_index = self._init_focus
        self._buttons = buttons

    def _select_next_button(self) -> None:
        self._buttons[self._focus_index].unset_focus()
        self._focus_index = (self._focus_index + 1) % len(self._buttons)
        self._buttons[self._focus_index].set_focus()

    def _select_prev_button(self) -> None:
        self._buttons[self._focus_index].unset_focus()
        if self._focus_index == self._init_focus:
            self._focus_index = 0
        self._focus_index = (self._focus_index - 1) % len(self._buttons)
        self._buttons[self._focus_index].set_focus()

    def _get_selected_button(self) -> Button:
        return self._buttons[self._focus_index]

    def add(self, button: Button) -> None:
        self._buttons.append(button)

    def update(self, keyboard_e: KeyboardEvents, mouse_e: MouseEvents) -> None:
        if keyboard_e.UP:
            mouse.hide()
            self._select_prev_button()
        elif keyboard_e.DOWN:
            mouse.hide()
            self._select_next_button()
        elif keyboard_e.ENTER:
            for button in self._buttons:
                if button.has_focus():
                    button.click()

        if mouse.is_visible():
            for index, button in enumerate(self._buttons):
                if button.collide_mouse():
                    if not button.has_focus():
                        button.set_focus()
                        self._focus_index = index

                    if mouse_e.BUTTON1:
                        button.press()
                    elif button.is_pressed():
                        button.release()
                else:
                    button.unset_focus()

    def draw(self, surface: pg.Surface) -> None:
        for button in self._buttons:
            button.draw(surface=surface)
