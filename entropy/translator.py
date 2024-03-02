from __future__ import annotations

import gettext

from collections import defaultdict
from pathlib import Path
from typing import Callable

from entropy.logging import get_logger
from entropy.tools.observer import Subject


logger = get_logger()


class Translator(Subject):
    def __init__(self, localedir: Path, locale: str) -> None:
        super().__init__()
        self._localedir = localedir
        self.locales = []
        self._translations: dict[str, dict[str, gettext.GNUTranslations]] = defaultdict(
            dict
        )
        self._translator: Callable[[str], str] = lambda x: x
        self._build_translations()
        self.locale = locale
        self.set_translation(locale=self.locale)

    def _build_translations(self) -> None:
        for locale_dir in self._localedir.glob("*"):
            for locale_file in locale_dir.joinpath("LC_MESSAGES").glob("*.mo"):
                locale = locale_dir.name
                domain = locale_file.stem
                self._translations[locale][domain] = gettext.translation(
                    domain=domain,
                    localedir=self._localedir,
                    languages=[locale],
                )

    def set_translation(self, locale: str, domain: str = "base") -> None:
        logger.info(f'Locale set to "{domain}" "{locale}".')
        self._translations[locale][domain].install()
        self._translator = self._translations[locale][domain].gettext
        self.locale = locale
        self.notify()

    def __call__(self, text: str) -> str:
        return self._translator(text)
