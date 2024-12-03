from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def cycle(obj: Iterable[T]) -> Generator[T, None, None]:
    """Пишите ваш код здесь."""
    saved = list(obj)
    while saved:
        for item in saved:
            yield item

class Cycle:
    def __init__(self, obj: Iterable[T]):
        """Реализуйте класс"""
        self.saved = list(obj)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if not self.saved:
            raise StopIteration
        item = self.saved[self.index]
        self.index = (self.index + 1) % len(self.saved)
        return item