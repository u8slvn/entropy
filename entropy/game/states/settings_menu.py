from __future__ import annotations

from enum import Enum
from enum import auto
from functools import partial
from typing import TYPE_CHECKING

import pygame
import pygame as pg

from entropy import assets
from entropy.commands.display import DisableFullscreen
from entropy.commands.display import EnableFullscreen
from entropy.commands.locale import SwitchLocaleTo
from entropy.config import get_config
from entropy.constants import GUI_TEXT_COLOR
from entropy.game.entity import GameEntity
from entropy.game.states.base import State
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.button import AttrObserver
from entropy.gui.components.menu import MenuWidgetGroup
from entropy.gui.components.slider import TitledSlider
from entropy.gui.components.templates.button import ConfigSettingsButton
from entropy.gui.components.templates.button import SettingsButton
from entropy.gui.components.templates.text import ButtonText
from entropy.gui.components.templates.text import SliderText
from entropy.gui.components.text import Text
from entropy.mixer import Channel
from entropy.utils import Color
from entropy.utils import Pos
from entropy.utils import Size


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.components.button import Button
    from entropy.gui.input import Inputs


config = get_config()


class Submenu(Enum):
    SETTINGS = auto()
    DISPLAY = auto()
    SOUND = auto()
    LANGUAGE = auto()
    DIALOGUE = auto()


class SettingsMenu(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._background = ColorBackground(color=Color(0, 0, 0, 150))
        self._font = assets.fonts.get("LanaPixel", "settings")
        self._submenu = self._build_submenu(Submenu.SETTINGS)

    def setup(self) -> None:
        self._submenu.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.SPACE:
            self.exit()

        self._submenu.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._submenu.update()

    def draw(self, surface: pg.Surface) -> None:
        if self.control.prev_state is not None:
            self.control.prev_state.draw(surface=surface)

        self._background.draw(surface=surface)
        self._submenu.draw(surface=surface)

    def teardown(self) -> None:
        config.save()
        self._submenu.teardown()

    def transition_to(self, submenu: Submenu):
        self._submenu.teardown()
        self._submenu = self._build_submenu(submenu=submenu)
        self._submenu.setup()

    def _build_submenu(self, submenu: Submenu) -> SettingsSubmenu:
        back_button = SettingsButton(
            text=ButtonText("BACK"),
            callback=partial(self.transition_to, Submenu.SETTINGS),
        )
        match submenu:
            case Submenu.DISPLAY:
                title = SettingsMenuTitle("DISPLAY")
                widgets = [
                    ConfigSettingsButton(
                        text=ButtonText("FULLSCREEN"),
                        callback=EnableFullscreen(),
                        attr_observer=AttrObserver(
                            subject=config, attr="fullscreen", match=True
                        ),
                    ),
                    ConfigSettingsButton(
                        text=ButtonText("FRAMED"),
                        callback=DisableFullscreen(),
                        attr_observer=AttrObserver(
                            subject=config, attr="fullscreen", match=False
                        ),
                    ),
                ]

            case Submenu.SOUND:
                title = SettingsMenuTitle("SOUND")
                widgets = [
                    TitledSlider(
                        text=SliderText("MAIN VOLUME"),
                        size=Size(550, 30),
                        initial_value=config.main_volume,
                        min=0,
                        max=1,
                        button=assets.images.get("slider-button-sheet"),
                        channel=Channel.GENERAL,
                    ),
                    TitledSlider(
                        text=SliderText("MUSIC VOLUME"),
                        size=Size(550, 30),
                        initial_value=config.music_volume,
                        min=0,
                        max=1,
                        button=assets.images.get("slider-button-sheet"),
                        channel=Channel.MUSIC,
                    ),
                    TitledSlider(
                        text=SliderText("ATMOSPHERE VOLUME"),
                        size=Size(550, 30),
                        initial_value=config.atmosphere_volume,
                        min=0,
                        max=1,
                        button=assets.images.get("slider-button-sheet"),
                        channel=Channel.ATMOSPHERE,
                    ),
                    TitledSlider(
                        text=SliderText("VOICE VOLUME"),
                        size=Size(550, 30),
                        initial_value=config.voice_volume,
                        min=0,
                        max=1,
                        button=assets.images.get("slider-button-sheet"),
                        channel=Channel.VOICE,
                    ),
                    TitledSlider(
                        text=SliderText("UI SFX VOLUME"),
                        size=Size(550, 30),
                        initial_value=config.uisfx_volume,
                        min=0,
                        max=1,
                        button=assets.images.get("slider-button-sheet"),
                        channel=Channel.UISFX,
                    ),
                ]

            case Submenu.LANGUAGE:
                title = SettingsMenuTitle("LANGUAGE")
                widgets = [
                    ConfigSettingsButton(
                        text=ButtonText("ENGLISH"),
                        callback=SwitchLocaleTo(locale="en"),
                        attr_observer=AttrObserver(
                            subject=config, attr="locale", match="en"
                        ),
                    ),
                    ConfigSettingsButton(
                        text=ButtonText("FRANÇAIS"),
                        callback=SwitchLocaleTo(locale="fr"),
                        attr_observer=AttrObserver(
                            subject=config, attr="locale", match="fr"
                        ),
                    ),
                ]

            case Submenu.DIALOGUE:
                title = SettingsMenuTitle("DIALOGUE")
                widgets = []

            case _:
                title = SettingsMenuTitle("SETTINGS")
                widgets = [
                    SettingsButton(
                        text=ButtonText("DISPLAY"),
                        callback=partial(self.transition_to, Submenu.DISPLAY),
                    ),
                    SettingsButton(
                        text=ButtonText("SOUND"),
                        callback=partial(self.transition_to, Submenu.SOUND),
                    ),
                    SettingsButton(
                        text=ButtonText("LANGUAGE"),
                        callback=partial(self.transition_to, Submenu.LANGUAGE),
                    ),
                    SettingsButton(
                        text=ButtonText("DIALOGUE"),
                        callback=partial(self.transition_to, Submenu.DIALOGUE),
                    ),
                ]
                back_button = SettingsButton(
                    text=ButtonText("BACK"),
                    callback=self.exit,
                )

        menu = MenuWidgetGroup(
            pos=Pos(0, 310),
            margin=30,
            widgets=widgets,
            center_x=True,
        )
        return SettingsSubmenu(title=title, menu=menu, back_button=back_button)


SettingsMenuTitle = partial(
    Text,
    font=assets.fonts.get(name=config.font, size="settings"),
    color=GUI_TEXT_COLOR,
)


class SettingsSubmenu(GameEntity):
    def __init__(self, title: Text, menu: MenuWidgetGroup, back_button: Button):
        self._title = title
        self._menu = menu
        self._back_button = back_button

    def setup(self) -> None:
        self._title.setup()
        self._menu.setup()
        self._back_button.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._title.process_inputs(inputs=inputs)
        self._menu.process_inputs(inputs=inputs)
        self._back_button.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._title.update()
        self._menu.update()
        self._back_button.update()

    def draw(self, surface: pygame.Surface) -> None:
        self._title.set_pos(pos=Pos(0, 150), center_x=True)
        self._title.draw(surface=surface)
        self._menu.draw(surface=surface)
        self._back_button.set_pos(pos=Pos(0, 900), center_x=True)
        self._back_button.draw(surface=surface)

    def teardown(self) -> None:
        self._title.teardown()
        self._menu.teardown()
        self._back_button.teardown()
