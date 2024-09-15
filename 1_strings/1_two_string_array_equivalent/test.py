import pytest
from main import is_array_string_are_equal


@pytest.mark.parametrize(
    'array_string_1, array_string_2, expected',
    [
        (['ab', 'c'], ['a', 'bc'], True),
        (['a', 'c', 'b'], ['a', 'c'], False),
        (['abCdeFg', 'hIjK'], ['abcdefghijk'], True),
        ([], [], True),
        (['abcde'], [], False),
    ]
)
def test_is_array_string_are_equal(array_string_1: list[str], array_string_2: list[str], expected: bool):
    """
    Тестируем функцию идентичности массивов строк.

    Args:
        array_string_1: массив строк.
        array_string_2: массив строк.
        expected: ожидаемый результат.
    """
    assert is_array_string_are_equal(array_string_1, array_string_2) == expected
