from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def batched(obj: Iterable[T], n: int) -> Generator[tuple[T], None, None]:
    """Пиши свой код здесь."""


class Batched:
    def __init__(self, obj: Iterable[T], n: int):
        """Реализуй этот класс."""
