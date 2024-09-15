from itertools import cycle as real_cycle, zip_longest
from typing import Iterable

import pytest

from .self_cycle import cycle, Cycle


class TestGeneratorCycle:
    @pytest.mark.parametrize(
        "iterable_object",
        [
            "1234",
            [1, 2, 3, 4],
            {1: 1, 2: 2, 3: 3},
            {1, 2, 3, 4},
            (1, 2, 3, 4),
        ]
    )
    def test_success(self, iterable_object: Iterable):
        rc = real_cycle(iterable_object)
        c = cycle(iterable_object)

        stop_idx = 100
        for idx, (rc_element, c_element) in enumerate(zip_longest(rc, c)):
            assert rc_element == c_element
            if idx == stop_idx:
                break


class TestClassCycle:
    @pytest.mark.parametrize(
        "iterable_object",
        [
            "1234",
            [1, 2, 3, 4],
            {1: 1, 2: 2, 3: 3},
            {1, 2, 3, 4},
            (1, 2, 3, 4),
        ]
    )
    def test_success(self, iterable_object: Iterable):
        rc = real_cycle(iterable_object)
        c = Cycle(iterable_object)

        stop_idx = 100
        for idx, (rc_element, c_element) in enumerate(zip_longest(rc, c)):
            assert rc_element == c_element
            if idx == stop_idx:
                break