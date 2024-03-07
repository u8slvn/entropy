from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import mixer
from entropy import translator
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.base import Widget
from entropy.tools.observer import Observer
from entropy.utils.measure import Color
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event

T = translator


class Text(Widget):
    def __init__(
        self,
        parent: Widget,
        text: str,
        color: Color | str,
        font: pygame.font.Font,
        background: Color | str | None = None,
        pos: Pos = Pos(0, 0),
        align_margin: Pos = Pos(0, 0),  # Topleft margin, works also with align.
        align: Align | None = None,
    ):
        self._text = text
        self._color = color
        self._font = font
        self._background = background
        self._align_margin = align_margin
        self._surf = self._render()

        rect = pygame.Rect(*(pos + parent.pos), *self._surf.get_size())
        super().__init__(parent=parent, rect=rect, align=align)

    def update_align(self) -> None:
        """Overwrite base update align method in order to take margin in account."""
        match self.align:
            case Align.CENTER:
                self.rect.center = self.parent.center
                self.rect.topleft = Pos(*self.rect.topleft) + self._align_margin
            case Align.CENTER_X:
                self.rect.centerx = self.parent.centerx
                self.rect.top += self._align_margin.x
            case Align.CENTER_Y:
                self.rect.centery = self.parent.centery
                self.rect.left += self._align_margin.y

    def _render(self) -> pygame.Surface:
        return self._font.render(self._text, False, self._color, self._background)

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.rect)

    def teardown(self) -> None:
        pass


class TText(Text, Observer):
    """Translated Text."""

    def __init__(
        self,
        parent: Widget,
        text: str,
        color: Color | str,
        font: pygame.font.Font,
        background: Color | str | None = None,
        pos: Pos = Pos(0, 0),
        align_margin: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        self.__text = text
        self._locale_changed = False

        super().__init__(
            parent=parent,
            text=T(text),
            color=color,
            font=font,
            background=background,
            pos=pos,
            align_margin=align_margin,
            align=align,
        )

    def on_notify(self) -> None:
        self._locale_changed = True

    def setup(self) -> None:
        super().setup()
        translator.add_observer(observer=self)

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        if self._locale_changed is True:
            self._locale_changed = False
            self._text = T(self.__text)
            self._surf = self._render()

            rect = pygame.Rect(*self.pos, *self._surf.get_size())
            self.rect = rect
            self.update_align()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.rect)

    def teardown(self) -> None:
        translator.remove_observer(observer=self)

    def __repr__(self) -> str:
        return f'<TText value="{self.__text}">'


class TypeWriterText(Widget):
    def __init__(
        self,
        parent: Widget,
        text: str,
        color: Color | str,
        font: pygame.font.Font,
        width: int,
        speed: float,
        voice: str | None = None,
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        self._text = text
        self._color = color
        self._font = font
        self._speed = speed
        self._voice = voice
        self._counter = 0.0
        self._done = False
        self._surf = self._render_surf(width=width)
        self._text_surf = pygame.Surface((0, 0), pygame.SRCALPHA, 32)

        rect = pygame.Rect(*pos, *self._surf.get_size())
        super().__init__(parent=parent, rect=rect, align=align)

    def _render_surf(self, width: int) -> pygame.Surface:
        words = self._text.split(" ")
        output_text = []
        line = []

        for i, word in enumerate(words, start=1):
            line.append(word)
            rendered = self._font.render(" ".join(line), antialias=False, color=0)

            if rendered.get_width() > width:
                output_text.append(" ".join(line[:-1]))
                line = [word]

            if i >= len(words):
                output_text.append(" ".join(line))

        self._text = "\n".join(output_text)

        text_surf = self._font.render(self._text, antialias=False, color=(0, 0, 0, 0))
        surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA, 32)
        surf.set_alpha(0)

        return surf

    def is_done(self) -> bool:
        return self._done

    def skip(self) -> None:
        self._counter = len(self._text)

    def setup(self) -> None:
        self._counter = 0
        self._done = False

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        if self._done is True:
            return

        self._counter += self._speed * dt
        if self._counter >= len(self._text):
            self._done = True

        self._text_surf = self._font.render(
            self._text[0 : int(self._counter)],
            antialias=False,
            color=self._color,
        )

        if self._voice and not mixer.voice_is_busy():
            mixer.play_voice(name=self._voice)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._text_surf, self.rect)

    def teardown(self) -> None:
        pass
