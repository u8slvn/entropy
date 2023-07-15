from __future__ import annotations

import gettext
from typing import TYPE_CHECKING, Callable

from entropy.locations import LOCALES_DIR


if TYPE_CHECKING:
    from entropy.components.text import Text


class Translator:
    def __init__(self, langs: list[str], default: str) -> None:
        self.langs = langs
        self._registered_texts: list[Text] = []
        self._translations: dict[str, gettext.GNUTranslations] = {}
        self._translator: Callable[[str], str] = lambda x: x
        self._build_translations()
        self.set_translation(lang=default)

    def _build_translations(self) -> None:
        for lang in self.langs:
            self._translations[lang] = gettext.translation(
                domain="base",
                localedir=LOCALES_DIR,
                languages=[lang],
            )

    def register_text(self, text: Text) -> None:
        self._registered_texts.append(text)

    def update_texts(self) -> None:
        for text in self._registered_texts:
            text.update()

    def set_translation(self, lang: str) -> None:
        self._translations[lang].install()
        self._translator = self._translations[lang].gettext
        self.update_texts()

    def __call__(self, text: str) -> str:
        return self._translator(text)
