from __future__ import annotations

from enum import StrEnum
from enum import auto
from typing import TYPE_CHECKING
from typing import Type

import pygame as pg

from entropy import assets
from entropy import mixer
from entropy.commands.display import DisableFullscreen
from entropy.commands.display import EnableFullscreen
from entropy.commands.locale import SwitchLocaleTo
from entropy.commands.sound import SetVolume
from entropy.commands.state import TransitionToNextState
from entropy.config import get_config
from entropy.constants import GUI_BUTTON_FONT_SIZE
from entropy.constants import GUI_BUTTON_TEXT_COLOR
from entropy.constants import GUI_TEXT_COLOR
from entropy.game.states.base import State
from entropy.gui.components import button
from entropy.gui.components import slider
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.base import ALIGN
from entropy.gui.components.button import AttrObserver
from entropy.gui.components.button import ObserverButton
from entropy.gui.components.button import TextButton
from entropy.gui.components.menu import Group
from entropy.gui.components.menu import MenuGroup
from entropy.gui.components.slider import TitledSlider
from entropy.gui.components.text import TText
from entropy.mixer import Channel
from entropy.utils import Color
from entropy.utils import Pos
from entropy.utils import Size


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.components.base import Widget
    from entropy.gui.input import Inputs

config = get_config()


class Submenu(StrEnum):
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

    def transition_to(self, state_name: str):
        self._submenu.teardown()
        self._submenu = self._build_submenu(submenu=Submenu(state_name))
        self._submenu.setup()

    def _build_submenu(self, submenu: Submenu) -> Group:
        margin_top_menu = 200
        space_between_buttons = 100
        margin_top_title = 150
        margin_top_back_button = 900

        group = Group(parent=self._background)
        menu_group = MenuGroup(parent=group)

        back_button_action = TransitionToNextState(
            state=self, next_state=Submenu.SETTINGS
        )

        match submenu:
            case Submenu.DISPLAY:
                text_title = "DISPLAY"
                widgets = [
                    {
                        "widget_cls": ObserverButton,
                        "text": "FULLSCREEN",
                        "callback": EnableFullscreen(),
                        "attr_observer": AttrObserver(
                            subject=config, attr="fullscreen", match=True
                        ),
                    },
                    {
                        "widget_cls": ObserverButton,
                        "text": "FRAMED",
                        "callback": DisableFullscreen(),
                        "attr_observer": AttrObserver(
                            subject=config, attr="fullscreen", match=False
                        ),
                    },
                ]

            case Submenu.SOUND:
                margin_top_menu = 190
                text_title = "SOUND"
                widgets = [
                    {
                        "widget_cls": TitledSlider,
                        "text": "MAIN VOLUME",
                        "initial_value": config.main_volume,
                        "command": SetVolume(channel=Channel.MAIN),
                    },
                    {
                        "widget_cls": TitledSlider,
                        "text": "MUSIC VOLUME",
                        "initial_value": config.music_volume,
                        "command": SetVolume(channel=Channel.MUSIC),
                    },
                    {
                        "widget_cls": TitledSlider,
                        "text": "ATMOSPHERE VOLUME",
                        "initial_value": config.atmosphere_volume,
                        "command": SetVolume(channel=Channel.ATMOSPHERE),
                    },
                    {
                        "widget_cls": TitledSlider,
                        "text": "VOICE VOLUME",
                        "initial_value": config.voice_volume,
                        "command": SetVolume(channel=Channel.VOICE),
                    },
                    {
                        "widget_cls": TitledSlider,
                        "text": "SFX VOLUME",
                        "initial_value": config.uisfx_volume,
                        "command": SetVolume(channel=Channel.UISFX),
                    },
                ]

            case Submenu.LANGUAGE:
                text_title = "LANGUAGE"
                widgets = [
                    {
                        "widget_cls": ObserverButton,
                        "text": "ENGLISH",
                        "callback": SwitchLocaleTo(locale="en"),
                        "attr_observer": AttrObserver(
                            subject=config, attr="locale", match="en"
                        ),
                    },
                    {
                        "widget_cls": ObserverButton,
                        "text": "FRANÇAIS",
                        "callback": SwitchLocaleTo(locale="fr"),
                        "attr_observer": AttrObserver(
                            subject=config, attr="locale", match="fr"
                        ),
                    },
                ]

            case Submenu.DIALOGUE:
                text_title = "DIALOGUE"
                widgets = []

            case _:
                text_title = "SETTINGS"
                widgets = [
                    {
                        "widget_cls": TextButton,
                        "text": "DISPLAY",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.DISPLAY
                        ),
                    },
                    {
                        "widget_cls": TextButton,
                        "text": "SOUND",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.SOUND
                        ),
                    },
                    {
                        "widget_cls": TextButton,
                        "text": "LANGUAGE",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.LANGUAGE
                        ),
                    },
                    {
                        "widget_cls": TextButton,
                        "text": "DIALOGUE",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.DIALOGUE
                        ),
                    },
                ]
                back_button_action = self.exit

        for i, widget in enumerate(widgets, start=1):
            pos = Pos(0, margin_top_menu + space_between_buttons * i)
            button = self._build_menu_widget(parent=menu_group, **widget, pos=pos)
            menu_group.add_widget(widget=button)

        title = self._build_menu_title(
            parent=group, text=text_title, pos=Pos(0, margin_top_title)
        )
        back_button = self._build_menu_widget(
            widget_cls=TextButton,
            parent=menu_group,
            text="BACK",
            callback=back_button_action,
            pos=Pos(0, margin_top_back_button),
        )

        menu_group.add_widget(widget=back_button)

        group.add_widgets(widgets=[title, menu_group])

        return group

    @staticmethod
    def _build_menu_title(parent: Widget, text: str, pos: Pos):
        return TText(
            parent=parent,
            text=text,
            font=assets.fonts.get(name=config.font, size="settings"),
            color=GUI_TEXT_COLOR,
            pos=pos,
            align=ALIGN.CENTER_X,
        )

    @staticmethod
    def _build_menu_widget(
        widget_cls: Type[TextButton] | Type[ObserverButton] | Type[TitledSlider],
        **kwargs,
    ) -> Widget:
        text_font = assets.fonts.get(name=config.font, size=GUI_BUTTON_FONT_SIZE)

        match widget_cls:
            case button.TextButton | button.ObserverButton:
                return widget_cls(
                    **kwargs,
                    image=assets.images.get("settings-button-sheet"),
                    sound_focus="hover",
                    sound_clicked="click",
                    text_color=GUI_BUTTON_TEXT_COLOR,
                    text_font=text_font,
                    text_align=ALIGN.CENTER,
                    align=ALIGN.CENTER_X,
                )

            case slider.TitledSlider:
                return widget_cls(
                    **kwargs,
                    size=Size(550, 30),
                    min_value=0,
                    max_value=1,
                    button_image=assets.images.get("slider-button-sheet"),
                    sound_focus="hover",
                    text_color=GUI_BUTTON_TEXT_COLOR,
                    text_font=text_font,
                    space_between=30,
                    text_align=ALIGN.CENTER_X,
                    align=ALIGN.CENTER_X,
                )
