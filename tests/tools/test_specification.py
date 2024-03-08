from __future__ import annotations

from dataclasses import dataclass

from entropy.tools.specification import Specification


@dataclass
class TestSubject:
    id: int
    name: str
    alive: bool


class SubjectIsAlive(Specification[TestSubject]):
    def is_satisfied_by(self, candidate: TestSubject) -> bool:
        return candidate.alive is True


class SubjectNameStartsWithAnA(Specification[TestSubject]):
    def is_satisfied_by(self, candidate: TestSubject) -> bool:
        return candidate.name.startswith(("a", "A"))


class SubjectIDIsZero(Specification[TestSubject]):
    def is_satisfied_by(self, candidate: TestSubject) -> bool:
        return candidate.id == 0


subject0 = TestSubject(0, "Arch", True)
subject1 = TestSubject(1, "Ape", False)


def test_is_satisfied_by() -> None:
    spec = SubjectIsAlive()

    assert spec(subject0) is True


def test_spec_and() -> None:
    spec = SubjectIsAlive() & SubjectIDIsZero()

    assert spec(subject0) is True


def test_spec_or() -> None:
    spec = SubjectNameStartsWithAnA() | SubjectIDIsZero()

    assert spec(subject1) is True


def test_spec_not() -> None:
    spec = ~SubjectIsAlive()

    assert spec(subject1) is True
