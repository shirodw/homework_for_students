import pytest

from main import get_max_number_of_words_from_sentences


@pytest.mark.parametrize(
    'sentences, expected',
    [
        (["alice and bob love cats", "i think so too", "this is great thanks very much"], 6),
        (["please wait", "continue to fight", "continue to win"], 3),
        (['', ''], 0),
    ]
)
def test_get_max_number_of_words_from_sentences(sentences: list[str], expected: bool):
    """
    Тестируем функцию идентичности массивов строк.

    Args:
        sentences: массив предложений.
        expected: ожидаемый результат.
    """
    assert get_max_number_of_words_from_sentences(sentences) == expected
