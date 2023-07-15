from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING
from typing import Type

import pygame as pg

import entropy

from entropy.components.fps import FPSViewer
from entropy.misc.action import Actions
from entropy.misc.mouse import Mouse
from entropy.utils import Resolution


if TYPE_CHECKING:
    from entropy.states import State


class Control:
    def __init__(
        self,
        fps: float,
    ) -> None:
        self.fps = fps
        self.render_surface = pg.Surface(entropy.window.render_res).convert()
        self.state_stack: list[State] = []
        self.prev_state: State | None = None
        from entropy.states.splash import Splash  # Fix this shit late

        self.transition_to(state=Splash)
        self.running = False
        self.clock = pg.time.Clock()
        self.fps_viewer = FPSViewer(clock=self.clock)
        self.mouse = Mouse()
        self.actions = Actions()

    @property
    def current_state(self) -> State:
        return self.state_stack[-1]

    def transition_to(self, state: Type[State]) -> None:
        if len(self.state_stack) > 1:
            self.prev_state = self.current_state
        self.state_stack.append(state(control=self))

    def get_events(self) -> None:
        self.mouse.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.VIDEORESIZE and not entropy.window.fullscreen:
                entropy.window.resize_screen(resolution=Resolution(event.w, event.h))

            self.current_state.handle_event(event=event)
            self.actions.parse_event(event=event)

    def update(self) -> None:
        if self.actions.F6:
            entropy.window.toggle_fullscreen()

        self.current_state.update(actions=self.actions, mouse=self.mouse)
        self.fps_viewer.update(actions=self.actions)

        self.actions.reset()

    def render(self) -> None:
        self.current_state.draw(surface=self.render_surface)
        self.fps_viewer.draw(surface=self.render_surface)
        entropy.window.render(surface=self.render_surface)

    def start(self) -> None:
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
        pg.quit()
        exit()
