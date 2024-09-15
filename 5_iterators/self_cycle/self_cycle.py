from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def cycle(obj: Iterable[T]) -> Generator[T, None, None]:
    """Пишите ваш код здесь."""


class Cycle:
    def __init__(self, obj: Iterable[T]):
        """Реализуйте класс"""
