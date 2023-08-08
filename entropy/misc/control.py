from __future__ import annotations

import time

from time import sleep
from typing import TYPE_CHECKING

import pygame

import entropy

from entropy import logger
from entropy import states
from entropy.gui.components.fps import FPSViewer
from entropy.gui.input import Inputs
from entropy.utils import Res


if TYPE_CHECKING:
    from entropy.states import State

logger = logger()


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
        self.inputs = Inputs()
        self.clock = pygame.time.Clock()
        self.dt = self.prev_time = 0.0
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

    def get_dt(self) -> None:
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def get_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE and not entropy.window.fullscreen:
                entropy.window.resize_screen(resolution=Res(event.w, event.h))

            self.inputs.parse_event(event=event)

    def process_inputs(self) -> None:
        if self.inputs.keyboard.F6:
            entropy.window.toggle_fullscreen()

        entropy.mouse.process_inputs(inputs=self.inputs, dt=self.dt)
        self.fps_viewer.process_inputs(inputs=self.inputs, dt=self.dt)
        self.current_state.process_inputs(inputs=self.inputs, dt=self.dt)

    def update(self) -> None:
        entropy.mouse.update()
        self.current_state.update()
        self.fps_viewer.update()

        self.inputs.reset()

    def render(self) -> None:
        self.current_state.draw(surface=self.render_surface)
        self.fps_viewer.draw(surface=self.render_surface)
        entropy.window.render(surface=self.render_surface)

    def start(self, state: str = "Splash") -> None:
        states.load()
        self.transition_to(state=state)
        self.running = True

        while self.running:
            self.get_dt()
            self.get_events()
            self.process_inputs()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        self.stop()

    @staticmethod
    def stop(delay=0.3) -> None:
        sleep(delay)
        pygame.quit()
        exit()
