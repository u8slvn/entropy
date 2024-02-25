from __future__ import annotations

from enum import Enum
from enum import auto
from functools import partial
from typing import TYPE_CHECKING

import pygame
import pygame as pg

from entropy import assets
from entropy import mixer
from entropy import window
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
from entropy.gui.components.templates.button import ConfigSettingsButton
from entropy.gui.components.templates.button import SettingsButton
from entropy.gui.components.templates.slider import VolumeSlider
from entropy.gui.components.templates.text import ButtonText
from entropy.gui.components.templates.text import SliderText
from entropy.gui.components.text import Text
from entropy.mixer import Channel
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.control import Control
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
        mixer.save_volumes()
        config.save()
        self._submenu.teardown()

    def transition_to(self, submenu: Submenu):
        self._submenu.teardown()
        self._submenu = self._build_submenu(submenu=submenu)
        self._submenu.setup()

    def _build_submenu(self, submenu: Submenu) -> SettingsSubmenu:
        button_x = 735
        slider_x = 685
        menu_y = 200
        menu_step = 100
        back_button_y = 900
        back_button_action = partial(self.transition_to, Submenu.SETTINGS)

        match submenu:
            case Submenu.DISPLAY:
                title = SettingsMenuTitle("DISPLAY")
                widgets = [
                    ConfigSettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 1)),
                        text=ButtonText("FULLSCREEN"),
                        callback=EnableFullscreen(),
                        attr_observer=AttrObserver(
                            subject=config, attr="fullscreen", match=True
                        ),
                    ),
                    ConfigSettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 2)),
                        text=ButtonText("FRAMED"),
                        callback=DisableFullscreen(),
                        attr_observer=AttrObserver(
                            subject=config, attr="fullscreen", match=False
                        ),
                    ),
                ]

            case Submenu.SOUND:
                menu_y = 180
                menu_step = 100
                title = SettingsMenuTitle("SOUND")
                widgets = [
                    VolumeSlider(
                        pos=(Pos(slider_x, menu_y + menu_step * 1)),
                        text=SliderText("MAIN VOLUME"),
                        initial_value=config.main_volume,
                        channel=Channel.MAIN,
                    ),
                    VolumeSlider(
                        pos=(Pos(slider_x, menu_y + menu_step * 2)),
                        text=SliderText("MUSIC VOLUME"),
                        initial_value=config.music_volume,
                        channel=Channel.MUSIC,
                    ),
                    VolumeSlider(
                        pos=(Pos(slider_x, menu_y + menu_step * 3)),
                        text=SliderText("ATMOSPHERE VOLUME"),
                        initial_value=config.atmosphere_volume,
                        channel=Channel.ATMOSPHERE,
                    ),
                    VolumeSlider(
                        pos=(Pos(slider_x, menu_y + menu_step * 4)),
                        text=SliderText("VOICE VOLUME"),
                        initial_value=config.voice_volume,
                        channel=Channel.VOICE,
                    ),
                    VolumeSlider(
                        pos=(Pos(slider_x, menu_y + menu_step * 5)),
                        text=SliderText("UI SFX VOLUME"),
                        initial_value=config.uisfx_volume,
                        channel=Channel.UISFX,
                    ),
                ]

            case Submenu.LANGUAGE:
                title = SettingsMenuTitle("LANGUAGE")
                widgets = [
                    ConfigSettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 1)),
                        text=ButtonText("ENGLISH"),
                        callback=SwitchLocaleTo(locale="en"),
                        attr_observer=AttrObserver(
                            subject=config, attr="locale", match="en"
                        ),
                    ),
                    ConfigSettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 2)),
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
                        pos=(Pos(button_x, menu_y + menu_step * 1)),
                        text=ButtonText("DISPLAY"),
                        callback=partial(self.transition_to, Submenu.DISPLAY),
                    ),
                    SettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 2)),
                        text=ButtonText("SOUND"),
                        callback=partial(self.transition_to, Submenu.SOUND),
                    ),
                    SettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 3)),
                        text=ButtonText("LANGUAGE"),
                        callback=partial(self.transition_to, Submenu.LANGUAGE),
                    ),
                    SettingsButton(
                        pos=(Pos(button_x, menu_y + menu_step * 4)),
                        text=ButtonText("DIALOGUE"),
                        callback=partial(self.transition_to, Submenu.DIALOGUE),
                    ),
                ]
                back_button_action = self.exit

        back_button = SettingsButton(
            pos=Pos(button_x, back_button_y),
            text=ButtonText("BACK"),
            callback=back_button_action,
        )

        title_x = (window.default_res.w - title.width) // 2
        title.set_pos(Pos(title_x, 150))

        widgets.append(back_button)

        menu = MenuWidgetGroup(widgets=widgets)
        return SettingsSubmenu(
            title=title,
            menu=menu,
        )


SettingsMenuTitle = partial(
    Text,
    font=assets.fonts.get(name=config.font, size="settings"),
    color=GUI_TEXT_COLOR,
)


class SettingsSubmenu(GameEntity):
    def __init__(self, title: Text, menu: MenuWidgetGroup):
        self._title = title
        self._menu = menu

    def setup(self) -> None:
        self._title.setup()
        self._menu.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._title.process_inputs(inputs=inputs)
        self._menu.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._title.update()
        self._menu.update()

    def draw(self, surface: pygame.Surface) -> None:
        self._title.draw(surface=surface)
        self._menu.draw(surface=surface)

    def teardown(self) -> None:
        self._title.teardown()
        self._menu.teardown()
