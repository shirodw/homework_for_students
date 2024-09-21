import pytest

from calculator import (
    zero,
    one,
    two,
    three,
    four,
    five,
    six,
    seven,
    eight,
    nine,
    plus,
    minus,
    divided_by,
    times,
)


function_map = {
    "0": zero,
    "1": one,
    "2": two,
    "3": three,
    "4": four,
    "5": five,
    "6": six,
    "7": seven,
    "8": eight,
    "9": nine,
    "*": times,
    "/": divided_by,
    "+": plus,
    "-": minus
}


@pytest.mark.parametrize(
    "expression, result",
    [
        ("1 + 0", 1 + 0),
        ("2 + 1", 2 + 1),
        ("3 + 2", 3 + 2),
        ("4 + 5", 4 + 5),
        ("6 + 7", 6 + 7),
        ("8 + 9", 8 + 9),
        ("1 * 0", 1 * 0),
        ("2 * 1", 2 * 1),
        ("3 * 2", 3 * 2),
        ("4 * 5", 4 * 5),
        ("6 * 7", 6 * 7),
        ("8 * 9", 8 * 9),
        ("1 - 0", 1 - 0),
        ("2 - 1", 2 - 1),
        ("3 - 2", 3 - 2),
        ("5 - 4", 5 - 4),
        ("7 - 6", 7 - 6),
        ("9 - 8", 9 - 8),
        ("9 / 1", 9 // 1),
        ("8 / 2", 8 // 2),
        ("7 / 3", 7 // 3),
        ("6 / 4", 6 // 4),
    ]
)
def test_calculator(expression: str, result: int):
    left_symbol, operation_symbol, right_symbol = expression.split()
    left_op = function_map.get(left_symbol)
    operation_op = function_map.get(operation_symbol)
    right_op = function_map.get(right_symbol)
    assert result == left_op(operation_op(right_op()))
