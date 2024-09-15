from main import get_correct_article, recover_article


def test_is_sentence_is_pangram():
    """
    Тестируем функцию восстановления статьи.
    """
    assert get_correct_article() == recover_article()
