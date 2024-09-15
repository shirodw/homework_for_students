import pytest
from main import format_phone

STANDARD = "8 (901) 123-45-67"

@pytest.mark.parametrize(
    'input_phone, result_phone',
    [
        ("89011234567", STANDARD),
        ("9011234567", STANDARD),
        ("79011234567", STANDARD),
        ("+79011234567", STANDARD),
        ("8 __()-! 901-123-45-67", STANDARD),
        ("+7901-123-45   67", STANDARD),
        ("#@!(zz8901-___123-45gg67 какая-то ещё петрушка R$&*z", STANDARD)
    ]
)
def test_format_phone(input_phone, result_phone):
    assert format_phone(input_phone) == result_phone
