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
from entropy.commands.state import TransitionToNextState
from entropy.config import get_config
from entropy.constants import GUI_BUTTON_FONT_SIZE
from entropy.constants import GUI_BUTTON_TEXT_COLOR
from entropy.constants import GUI_TEXT_COLOR
from entropy.game.states.base import State
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.base import ALIGN
from entropy.gui.components.button import AttrObserver
from entropy.gui.components.button import ObserverButton
from entropy.gui.components.button import TextButton
from entropy.gui.components.menu import Group
from entropy.gui.components.menu import MenuGroup
from entropy.gui.components.text import TText
from entropy.utils import Color
from entropy.utils import Pos


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
        # slider_x = 685
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
                        "button_cls": ObserverButton,
                        "text": "FULLSCREEN",
                        "callback": EnableFullscreen(),
                        "attr_observer": AttrObserver(
                            subject=config, attr="fullscreen", match=True
                        ),
                    },
                    {
                        "button_cls": ObserverButton,
                        "text": "FRAMED",
                        "callback": DisableFullscreen(),
                        "attr_observer": AttrObserver(
                            subject=config, attr="fullscreen", match=False
                        ),
                    },
                ]

            case Submenu.SOUND:
                # menu_y = 180
                # menu_step = 100
                text_title = "SOUND"
                widgets = [
                    # VolumeSlider(
                    #     pos=(Pos(slider_x, menu_y + menu_step * 1)),
                    #     text=SliderText("MAIN VOLUME"),
                    #     initial_value=config.main_volume,
                    #     channel=Channel.MAIN,
                    # ),
                    # VolumeSlider(
                    #     pos=(Pos(slider_x, menu_y + menu_step * 2)),
                    #     text=SliderText("MUSIC VOLUME"),
                    #     initial_value=config.music_volume,
                    #     channel=Channel.MUSIC,
                    # ),
                    # VolumeSlider(
                    #     pos=(Pos(slider_x, menu_y + menu_step * 3)),
                    #     text=SliderText("ATMOSPHERE VOLUME"),
                    #     initial_value=config.atmosphere_volume,
                    #     channel=Channel.ATMOSPHERE,
                    # ),
                    # VolumeSlider(
                    #     pos=(Pos(slider_x, menu_y + menu_step * 4)),
                    #     text=SliderText("VOICE VOLUME"),
                    #     initial_value=config.voice_volume,
                    #     channel=Channel.VOICE,
                    # ),
                    # VolumeSlider(
                    #     pos=(Pos(slider_x, menu_y + menu_step * 5)),
                    #     text=SliderText("UI SFX VOLUME"),
                    #     initial_value=config.uisfx_volume,
                    #     channel=Channel.UISFX,
                    # ),
                ]

            case Submenu.LANGUAGE:
                text_title = "LANGUAGE"
                widgets = [
                    {
                        "button_cls": ObserverButton,
                        "text": "ENGLISH",
                        "callback": SwitchLocaleTo(locale="en"),
                        "attr_observer": AttrObserver(
                            subject=config, attr="locale", match="en"
                        ),
                    },
                    {
                        "button_cls": ObserverButton,
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
                        "button_cls": TextButton,
                        "text": "DISPLAY",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.DISPLAY
                        ),
                    },
                    {
                        "button_cls": TextButton,
                        "text": "SOUND",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.SOUND
                        ),
                    },
                    {
                        "button_cls": TextButton,
                        "text": "LANGUAGE",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.LANGUAGE
                        ),
                    },
                    {
                        "button_cls": TextButton,
                        "text": "DIALOGUE",
                        "callback": TransitionToNextState(
                            state=self, next_state=Submenu.DIALOGUE
                        ),
                    },
                ]
                back_button_action = self.exit

        for i, widget in enumerate(widgets, start=1):
            pos = Pos(0, margin_top_menu + space_between_buttons * i)
            button = self._build_menu_button(parent=menu_group, **widget, pos=pos)
            menu_group.add_widget(widget=button)

        title = self._build_menu_title(
            parent=group, text=text_title, pos=Pos(0, margin_top_title)
        )
        back_button = self._build_menu_button(
            button_cls=TextButton,
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
    def _build_menu_button(button_cls: Type[TextButton], **kwargs) -> TextButton:
        return button_cls(
            **kwargs,
            image=assets.images.get("settings-button-sheet"),
            sound_focus="hover",
            sound_clicked="click",
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.fonts.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            text_align=ALIGN.CENTER,
            align=ALIGN.CENTER_X,
        )
