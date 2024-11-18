import re
from collections import Counter
def top_10_most_common_words(text: str) -> dict[str, int]:
    """Функция возвращает топ 10 слов, встречающихся в тексте.

    Args:
        text: исходный текст

    Returns:
        словарь типа {слово: количество вхождений}
    """
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    words = cleaned_text.split()
    filtered_words = []
    for word in words:
        if len(word) >= 3:
            filtered_words.append(word)
    word_counts = Counter(filtered_words)
    most_common = dict(sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))[:10])
    return most_common