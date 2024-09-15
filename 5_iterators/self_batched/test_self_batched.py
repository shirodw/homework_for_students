from itertools import batched as real_batched

import pytest

from .self_batched import batched, Batched


class TestGeneratorBatched:
    @pytest.mark.parametrize(
        "iterable, n",
        (
            (
                "ABCDEFG", 3
            ),
            (
                [1, 2, 3, 4, 5, 6], 2
            ),
            (
                (1, 2, 3, 4, 5, 6, 7), 1
            )
        )
    )
    def test_success(self, iterable, n):
        rb = real_batched(iterable, n)
        b = batched(iterable, n)

        for idx, (rb_element, b_element) in enumerate(zip(rb, b)):
            assert rb_element == b_element


class TestClassBatched:
    @pytest.mark.parametrize(
        "iterable, n",
        (
            (
                "ABCDEFG", 3
            ),
            (
                [1, 2, 3, 4, 5, 6], 2
            ),
            (
                (1, 2, 3, 4, 5, 6, 7), 1
            )
        )
    )
    def test_success(self, iterable, n):
        rb = real_batched(iterable, n)
        b = Batched(iterable, n)

        for idx, (rb_element, b_element) in enumerate(zip(rb, b)):
            assert b_element == rb_element
