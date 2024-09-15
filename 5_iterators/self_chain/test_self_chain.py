from itertools import chain as real_chain
from typing import Iterable

import pytest

from .self_chain import Chain, chain


class TestGeneratorChain:
    @pytest.mark.parametrize(
        "iterable_objects",
        [
            ["1234", [1, 2, 3, 4], ["a", "b", 1], {1: 1, 2: 2}],
            ["1234", []]
        ]
    )
    def test_success(self, iterable_objects: list[Iterable]):
        rc = real_chain(*iterable_objects)
        c = chain(*iterable_objects)

        for idx, (rc_element, c_element) in enumerate(zip(rc, c)):
            assert rc_element == c_element


class TestClassChain:
    @pytest.mark.parametrize(
        "iterable_objects",
        [
            ["1234", [1, 2, 3, 4], ["a", "b", 1], {1: 1, 2: 2}],
            ["1234", []]
        ]
    )
    def test_success(self, iterable_objects: Iterable):
        rc = real_chain(*iterable_objects)
        c = Chain(*iterable_objects)

        for idx, (rc_element, c_element) in enumerate(zip(rc, c)):
            assert rc_element == c_element
