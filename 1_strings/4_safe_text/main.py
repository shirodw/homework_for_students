import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPLIT_SYMBOL = '.\n'


def get_article(path: str) -> str:
    with open(path, 'r') as file:
        file_article = file.read()
    return file_article


def get_correct_article() -> str:
    return get_article(os.path.join(BASE_DIR, '4_safe_text', 'articles', 'correct_article.txt'))


def get_wrong_article() -> str:
    return get_article(os.path.join(BASE_DIR, '4_safe_text', 'articles', 'wrong_article.txt'))


def recover_article() -> str:

    wrong_article = get_wrong_article()
    sentences = wrong_article.split(SPLIT_SYMBOL)
    recovered_sentences = []
    for sentence in sentences:
        while sentence and sentence[-1] == '!':
            sentence = sentence[:-1]
        cleaned_sentence = sentence.lower()[::-1]
        cleaned_sentence = cleaned_sentence.replace('woof-woof', 'cat')
        if cleaned_sentence:
            cleaned_sentence = cleaned_sentence[0].upper() + cleaned_sentence[1:]
        recovered_sentences.append(cleaned_sentence)
    wrong_article = SPLIT_SYMBOL.join(recovered_sentences)

    return wrong_article
