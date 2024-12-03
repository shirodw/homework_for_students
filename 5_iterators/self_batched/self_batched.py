from typing import Generator, Iterable, TypeVar

T = TypeVar("T")


def batched(obj: Iterable[T], n: int) -> Generator[tuple[T], None, None]:
    """Пиши свой код здесь."""
    obj = iter(obj)
    while True:
        batch = []
        for _ in range(n):
            try:
                batch.append(next(obj))
            except StopIteration:
                break
        if not batch:
            break
        yield tuple(batch)


class Batched:
    def __init__(self, obj: Iterable[T], n: int):
        """Реализуй этот класс."""
        self.obj = iter(obj)
        self.n = n

    def __iter__(self):
        return self

    def __next__(self) -> tuple[T, ...]:
        batch = []
        for _ in range(self.n):
            try:
                batch.append(next(self.obj))
            except StopIteration:
                break
        if not batch:
            raise StopIteration
        return tuple(batch)