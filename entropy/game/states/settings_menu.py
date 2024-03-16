from __future__ import annotations

from enum import StrEnum
from enum import auto
from functools import partial
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame as pg

from entropy import assets
from entropy import mixer
from entropy.commands.base import Commands
from entropy.commands.display import DisableFullscreen
from entropy.commands.display import EnableFullscreen
from entropy.commands.locale import SwitchLocaleTo
from entropy.commands.mixer import PlayVoice
from entropy.commands.mixer import SaveMixerVolume
from entropy.commands.state import ExitState
from entropy.commands.state import TransitionToNextState
from entropy.config import get_config
from entropy.constants import GUI_BUTTON_FONT_SIZE
from entropy.constants import GUI_BUTTON_TEXT_COLOR
from entropy.constants import GUI_TEXT_COLOR
from entropy.event.specs import back_is_pressed
from entropy.game.states.base import State
from entropy.gui.elements.background import ColorBackground
from entropy.gui.elements.base import UIElement
from entropy.gui.elements.button import AttrObserver
from entropy.gui.elements.button import Button
from entropy.gui.elements.menu import Menu
from entropy.gui.elements.slider import Slider
from entropy.gui.elements.text import Text
from entropy.gui.elements.utils import move
from entropy.logging import get_logger
from entropy.mixer import Channel
from entropy.utils.measure import Color
from entropy.utils.measure import Size


if TYPE_CHECKING:
    from entropy.commands.base import Command
    from entropy.event.event import Event
    from entropy.game.control import Control

logger = get_logger()
config = get_config()


class Menus(StrEnum):
    SETTINGS = auto()
    DISPLAY = auto()
    SOUND = auto()
    LANGUAGE = auto()
    DIALOGUE = auto()


