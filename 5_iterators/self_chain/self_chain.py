from typing import TypeVar, Iterable, Generator

T = TypeVar("T")


def chain(*iterables: Iterable[T]) -> Generator[T, None, None]:
    """Пишите ваш код здесь"""


class Chain:
    def __init__(self, *iterables: Iterable[T]):
        """Реализуйте класс ниже"""
