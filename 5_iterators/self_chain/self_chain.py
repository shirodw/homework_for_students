from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def chain(*iterables: Iterable[T]) -> Generator[T, None, None]:
    """Пишите ваш код здесь"""
    for it in iterables:
        for item in it:
            yield item

class Chain:
    def __init__(self, *iterables: Iterable[T]):
        """Реализуйте класс ниже"""
        self.iterables = iterables
        self.current_iter = iter([])

    def __iter__(self):
        self.iterables = iter(self.iterables)
        self.current_iter = iter([])
        return self

    def __next__(self) -> T:
        while True:
            try:
                return next(self.current_iter)
            except StopIteration:
                self.current_iter = iter(next(self.iterables))