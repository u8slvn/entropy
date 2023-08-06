from __future__ import annotations

import gettext

from typing import Callable

from entropy.locations import LOCALES_DIR
from entropy.tools.observer import Observer


class Translator(Observer):
    def __init__(self, langs: list[str], lang: str) -> None:
        super().__init__()
        self.langs = langs
        self._translations: dict[str, gettext.GNUTranslations] = {}
        self._translator: Callable[[str], str] = lambda x: x
        self._build_translations()
        self.lang = lang
        self.set_translation(lang=self.lang)

    def _build_translations(self) -> None:
        for lang in self.langs:
            self._translations[lang] = gettext.translation(
                domain="base",
                localedir=LOCALES_DIR,
                languages=[lang],
            )

    def notify(self) -> None:
        for text in self._registered_subjects:
            text.update()

    def set_translation(self, lang: str) -> None:
        self._translations[lang].install()
        self._translator = self._translations[lang].gettext
        self.lang = lang
        self.notify()

    def __call__(self, text: str) -> str:
        return self._translator(text)
