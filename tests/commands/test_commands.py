from __future__ import annotations

import pytest

from entropy.commands.base import Commands


@pytest.fixture
def command():
    class TestCommand(Commands):
        def __init__(self, action, value):
            super().__init__()
            self.action = action
            self._value = value

        def __call__(self):
            self.action(self._value)

    return TestCommand


def test_command_call_an_action(mocker, command):
    action = mocker.Mock()
    test_command = command(action=action, value=mocker.sentinel.test)

    test_command()

    action.assert_called_once_with(mocker.sentinel.test)


def test_commands_call_all_action(mocker, command):
    action1 = mocker.Mock()
    action2 = mocker.Mock()
    test_command1 = command(action=action1, value=mocker.sentinel.test1)
    test_command2 = command(action=action2, value=mocker.sentinel.test2)
    commands = Commands([test_command1, test_command2])

    commands()

    action1.assert_called_once_with(mocker.sentinel.test1)
    action2.assert_called_once_with(mocker.sentinel.test2)
