import re
def format_phone(phone_number: str) -> str:
    """Функция возвращает отформатированный телефон.

    Args:
        phone_number: исходный телефон

    Returns:
        отформатированный телефон
    """
    digits = re.sub(r'\D', '', phone_number)

    if len(digits) == 11 and digits.startswith('8'):
        digits = digits[1:]
    elif len(digits) == 11 and digits.startswith('7'):
        digits = digits[1:]
    elif len(digits) == 12 and digits.startswith('7'):
        digits = digits[2:]
    elif len(digits) == 10 and digits.startswith('9'):
        pass
    else:
        return digits

    formatted_phone_number = f"8 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"

    return formatted_phone_number