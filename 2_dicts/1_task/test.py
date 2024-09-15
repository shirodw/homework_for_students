from decimal import Decimal

import pytest
from pydantic import BaseModel, ValidationError
from main import get_parsed_employees_info


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
    employees_info = {'result': get_parsed_employees_info()}

    try:
        ListOfEmployeeInfo.model_validate(employees_info, strict=True)
    except ValidationError as e:
        assert False, str(e.errors())
