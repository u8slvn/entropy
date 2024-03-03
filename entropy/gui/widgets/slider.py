from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame

from entropy import mixer
from entropy import mouse
from entropy.constants import SLIDER_BG_COLOR
from entropy.constants import SLIDER_PROGRESS_COLOR
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.base import Widget
from entropy.gui.widgets.text import TText
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.commands.base import ConfigurableCommand
    from entropy.gui.input import Inputs
    from entropy.utils import Color
    from entropy.utils import Size


class Slider(Widget):
    _step = 0.1

    def __init__(
        self,
        parent: Widget,
        size: Size,
        min_value: int,
        max_value: int,
        initial_value: float,
        command: ConfigurableCommand,
        button_image: pygame.Surface,
        sound_focus: str,
        sound_on_hold: Callable[[], None] | None = None,
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        self._focus = False
        self._grabbed = False

        self._last_value = 0
        self._value = initial_value
        self._min_value = min_value
        self._max_value = max_value

        self._sound_focus = sound_focus
        self._sound_on_hold = sound_on_hold

        self._buttons = self._build_buttons(button_image)
        self._button = self._buttons[self._focus]
        self._button_rect = self._button.get_rect()
        self._button_x = 0
        self._command = command

        self._progress = pygame.Rect(*pos, *size)
        rect = pygame.Rect(*pos, *size)
        super().__init__(parent=parent, rect=rect, align=align)

        self._min_pos = self.pos.x
        self._max_pos = self.pos.x + self.size.w
        self._button_rect.topleft = (
            self.pos.x,
            self.pos.y - (self._button_rect.h - self.size.h) // 2,
        )
        self.set_value(value=self._value)

    def update_align(self) -> None:
        match self.align:
            case Align.CENTER:
                self.rect.center = self.parent.center
                self._progress.center = self.parent.center
            case Align.CENTER_X:
                self.rect.centerx = self.parent.centerx
                self._progress.centerx = self.parent.centerx
            case Align.CENTER_Y:
                self.rect.centery = self.parent.centery
                self._progress.centery = self.parent.centery

    @staticmethod
    def _build_buttons(image: pygame.Surface) -> list[pygame.Surface]:
        width = image.get_width()
        height = image.get_height() // 2

        x = y = 0
        buttons = []
        for btn in range(2):
            buttons.append(image.subsurface((x, y, width, height)))
            y += height

        return buttons

    def set_focus(self) -> None:
        if self.has_focus():
            return

        self._focus = True
        mixer.play_uisfx(self._sound_focus)

    def unset_focus(self) -> None:
        self._focus = False

    def has_focus(self) -> None:
        return self._focus is True

    @property
    def range_value(self) -> int:
        return self._max_pos - self._min_pos

    def move_slider(self, x: int) -> None:
        if x < self._min_pos:
            x = self._min_pos
        if x > self._max_pos:
            x = self._max_pos
        self._button_rect.centerx = x
        self._progress.w = self._button_rect.centerx - self._min_pos

    def get_value(self) -> float:
        button_value = self._button_rect.centerx - self._min_pos

        value = (button_value / self.range_value) * (
            self._max_value - self._min_value
        ) + self._min_value
        return round(value, 2)

    def set_value(self, value: float) -> None:
        self._last_value = self.get_value()
        self._button_x = int(self._min_pos + self.range_value * value)
        self.move_slider(x=self._button_x)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.is_visible():
            if mouse.collide_with(self._rect) or mouse.collide_with(self._button_rect):
                if inputs.mouse.BUTTON1 and mouse.is_button_pressed(mouse.BUTTON1):
                    self._grabbed = True
            if not mouse.is_button_pressed(mouse.BUTTON1):
                self._grabbed = False
            if mouse.collide_with(self._button_rect) or self._grabbed:
                self.set_focus()
            else:
                self.unset_focus()

            if self._grabbed:
                self._button_x = mouse.pos.x

        elif self.has_focus():
            self._grabbed = True

            if inputs.keyboard.LEFT:
                value = round(self.get_value(), 1)
                self.set_value(value - self._step)
                mixer.play_uisfx(self._sound_focus)
            elif inputs.keyboard.RIGHT:
                value = round(self.get_value(), 1)
                self.set_value(value + self._step)
                mixer.play_uisfx(self._sound_focus)
            else:
                self._grabbed = False

    def update(self, dt: float) -> None:
        self._button = self._buttons[self._focus]
        if self._grabbed:
            self.move_slider(self._button_x)

            if self._sound_on_hold is not None:
                self._sound_on_hold()

            value = self.get_value()
            if self._last_value != value:
                self._command.configure(value)
                self._command()

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, SLIDER_BG_COLOR, self._rect)
        pygame.draw.rect(surface, SLIDER_PROGRESS_COLOR, self._progress)
        surface.blit(self._button, self._button_rect)

    def teardown(self) -> None:
        pass


class TitledSlider(Widget):
    _margin = 7

    def __init__(
        self,
        parent: Widget,
        size: Size,
        min_value: int,
        max_value: int,
        initial_value: float,
        command: ConfigurableCommand,
        button_image: pygame.Surface,
        text: str,
        text_color: Color | str,
        text_font: pygame.font.Font,
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
            sound_focus=sound_focus,
            sound_on_hold=sound_on_hold,
            command=command,
            button_image=button_image,
            pos=Pos(pos.x, pos.y + self._space_between),
            align=align,
        )

        rect = pygame.Rect(*pos, 0, 0)
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

    def process_inputs(self, inputs: Inputs) -> None:
        self._text.process_inputs(inputs=inputs)
        self._slider.process_inputs(inputs=inputs)

    def update(self, dt: float) -> None:
        self._text.update(dt=dt)
        self._slider.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._text.draw(surface=surface)
        self._slider.draw(surface=surface)

    def teardown(self) -> None:
        self._text.teardown()
        self._slider.teardown()

    def set_focus(self) -> None:
        self._slider.set_focus()

    def unset_focus(self) -> None:
        self._slider.unset_focus()

    def has_focus(self) -> None:
        self._slider.has_focus()
