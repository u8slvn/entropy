from collections import OrderedDict

import pygame

from entropy.misc.game import Game
from entropy.misc.window import FullScreenResolution, Monitor, Resolution
from entropy.states.menu import Menu
from entropy.states.splash import Splash


def create_game(title: str) -> Game:
    pygame.init()
    monitor = Monitor()
    game = Game(title=title, monitor=monitor)

    resolutions = OrderedDict(
        {
            "SD": Resolution(width=720, height=480),
            "SHD": Resolution(width=1280, height=720),
            "FHD": Resolution(width=1920, height=1080),
            "FULLSCREEN": FullScreenResolution(monitor=monitor),
        }
    )
    game.setup_resolution(resolutions=resolutions, default_resolution="FULLSCREEN")

    states = {
        "SPLASH": Splash(game=game),
        "MENU": Menu(game=game),
    }
    game.setup_states(states=states, default_state="SPLASH")

    return game