class SettingsMenu(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.background = ColorBackground(color=Color(0, 0, 0, 150))
        self._font = assets.font.get("LanaPixel", "lg")
        self.menu = self._build_menu(Menus.SETTINGS)

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        super().process_event(event)
        self.menu.process_event(event)

        if back_is_pressed(event):
            self.exit()

    def update(self, dt: float) -> None:
        super().update(dt)

    def draw(self, surface: pg.Surface) -> None:
        if self.control.prev_state is not None:
            self.control.prev_state.draw(surface)

        self.background.draw(surface)
        super().draw(surface)

    def teardown(self) -> None:
        super().teardown()
        config.save()

    def transition_to(self, state_name: str, with_exit: bool = False) -> None:
        self.ui_elements.empty()
        logger.debug(f'Switch to settings menu "{state_name}".')
        self.menu = self._build_menu(menu=Menus(state_name))

    def _build_menu(self, menu: Menus) -> Menu:
        margin_top_menu = 280
        space_between_buttons = 50
        margin_top_title = 150
        margin_top_back_button = 900

        back_button_action: Command = TransitionToNextState(
            state=self, next_state=Menus.SETTINGS
        )

        match menu:
            case Menus.DISPLAY:
                text_title = "DISPLAY"
                items: list[UIElement] = [
                    self._build_menu_button(
                        text="FULLSCREEN",
                        action=EnableFullscreen(),
                        attr_observer=AttrObserver(
                            subject=config, attr="fullscreen", match=True
                        ),
                        checked=config.fullscreen,
                    ),
                    self._build_menu_button(
                        text="FRAMED",
                        action=DisableFullscreen(),
                        attr_observer=AttrObserver(
                            subject=config, attr="fullscreen", match=False
                        ),
                        checked=not config.fullscreen,
                    ),
                ]

            case Menus.SOUND:
                margin_top_menu = 300
                space_between_buttons = 70
                text_title = "SOUND"
                items = [
                    self._build_menu_slider(
                        text="MAIN VOLUME",
                        initial_value=config.main_volume,
                        update_callback=partial(mixer.set_volume, channel=Channel.MAIN),
                    ),
                    self._build_menu_slider(
                        text="MUSIC VOLUME",
                        initial_value=config.music_volume,
                        update_callback=partial(
                            mixer.set_volume, channel=Channel.MUSIC
                        ),
                    ),
                    self._build_menu_slider(
                        text="ATMOSPHERE VOLUME",
                        initial_value=config.atmosphere_volume,
                        update_callback=partial(
                            mixer.set_volume, channel=Channel.ATMOSPHERE
                        ),
                    ),
                    self._build_menu_slider(
                        text="VOICE VOLUME",
                        initial_value=config.voice_volume,
                        update_callback=partial(
                            mixer.set_volume, channel=Channel.VOICE
                        ),
                        sound_on_hold=PlayVoice(name="narrator"),
                    ),
                    self._build_menu_slider(
                        text="SFX VOLUME",
                        initial_value=config.uisfx_volume,
                        update_callback=partial(
                            mixer.set_volume, channel=Channel.UISFX
                        ),
                    ),
                ]
                back_button_action = Commands([SaveMixerVolume(), back_button_action])

            case Menus.LANGUAGE:
                text_title = "LANGUAGE"
                items = [
                    self._build_menu_button(
                        text="ENGLISH",
                        action=SwitchLocaleTo(locale="en"),
                        attr_observer=AttrObserver(
                            subject=config, attr="locale", match="en"
                        ),
                        checked=config.locale == "en",
                    ),
                    self._build_menu_button(
                        text="FRANÇAIS",
                        action=SwitchLocaleTo(locale="fr"),
                        attr_observer=AttrObserver(
                            subject=config, attr="locale", match="fr"
                        ),
                        checked=config.locale == "fr",
                    ),
                ]

            case Menus.DIALOGUE:
                text_title = "DIALOGUE"
                items = []

            case _:
                text_title = "SETTINGS"
                items = [
                    self._build_menu_button(
                        text="DISPLAY",
                        action=TransitionToNextState(
                            state=self, next_state=Menus.DISPLAY
                        ),
                    ),
                    self._build_menu_button(
                        text="SOUND",
                        action=TransitionToNextState(
                            state=self, next_state=Menus.SOUND
                        ),
                    ),
                    self._build_menu_button(
                        text="LANGUAGE",
                        action=TransitionToNextState(
                            state=self, next_state=Menus.LANGUAGE
                        ),
                    ),
                    self._build_menu_button(
                        text="DIALOGUE",
                        action=TransitionToNextState(
                            state=self, next_state=Menus.DIALOGUE
                        ),
                    ),
                ]
                back_button_action = ExitState(self)

        self._build_menu_title(
            text=text_title, center=(self.background.rect.centerx, margin_top_title)
        )

        back_button = self._build_menu_button(
            text="BACK",
            action=back_button_action,
            center=(self.background.rect.centerx, margin_top_back_button),
        )

        move(
            items=items,
            space_between=space_between_buttons,
            direction="vertical",
            center=(self.background.rect.centerx, margin_top_menu),
        )

        items.append(back_button)
        return Menu(items=items, direction="vertical")

    def _build_menu_title(self, text: str, **kwargs: Any) -> None:
        Text(
            self.ui_elements,
            font=assets.font.get(name=config.font, size="lg"),
            text=text,
            color=GUI_TEXT_COLOR,
            **kwargs,
        )

    def _build_menu_button(
        self,
        action: Callable[[], None],
        text: str,
        checked: bool = False,
        attr_observer: AttrObserver | None = None,
        **kwargs: Any,
    ) -> Button:
        return Button(
            self.ui_elements,
            image=assets.gui.get("settings-button-sheet"),
            focus_sound="hover",
            click_sound="click",
            action=action,
            text=text,
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.font.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            checked=checked,
            attr_observer=attr_observer,
            **kwargs,
        )

    def _build_menu_slider(
        self,
        text: str,
        initial_value: float,
        update_callback: Callable[[float], None],
        **kwargs: Any,
    ) -> Slider:
        return Slider(
            self.ui_elements,
            initial_value=initial_value,
            size=Size(550, 30),
            min_value=0,
            max_value=1,
            update_callback=update_callback,
            button_image=assets.gui.get("slider-button-sheet"),
            sound_focus="hover",
            text=text,
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.font.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            **kwargs,
        )
