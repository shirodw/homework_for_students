from main import recover_article, get_correct_article


def test_is_sentence_is_pangram():
    """
    Тестируем функцию восстановления статьи.
    """
    assert get_correct_article() == recover_article()
