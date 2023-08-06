from __future__ import annotations

from entropy import config
from entropy import translator
from entropy.commands.base import Command


class SwitchLocaleTo(Command):
    def __init__(self, lang: str):
        self._lang = lang

    def __call__(
        self,
    ) -> None:
        if translator.lang == self._lang:
            return

        translator.set_translation(lang=self._lang)
        config.update_attr(name="lang", value=self._lang)
