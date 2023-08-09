from __future__ import annotations

import gettext
import logging

from typing import Callable

from entropy.locations import LOCALES_DIR
from entropy.tools.observer import Subject


logger = logging.getLogger(__name__)


class Translator(Subject):
    def __init__(self, locales: list[str], locale: str) -> None:
        super().__init__()
        self.locales = locales
        self._translations: dict[str, gettext.GNUTranslations] = {}
        self._translator: Callable[[str], str] = lambda x: x
        self._build_translations()
        self.locale = locale
        self.set_translation(locale=self.locale)

    def _build_translations(self) -> None:
        for locale in self.locales:
            self._translations[locale] = gettext.translation(
                domain="base",
                localedir=LOCALES_DIR,
                languages=[locale],
            )

    def set_translation(self, locale: str) -> None:
        logger.info(f'Locale set to "{locale}".')
        self._translations[locale].install()
        self._translator = self._translations[locale].gettext
        self.locale = locale
        self.notify()

    def __call__(self, text: str) -> str:
        return self._translator(text)
