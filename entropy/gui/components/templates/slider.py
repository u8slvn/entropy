from __future__ import annotations

from functools import partial

from entropy import assets
from entropy.gui.components.slider import TitledSlider
from entropy.utils import Size


VolumeSlider = partial(
    TitledSlider,
    size=Size(550, 30),
    min_value=0,
    max_value=1,
    button=assets.images.get("slider-button-sheet"),
    sound_focus="hover",
)
