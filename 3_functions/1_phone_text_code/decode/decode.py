def decode_numbers(numbers: str) -> str | None:
    keypad = {
        '1': ".,?!:;",
        '2': "абвг",
        '3': "дежз",
        '4': "ийкл",
        '5': "мноп",
        '6': "рсту",
        '7': "фхчц",
        '8': "шщъы",
        '9': "ьэюя",
        '0': " "
    }
    result = []
    groups = numbers.split()
    for group in groups:
        if not group:
            continue
        if len(set(group)) != 1:
            return None
        button = group[0]
        press_count = len(group)
        if button not in keypad or press_count > len(keypad[button]):
            return None
        result.append(keypad[button][press_count - 1])
    return ''.join(result)
