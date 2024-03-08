"""
Define event specifications in order to avoid repeating certain logics.
"""

from __future__ import annotations

from entropy.event.event import Event
from entropy.event.types import inputs
from entropy.tools.specification import Specification


class ButtonIsPressed(Specification[Event]):
    def __init__(self, button: int) -> None:
        self._button = button

    def is_satisfied_by(self, candidate: Event) -> bool:
        return candidate.pressed and candidate.key == self._button


class ButtonIsHeld(Specification[Event]):
    def __init__(self, button: int) -> None:
        self._button = button

    def is_satisfied_by(self, candidate: Event) -> bool:
        return candidate.held and candidate.key == self._button


a_is_pressed = ButtonIsPressed(button=inputs.A)
b_is_pressed = ButtonIsPressed(button=inputs.B)
click_is_pressed = ButtonIsPressed(button=inputs.CLICK)
a_or_click_is_pressed = a_is_pressed | click_is_pressed
b_or_click_is_pressed = b_is_pressed | click_is_pressed
up_is_pressed = ButtonIsPressed(button=inputs.UP)
right_is_pressed = ButtonIsPressed(button=inputs.RIGHT)
left_is_pressed = ButtonIsPressed(button=inputs.LEFT)
left_or_right_is_pressed = left_is_pressed | right_is_pressed
down_is_pressed = ButtonIsPressed(button=inputs.DOWN)
back_is_pressed = ButtonIsPressed(button=inputs.BACK)
debug_is_pressed = ButtonIsPressed(button=inputs.DEBUG)

a_is_held = ButtonIsHeld(button=inputs.A)
b_is_held = ButtonIsHeld(button=inputs.B)
up_is_held = ButtonIsHeld(button=inputs.UP)
right_is_held = ButtonIsHeld(button=inputs.RIGHT)
left_is_held = ButtonIsHeld(button=inputs.LEFT)
down_is_held = ButtonIsHeld(button=inputs.DOWN)
click_is_held = ButtonIsHeld(button=inputs.CLICK)
back_is_held = ButtonIsHeld(button=inputs.BACK)
