import pytest

from main import is_sentence_is_pangram


@pytest.mark.parametrize(
    'sentence, expected',
    [
        ('thequickbrownfoxjumpsoverthelazydog', True),
        ('helloworld', False),
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', True),
        ('', False),
    ]
)
def test_is_sentence_is_pangram(sentence: str, expected: bool):
    """
    Тестируем функцию идентичности массивов строк.

    Args:
        sentence: предложение.
        expected: ожидаемый результат.
    """
    assert is_sentence_is_pangram(sentence) == expected
