from __future__ import annotations

import logging

from time import sleep
from typing import TYPE_CHECKING

import pygame

import entropy

from entropy import states
from entropy.gui.components.fps import FPSViewer
from entropy.gui.input.keyboard_events import KeyboardEvents
from entropy.gui.input.mouse_events import MouseEvents
from entropy.utils import Res


if TYPE_CHECKING:
    from entropy.states import State

logger = logging.getLogger(__name__)


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
        self.mouse_e = MouseEvents()
        self.keyboard_e = KeyboardEvents()
        self.clock = pygame.time.Clock()
        self.fps_viewer = FPSViewer(clock=self.clock)

    @property
    def current_state(self) -> State:
        return self.state_stack[-1]

    def transition_to(self, state: str) -> None:
        logger.info(f'Game state changed to "{state}".')
        if len(self.state_stack) >= 1:
            self.current_state.teardown()
            self.prev_state = self.current_state

        state_cls = states.get(state)
        state = state_cls(control=self)
        state.setup()
        self.state_stack.append(state)

    def get_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE and not entropy.window.fullscreen:
                entropy.window.resize_screen(resolution=Res(event.w, event.h))

            self.keyboard_e.parse_event(event=event)
            self.mouse_e.parse_event(event=event)

    def update(self) -> None:
        entropy.mouse.update()
        if self.keyboard_e.F6:
            entropy.window.toggle_fullscreen()

        self.current_state.update(keyboard_e=self.keyboard_e, mouse_e=self.mouse_e)
        self.fps_viewer.update(keyboard_e=self.keyboard_e)

        self.keyboard_e.reset()
        self.mouse_e.reset()

    def render(self) -> None:
        self.current_state.draw(surface=self.render_surface)
        self.fps_viewer.draw(surface=self.render_surface)
        entropy.window.render(surface=self.render_surface)

    def start(self, state: str = "Splash") -> None:
        states.load()
        self.transition_to(state=state)
        self.running = True

        while self.running:
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        self.stop()

    @staticmethod
    def stop(delay: float = 0.0) -> None:
        sleep(delay)
        pygame.quit()
        exit()
