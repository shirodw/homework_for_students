from decimal import Decimal

from main import get_parsed_employees_info
from pydantic import BaseModel, ValidationError


class EmployeeInfo(BaseModel, extra='forbid'):
    id: int
    name: str
    last_name: str
    age: int
    position: str
    salary: Decimal


class ListOfEmployeeInfo(BaseModel):
    result: list[EmployeeInfo]


def test_get_parsed_employees_info():
    """Протестируем итоговый результат работы парсера.

    Если результат не соответствует требуемой структуре, то выведем ошибку.
    """
    parsed_info = get_parsed_employees_info()
    employees_info = {'result': parsed_info}

    assert len(parsed_info) > 0

    try:
        ListOfEmployeeInfo.model_validate(employees_info, strict=True)
    except ValidationError as e:
        assert False, str(e.errors())
