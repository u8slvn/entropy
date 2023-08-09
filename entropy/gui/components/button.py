from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame

from entropy import config
from entropy import mouse
from entropy.game.object import GameEntity
from entropy.tools.observer import Observer
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.text import Text
    from entropy.gui.input import Inputs


class ButtonState(IntEnum):
    NORMAL = 0
    FOCUS = 1
    CHECKED = 2
    FOCUS_CHECKED = 3


class Button(GameEntity):
    def __init__(
        self,
        text: Text,
        image: pygame.Surface,
        sound_focus: pygame.mixer.Sound,
        sound_clicked: pygame.mixer.Sound,
        callback: Callable[[], None],
        pos: Pos,
        padding: Pos = Pos(0, 0),
    ) -> None:
        super().__init__()
        self._pressed = False
        self._images = self._build_images(image=image)
        self._image = self._images[ButtonState.NORMAL]
        self._rect = self._image.get_rect()
        self._rect.topleft = pos
        self._state = ButtonState.NORMAL

        x, y = self._rect.center
        text.set_center_pos(Pos(x + padding.x, y + padding.y))
        self._text = text

        self._sound_focus = sound_focus
        self._sound_clicked = sound_clicked

        self._callback = callback

    @staticmethod
    def _build_images(image: pygame.Surface) -> dict[ButtonState, pygame.Surface]:
        width = image.get_width()
        height = image.get_height() // 4

        x = y = 0
        images = {}
        for btn_state in ButtonState:
            images[btn_state] = image.subsurface((x, y, width, height))
            y += height

        return images

    def setup(self) -> None:
        self._text.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.is_visible():
            if self._rect.collidepoint(inputs.mouse.pos):
                if not self.has_focus():
                    self.set_focus()
                if inputs.mouse.BUTTON1:
                    self.press()
            else:
                self.unset_focus()

    def update(self):
        if self.is_pressed():
            self.release()
        self._text.update()
        self._image = self._images[self._state]

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, self._rect)
        self._text.draw(surface=surface)

    def teardown(self) -> None:
        self._text.teardown()

    def check(self) -> None:
        if self.has_focus():
            self._state = ButtonState.FOCUS_CHECKED
        else:
            self._state = ButtonState.CHECKED

    def uncheck(self) -> None:
        if self.has_focus():
            self._state = ButtonState.FOCUS
        else:
            self._state = ButtonState.NORMAL

    def is_checked(self) -> bool:
        return self._state in [ButtonState.CHECKED, ButtonState.FOCUS_CHECKED]

    def set_focus(self):
        if self.is_checked():
            self._state = ButtonState.FOCUS_CHECKED
        else:
            self._state = ButtonState.FOCUS
        self._sound_focus.play()

    def unset_focus(self):
        if self.is_checked():
            self._state = ButtonState.CHECKED
        else:
            self._state = ButtonState.NORMAL

    def has_focus(self) -> bool:
        return self._state in [ButtonState.FOCUS, ButtonState.FOCUS_CHECKED]

    def press(self) -> None:
        self._pressed = True

    def release(self) -> None:
        self._pressed = False
        self._sound_clicked.play()
        self._callback()

    def is_pressed(self) -> bool:
        return self._pressed


class ConfigObserverButton(Button, Observer):
    def __init__(self, *args, watch: str, match: Any, **kwargs):
        super().__init__(*args, **kwargs)
        self._watch = watch
        self._match = match

    def setup(self) -> None:
        super().setup()
        config.add_observer(observer=self)

    def on_notify(self) -> None:
        if getattr(config, self._watch) == self._match:
            self.check()
        else:
            self.uncheck()

    def teardown(self) -> None:
        super().teardown()
        config.remove_observer(observer=self)
