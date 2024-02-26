from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame

from entropy import mixer
from entropy import mouse
from entropy.gui.components.base import Widget
from entropy.gui.components.text import TText
from entropy.tools.observer import Observer
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.base import ALIGN
    from entropy.gui.input import Inputs
    from entropy.tools.observer import Subject
    from entropy.utils import Color


class ButtonState(IntEnum):
    NORMAL = 0
    FOCUS = 1
    CHECKED = 2
    FOCUS_CHECKED = 3


class Button(Widget):
    def __init__(
        self,
        parent: Widget,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        pos: Pos = Pos(0, 0),
        align: ALIGN | None = None,
    ) -> None:

        self.pressed = False
        self.images = self._build_images(image=image)
        self.image = self.images[ButtonState.NORMAL]
        self.state = ButtonState.NORMAL
        self.sound_focus = sound_focus
        self.sound_clicked = sound_clicked
        self.callback = callback

        rect = pygame.Rect(*pos, *self.image.get_size())
        super().__init__(parent=parent, rect=rect, align=align)

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

    def check(self) -> None:
        if self.has_focus():
            self.state = ButtonState.FOCUS_CHECKED
        else:
            self.state = ButtonState.CHECKED

    def uncheck(self) -> None:
        if self.has_focus():
            self.state = ButtonState.FOCUS
        else:
            self.state = ButtonState.NORMAL

    def is_checked(self) -> bool:
        return self.state in [ButtonState.CHECKED, ButtonState.FOCUS_CHECKED]

    def set_focus(self):
        if self.is_checked():
            self.state = ButtonState.FOCUS_CHECKED
        else:
            self.state = ButtonState.FOCUS
        mixer.play_uisfx(self.sound_focus)

    def unset_focus(self):
        if self.is_checked():
            self.state = ButtonState.CHECKED
        else:
            self.state = ButtonState.NORMAL

    def has_focus(self) -> bool:
        return self.state in [ButtonState.FOCUS, ButtonState.FOCUS_CHECKED]

    def press(self) -> None:
        self.pressed = True

    def release(self) -> None:
        self.pressed = False
        mixer.play_uisfx(self.sound_clicked)
        self.callback()

    def is_pressed(self) -> bool:
        return self.pressed

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.is_visible():
            if mouse.collide_with(self.rect):
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
        self.image = self.images[self.state]

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def teardown(self) -> None:
        pass


class TextButton(Button):
    def __init__(
        self,
        parent: Widget,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        text: str,
        text_color: Color | str,
        text_font: pygame.font.Font,
        text_align: ALIGN | None = None,
        text_pos: Pos = Pos(0, 0),
        pos: Pos = Pos(0, 0),
        align: ALIGN | None = None,
    ) -> None:
        super().__init__(
            parent=parent,
            image=image,
            sound_focus=sound_focus,
            sound_clicked=sound_clicked,
            callback=callback,
            pos=pos,
            align=align,
        )

        self._text = TText(
            parent=self,
            text=text,
            color=text_color,
            font=text_font,
            align=text_align,
            pos=text_pos,
        )

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

    def has_changed(self) -> bool:
        return getattr(self.subject, self._attr) == self._match


class ObserverButton(TextButton, Observer):
    def __init__(
        self,
        parent: Widget | None,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        attr_observer: AttrObserver,
        text: TText,
        pos: Pos = Pos(0, 0),
        text_padding: Pos = Pos(0, 0),
    ) -> None:
        super().__init__(
            parent=parent,
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
        if self._attr_observer.has_changed():
            self.check()
        else:
            self.uncheck()

    def teardown(self) -> None:
        super().teardown()
        self._attr_observer.subject.remove_observer(observer=self)
