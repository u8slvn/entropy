from __future__ import annotations

from functools import partial

from entropy import assets
from entropy.config import get_config
from entropy.constants import GUI_BUTTON_FONT_SIZE
from entropy.constants import GUI_BUTTON_TEXT_COLOR
from entropy.gui.widgets.text import TText


config = get_config()

default_button_font = assets.font.get(name=config.font, size=GUI_BUTTON_FONT_SIZE)

ButtonText = partial(
    TText,
    font=default_button_font,
    color=GUI_BUTTON_TEXT_COLOR,
)

SliderText = partial(
    TText,
    font=default_button_font,
    color=GUI_BUTTON_TEXT_COLOR,
)
