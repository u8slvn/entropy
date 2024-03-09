from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame as pg

from entropy import mixer
from entropy import mouse
from entropy.constants import SLIDER_BG_COLOR
from entropy.constants import SLIDER_PROGRESS_COLOR
from entropy.event.specs import click_is_pressed
from entropy.event.specs import left_or_right_is_pressed
from entropy.event.types import inputs
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.base import Widget
from entropy.gui.widgets.text import TText
from entropy.utils.measure import Pos
from entropy.utils.measure import Size


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.utils.measure import Color


class Slider(Widget):
    _step = 0.1

    def __init__(
        self,
        parent: Widget,
        size: Size,
        min_value: int,
        max_value: int,
        initial_value: float,
        update_callback: Callable[[float], None],
        button_image: pg.Surface,
        sound_focus: str,
        sound_on_hold: Callable[[], None] | None = None,
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        self._focus = False
        self._grabbed = False

        self._last_value = 0.0
        self._value = initial_value
        self._min_value = min_value
        self._max_value = max_value

        self._sound_focus = sound_focus
        self._sound_on_hold = sound_on_hold

        self._button = _Button(image=button_image, focus=self._focus)
        self._update_callback = update_callback

        self._bar = _Bar(pos=pos, size=size)
        super().__init__(parent=parent, rect=self._bar.rect, align=align)

        self._button.move(
            Pos(
                self.pos.x,
                self.pos.y - (self._button.size.h - self.size.h) // 2,
            )
        )
        self.set_value(value=self._value)

    def update_align(self) -> None:
        match self.align:
            case Align.CENTER:
                self._bar.center(*self.parent.center)
            case Align.CENTER_X:
                self._bar.center(x=self.parent.centerx)
            case Align.CENTER_Y:
                self._bar.center(y=self.parent.centery)

    def set_focus(self) -> None:
        if self._focus:
            return

        self._focus = True
        self._button.focus = True
        mixer.play_uisfx(self._sound_focus)

    def unset_focus(self) -> None:
        self._focus = False
        self._button.focus = False

    def has_focus(self) -> bool:
        return self._focus

    def move_slider(self, value: int) -> None:
        if value < self._bar.min:
            value = self._bar.min
        if value > self._bar.max:
            value = self._bar.max

        self._button.value = value
        self._bar.progress = value

    def get_value(self) -> float:
        button_value = self._button.value - self._bar.min
        value = (button_value / self._bar.range) * (
            self._max_value - self._min_value
        ) + self._min_value
        return round(value, 2)

    def set_value(self, value: float) -> None:
        self._last_value = self.get_value()
        value = self._bar.min + self._bar.range * value
        self.move_slider(value=int(value))

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        if mouse.visible:
            if mouse.collide_with(self.rect) or mouse.collide_with(self._button.rect):
                if click_is_pressed(event):
                    self._grabbed = True
            if not event.held:
                mouse.grabbing = False
                self._grabbed = False

            if mouse.collide_with(self._button.rect) or self._grabbed:
                self.set_focus()
            else:
                self.unset_focus()

            if self._grabbed:
                self._button.value = mouse.pos.x

        elif self.has_focus():
            if left_or_right_is_pressed(event):
                value = round(self.get_value(), 1)
                if event.key == inputs.LEFT:
                    self.set_value(value - self._step)
                else:
                    self.set_value(value + self._step)

                self._grabbed = True
            else:
                self._grabbed = False

    def update(self, dt: float) -> None:
        self._button.update()
        if self._grabbed:
            self.move_slider(self._button.value)

            if self._sound_on_hold is not None:
                self._sound_on_hold()

            value = self.get_value()
            if self._last_value != value:
                self._update_callback(value)

    def draw(self, surface: pg.Surface) -> None:
        self._bar.draw(surface)
        self._button.draw(surface)

    def teardown(self) -> None:
        pass


class _Button:
    def __init__(self, image: pg.Surface, focus: bool) -> None:
        self.focus = focus
        self._images = self._build_images(image)
        self._image = self._images[self.focus]
        self.rect = self._image.get_rect()

    @staticmethod
    def _build_images(image: pg.Surface) -> list[pg.Surface]:
        width = image.get_width()
        height = image.get_height() // 2

        x = y = 0
        buttons = []
        for btn in range(2):
            buttons.append(image.subsurface((x, y, width, height)))
            y += height

        return buttons

    @property
    def value(self) -> int:
        return self.rect.centerx

    @value.setter
    def value(self, value: int) -> None:
        self.rect.centerx = value

    @property
    def size(self) -> Size:
        return Size(*self._image.get_size())

    def move(self, pos: Pos) -> None:
        self.rect.topleft = pos

    def update(self) -> None:
        self._image = self._images[self.focus]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._image, self.rect)


