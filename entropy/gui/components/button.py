from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame

from entropy import mixer
from entropy import mouse
from entropy.gui.components.widget import WidgetComponent
from entropy.tools.observer import Observer
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.text import Text
    from entropy.gui.input import Inputs
    from entropy.tools.observer import Subject


class ButtonState(IntEnum):
    NORMAL = 0
    FOCUS = 1
    CHECKED = 2
    FOCUS_CHECKED = 3


class Button(WidgetComponent):
    def __init__(
        self,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        pos: Pos = Pos(0, 0),
    ) -> None:
        self._pressed = False
        self._images = self._build_images(image=image)
        self._image = self._images[ButtonState.NORMAL]
        self._rect = self._image.get_rect()
        self._rect.topleft = pos
        self._state = ButtonState.NORMAL
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

    def get_width(self) -> int:
        return self._image.get_width()

    def get_height(self) -> int:
        return self._image.get_height()

    def set_pos(self, pos: Pos, center_x: bool = False) -> None:
        if center_x is True:
            self._rect.topleft = Pos(self.get_center_x(), pos.y)
        else:
            self._rect.topleft = pos

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
        mixer.play_uisfx(self._sound_focus)

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
        mixer.play_uisfx(self._sound_clicked)
        self._callback()

    def is_pressed(self) -> bool:
        return self._pressed

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.is_visible():
            if mouse.collide_with(self._rect):
                if not self.has_focus():
                    self.set_focus()
                if inputs.mouse.BUTTON1:
                    self.press()
            else:
                self.unset_focus()
        if inputs.keyboard.ENTER and self.has_focus():
            self.press()

    def update(self):
        if self.is_pressed():
            self.release()
        self._image = self._images[self._state]

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, self._rect)

    def teardown(self) -> None:
        pass


class TextButton(Button):
    def __init__(
        self,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        text: Text,
        pos: Pos = Pos(0, 0),
        text_padding: Pos = Pos(0, 0),
    ) -> None:
        super().__init__(
            image=image,
            sound_focus=sound_focus,
            sound_clicked=sound_clicked,
            callback=callback,
            pos=pos,
        )
        self._text_padding = text_padding
        self._text = text
        self._set_text_pos()

    def _set_text_pos(self) -> None:
        self._text.set_center_pos(
            Pos(
                self._rect.centerx + self._text_padding.x,
                self._rect.centery + self._text_padding.y,
            )
        )

    def set_pos(self, pos: Pos, center_x: bool = False) -> None:
        super().set_pos(pos=pos, center_x=center_x)
        self._set_text_pos()

    def setup(self) -> None:
        super().setup()
        self._text.setup()

    def update(self):
        super().update()
        self._text.update()

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface=surface)
        self._text.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._text.teardown()


class AttrObserver:
    def __init__(self, subject: Subject, attr: str, match: Any) -> None:
        self._attr = attr
        self._match = match
        self.subject = subject

    def attr_changed(self) -> bool:
        return getattr(self.subject, self._attr) == self._match


class ObserverButton(TextButton, Observer):
    def __init__(
        self,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        attr_observer: AttrObserver,
        text: Text,
        pos: Pos = Pos(0, 0),
        text_padding: Pos = Pos(0, 0),
    ) -> None:
        super().__init__(
            image=image,
            sound_focus=sound_focus,
            sound_clicked=sound_clicked,
            callback=callback,
            pos=pos,
            text=text,
            text_padding=text_padding,
        )
        self._attr_observer = attr_observer

    def setup(self) -> None:
        super().setup()
        self._attr_observer.subject.add_observer(observer=self)

    def on_notify(self) -> None:
        if self._attr_observer.attr_changed():
            self.check()
        else:
            self.uncheck()

    def teardown(self) -> None:
        super().teardown()
        self._attr_observer.subject.remove_observer(observer=self)
