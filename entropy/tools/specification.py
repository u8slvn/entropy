from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Generic
from typing import TypeVar


T = TypeVar("T")


class Specification(Generic[T], ABC):
    """Specification base class"""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        raise NotImplementedError

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def __and__(self, spec: Specification[T]) -> _AndSpecification[T]:
        return _AndSpecification(self, spec)

    def __or__(self, spec: Specification[T]) -> _OrSpecification[T]:
        return _OrSpecification(self, spec)

    def __invert__(self) -> _NotSpecification[T]:  # not
        return _NotSpecification(self)

    def __call__(self, candidate: Any) -> bool:
        """Additional syntax for ease of use."""
        return self.is_satisfied_by(candidate)

    def __repr__(self) -> str:
        return f"<{self.class_name}>"


class _AndOrSpecification(Specification[T]):
    """Base class for 'And' and 'Or' specifications."""

    def __init__(self, spec_a: Specification[T], spec_b: Specification[T]) -> None:
        super().__init__()
        self._specs = (spec_a, spec_b)

    def is_satisfied_by(self, candidate: T) -> bool:
        results = (spec.is_satisfied_by(candidate) for spec in self._specs)

        return self._check(*results)

    @abstractmethod
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        """Check the operator logic."""
        raise NotImplementedError


class _AndSpecification(_AndOrSpecification[T]):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a and spec_b


class _OrSpecification(_AndOrSpecification[T]):
    def _check(self, spec_a: bool, spec_b: bool) -> bool:
        return spec_a or spec_b


class _NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]) -> None:
        super().__init__()
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        result = self._spec.is_satisfied_by(candidate)

        return not result