class _Bar:
    def __init__(self, pos: Pos, size: Size):
        self.rect = pg.Rect(*pos, *size)
        self._progress = pg.Rect(*pos, *size)

    def center(self, x: int | None = None, y: int | None = None) -> None:
        x = x or self.rect.centerx
        y = y or self.rect.centery

        self.rect.center = x, y
        self._progress.center = x, y

    @property
    def min(self) -> int:
        return self.rect.left

    @property
    def max(self) -> int:
        return self.rect.right

    @property
    def range(self) -> int:
        return self.max - self.min

    @property
    def progress(self) -> int:
        return self._progress.w

    @progress.setter
    def progress(self, value: int) -> None:
        self._progress.w = value - self.min

    def draw(self, surface: pg.Surface) -> None:
        # TODO: move color outside the widget.
        pg.draw.rect(surface, SLIDER_BG_COLOR, self.rect)
        pg.draw.rect(surface, SLIDER_PROGRESS_COLOR, self._progress)


class TitledSlider(Widget):
    _margin = 7

    def __init__(
        self,
        parent: Widget,
        size: Size,
        min_value: int,
        max_value: int,
        initial_value: float,
        update_callback: Callable[[float], None],
        button_image: pg.Surface,
        text: str,
        text_color: Color | str,
        text_font: pg.font.Font,
        space_between: int,
        sound_focus: str,
        sound_on_hold: Callable[[], None] | None = None,
        text_background: Color | str | None = None,
        text_align: Align | None = None,
        text_align_margin: Pos = Pos(0, 0),
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        self._space_between = space_between

        self._text = TText(
            parent=parent,
            text=text,
            color=text_color,
            font=text_font,
            background=text_background,
            align=text_align,
            pos=pos,
            align_margin=text_align_margin,
        )
        self._slider = Slider(
            parent=parent,
            size=size,
            min_value=min_value,
            max_value=max_value,
            initial_value=initial_value,
            update_callback=update_callback,
            sound_focus=sound_focus,
            sound_on_hold=sound_on_hold,
            button_image=button_image,
            pos=Pos(pos.x, pos.y + self._space_between),
            align=align,
        )

        rect = pg.Rect(*pos, 0, 0)
        super().__init__(parent=parent, rect=rect, align=align)

    def update_align(self) -> None:
        super().update_align()
        match self.align:
            case Align.CENTER:
                pass
            case Align.CENTER_X:
                self._text.rect.centerx = self.parent.centerx
                self._slider.rect.centerx = self.parent.centerx
            case Align.CENTER_Y:
                pass

    @property
    def size(self) -> Size:
        return Size(self.size.w, self.size.h + self._margin + self._text.size.h)

    def setup(self) -> None:
        self._text.setup()
        self._slider.setup()

    def process_event(self, event: Event) -> None:
        self._text.process_event(event=event)
        self._slider.process_event(event=event)

    def update(self, dt: float) -> None:
        self._text.update(dt=dt)
        self._slider.update(dt=dt)

    def draw(self, surface: pg.Surface) -> None:
        self._text.draw(surface=surface)
        self._slider.draw(surface=surface)

    def teardown(self) -> None:
        self._text.teardown()
        self._slider.teardown()

    def set_focus(self) -> None:
        self._slider.set_focus()

    def unset_focus(self) -> None:
        self._slider.unset_focus()

    def has_focus(self) -> bool:
        return self._slider.has_focus()
