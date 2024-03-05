from __future__ import annotations

import pytest

from entropy.commands.base import Commands
from entropy.commands.base import ConfigurableCommand


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


@pytest.fixture
def configurable_command():
    class TestConfigurableCommand(ConfigurableCommand):

        def __init__(self, action, value):
            super().__init__()
            self.action = action
            self._value = value

        def __call__(self):
            self.action(*self._args, self._value)

    return TestConfigurableCommand


def test_command_call_an_action(mocker, command):
    action = mocker.Mock()
    test_command = command(action=action, value=mocker.sentinel.test)

    test_command()

    action.assert_called_once_with(mocker.sentinel.test)


def test_configurable_command_call_an_action(mocker, configurable_command):
    action = mocker.Mock()
    test_command = configurable_command(action=action, value=mocker.sentinel.test)

    test_command.configure(10)
    test_command()

    action.assert_called_once_with(10, mocker.sentinel.test)
