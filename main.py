#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse

import entropy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="entropy")
    parser.add_argument("-s", "--state", type=str, default="Splash")
    args = parser.parse_args()
    state = args.state

    entropy.init()
    entropy.start(state=state)

# import gettext
#
# lang_translations = gettext.translation('base', localedir='locales', languages=["en"])
# lang_translations.install()
#
# _ = lang_translations.gettext
#
