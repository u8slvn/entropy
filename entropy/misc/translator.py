from __future__ import annotations

import gettext

from entropy.locations import LOCALES_DIR


class Translator:
    def __init__(self, langs: list[str], default: str) -> None:
        self.langs = langs
        self._translations = {}
        self._translator = None
        self._build_translations()
        self.set_translation(lang=default)

    def _build_translations(self):
        for lang in self.langs:
            self._translations[lang] = gettext.translation(
                domain="base",
                localedir=LOCALES_DIR,
                languages=[lang],
            )

    def set_translation(self, lang: str):
        self._translations[lang].install()
        self._translator = self._translations[lang].gettext

    def __call__(self):
        return self._translator
