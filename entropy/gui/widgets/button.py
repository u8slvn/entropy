from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame

from entropy import mixer
from entropy import mouse
from entropy.event.types import inputs
from entropy.gui.widgets.base import Widget
from entropy.gui.widgets.text import TText
from entropy.tools.observer import Observer
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.gui.widgets.base import Align
    from entropy.tools.observer import Subject
    from entropy.utils.measure import Color


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
        align: Align | None = None,
    ) -> None:
        self._pressed = False
        self._images = self._build_images(image=image)
        self._image = self._images[ButtonState.NORMAL]
        self._state = ButtonState.NORMAL
        self._sound_focus = sound_focus
        self._sound_clicked = sound_clicked
        self._callback = callback

        rect = pygame.Rect(*pos, *self._image.get_size())
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

    def set_focus(self) -> None:
        if self.is_checked():
            self._state = ButtonState.FOCUS_CHECKED
        else:
            self._state = ButtonState.FOCUS
        mixer.play_uisfx(self._sound_focus)

    def unset_focus(self) -> None:
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

    def process_event(self, event: Event) -> None:
        if mouse.visible:
            if mouse.collide_with(self.rect):
                if not self.has_focus():
                    self.set_focus()
                if event.pressed and event.key in (inputs.B, inputs.CLICK):
                    self.press()
            else:
                self.unset_focus()
        elif event.pressed and event.key == inputs.B and self.has_focus():
            self.press()

    def update(self, dt: float) -> None:
        if self.is_pressed():
            self.release()
        self._image = self._images[self._state]

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._image, self.rect)

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
        text_background: Color | str | None = None,
        text_align: Align | None = None,
        text_pos: Pos = Pos(0, 0),
        text_align_margin: Pos = Pos(0, 0),
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
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
            background=text_background,
            align=text_align,
            pos=text_pos,
            align_margin=text_align_margin,
        )

    def setup(self) -> None:
        super().setup()
        self._text.setup()

    def update(self, dt: float) -> None:
        super().update(dt=dt)
        self._text.update(dt=dt)

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
        return bool(self._match == getattr(self.subject, self._attr))


class ObserverButton(TextButton, Observer):
    def __init__(
        self,
        parent: Widget,
        image: pygame.Surface,
        sound_focus: str,
        sound_clicked: str,
        callback: Callable[[], None],
        attr_observer: AttrObserver,
        text: str,
        text_color: Color | str,
        text_font: pygame.font.Font,
        text_background: Color | str | None = None,
        text_align: Align | None = None,
        text_pos: Pos = Pos(0, 0),
        text_align_margin: Pos = Pos(0, 0),
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        super().__init__(
            parent=parent,
            image=image,
            sound_focus=sound_focus,
            sound_clicked=sound_clicked,
            callback=callback,
            text=text,
            text_color=text_color,
            text_font=text_font,
            text_align=text_align,
            text_pos=text_pos,
            text_background=text_background,
            text_align_margin=text_align_margin,
            pos=pos,
            align=align,
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
