from __future__ import annotations

import time

from time import sleep
from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.constants import GAME_NAME
from entropy.event.handler import EventQueueHandler
from entropy.event.types import inputs
from entropy.event.types import system
from entropy.game import states
from entropy.gui.elements.fps import FPSViewer
from entropy.logging import get_logger
from entropy.utils.measure import Res
from entropy.utils.measure import cleanup


if TYPE_CHECKING:
    from entropy.game.states.base import State

logger = get_logger()


class Control:
    def __init__(
        self,
        fps: float,
    ) -> None:
        self.fps = fps
        self.render_surface = pygame.Surface(entropy.window.default_res)
        self.state_stack: list[State] = []
        self.prev_state: State | None = None
        self.running = False
        self.event_manager = EventQueueHandler()
        self.clock = pygame.time.Clock()
        self.dt: float = 0.0
        self.prev_time: float = 0.0
        self.fps_viewer = FPSViewer(clock=self.clock)

    @property
    def current_state(self) -> State:
        return self.state_stack[-1]

    def transition_to(self, state_name: str, with_exit: bool = False, **kwargs) -> None:
        logger.info(f'Game state changed to "{state_name}".')
        if len(self.state_stack) >= 1:
            self.prev_state = self.current_state
            self.prev_state.teardown()

            if with_exit is True:
                self.state_stack.pop()
                cleanup(self.prev_state)
                self.prev_state = None

        state_cls = states.get(state_name)
        state = state_cls(control=self, **kwargs)
        state.setup()
        self.state_stack.append(state)

    def get_dt(self) -> None:
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def process_events(self) -> None:
        for event in self.event_manager.process_events():
            if event.triggered and event.key == system.QUIT:
                self.running = False
            elif (
                event.triggered
                and event.key == system.DISPLAY_RESIZE
                and not entropy.window.fullscreen
            ):
                entropy.window.resize_screen(resolution=Res(*event.value))
            elif event.pressed and event.key == inputs.FULLSCREEN:
                entropy.window.toggle_fullscreen()

            entropy.mouse.process_event(event=event)
            self.fps_viewer.process_event(event=event)
            self.current_state.process_event(event=event)

    def update(self) -> None:
        entropy.mouse.update()
        self.current_state.update(dt=self.dt)
        self.fps_viewer.update(dt=self.dt)

    def render(self) -> None:
        self.current_state.draw(surface=self.render_surface)
        self.fps_viewer.draw(surface=self.render_surface)
        entropy.window.render(surface=self.render_surface)

    def start(self, state: str = "Splash") -> None:
        logger.info(f"Start {GAME_NAME}.")
        states.load()
        self.transition_to(state_name=state)
        self.running = True

        while self.running:
            self.get_dt()
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        self.stop()

    @staticmethod
    def stop(delay: float = 0.2) -> None:
        logger.info(f"Stop {GAME_NAME}.")
        sleep(delay)
        pygame.quit()
        exit()
