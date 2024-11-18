import os
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SPLIT_SYMBOL = '\n'


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        file_article = file.read()
    return file_article


def get_employees_info() -> list[str]:
    """Внешнее апи, которое возвращает вам список строк с данными по сотрудникам."""
    return read_file(os.path.join(
        BASE_DIR, '1_task', 'input_data.txt',
    )).split(SPLIT_SYMBOL)


def get_parsed_employees_info() -> list[dict[str, int | str| Decimal]]:
    """Функция парсит данные, полученные из внешнего API и приводит их к стандартизированному виду."""
    raw_data = get_employees_info()
    parsed_employees_info = []

    # Ваш код ниже
    valid_keys = {
        'id': int,
        'name': str,
        'last_name': str,
        'age': int,
        'salary': Decimal,
        'position': str,
    }
    for data in raw_data:

        words = data.split()
        employee = {}

        for i in range(0, len(words), 2):
            key, value = words[i], words[i + 1]

            if key in valid_keys:

                if valid_keys[key] == int:
                    employee[key] = int(value)
                elif valid_keys[key] == Decimal:
                    employee[key] = Decimal(value)
                else:
                    employee[key] = value

        if set(valid_keys.keys()).issubset(employee.keys()):
            parsed_employees_info.append(employee)

    return parsed_employees_info
