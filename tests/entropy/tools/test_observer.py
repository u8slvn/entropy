from __future__ import annotations

from entropy.tools.observer import Observer
from entropy.tools.observer import Subject


class ObserverTest(Observer):
    def __init__(self, action):
        self.action = action

    def on_notify(self):
        self.action()


class SubjectTest(Subject):
    pass


def test_subject_calls_its_observers(mocker):
    subject = SubjectTest()
    observer1 = ObserverTest(mocker.Mock())
    observer2 = ObserverTest(mocker.Mock())
    subject.subscribe(observer1)
    subject.subscribe(observer2)

    subject.notify()

    observer1.action.assert_called_once()
    observer2.action.assert_called_once()


def test_subject_dont_call_unsubscribed_subject(mocker):
    subject = SubjectTest()
    observer = ObserverTest(mocker.Mock())
    subject.subscribe(observer)

    subject.unsubscribe(observer)
    subject.notify()

    observer.action.assert_not_called()
