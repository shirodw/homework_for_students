import time
from datetime import timedelta

import pytest

from .retry import retry


class RetryStub:
    def __init__(self, count_unsuccessful_calls: int = 0, raised_exception: Exception = Exception):
        self.total_calls = 0
        self._raised_exception = raised_exception
        self._count_unsuccessful_calls = count_unsuccessful_calls

    def execute(self, *args, **kwargs) -> bool:
        self.total_calls += 1
        if self._count_unsuccessful_calls > 0:
            self._count_unsuccessful_calls -= 1
            raise self._raised_exception

        return True


def test_function_with_incorrect_count_retry():
    stub = RetryStub()
    with pytest.raises(ValueError):
        stub.execute = retry(0, timedelta(seconds=1))(stub.execute)


def test_call_function_without_errors():
    stub = RetryStub()
    stub.execute = retry(1, timedelta(seconds=1))(stub.execute)
    start = time.monotonic()
    result = stub.execute()
    result_time = time.monotonic() - start
    assert result is True
    assert result_time < timedelta(seconds=1).total_seconds()
    assert stub.total_calls == 1


@pytest.mark.parametrize(
    "args, kwargs",
    [
        (
            (1, 2, 3),
            {"a": 1, "b": 2}
        ),
        (
            (),
            {"a": 1, "b": 2}
        ),
        (
            (1, 2),
            {}
        )
    ]
)
def test_call_function_with_diff_attributes_without_error(args, kwargs):
    stub = RetryStub()
    stub.execute = retry(1, timedelta(seconds=1))(stub.execute)
    start = time.monotonic()
    result = stub.execute(*args, **kwargs)
    result_time = time.monotonic() - start
    assert result is True
    assert result_time < timedelta(seconds=1).total_seconds()
    assert stub.total_calls == 1


@pytest.mark.parametrize(
    "count_errors",
    [
        1,
        2,
        3,
        4,
    ]
)
def test_call_function_with_exception_on_set_call(count_errors):
    stub = RetryStub(count_unsuccessful_calls=count_errors)
    stub.execute = retry(count_errors+1, timedelta(milliseconds=500))(stub.execute)
    start = time.monotonic()
    result = stub.execute()
    result_time = time.monotonic() - start
    expected_time = timedelta(milliseconds=500).total_seconds() * count_errors
    assert result is True
    assert result_time >= expected_time
    assert stub.total_calls == count_errors + 1


@pytest.mark.parametrize(
    "count_errors",
    [
        1,
        2,
        3,
        4,
    ]
)
def test_call_function_with_exception_after_all_try(count_errors):
    stub = RetryStub(count_unsuccessful_calls=count_errors)
    stub.execute = retry(count_errors, timedelta(milliseconds=500))(stub.execute)
    start = time.monotonic()
    with pytest.raises(Exception):
        stub.execute()
    result_time = time.monotonic() - start
    expected_time = timedelta(milliseconds=500).total_seconds() * count_errors
    assert result_time < expected_time
    assert stub.total_calls == count_errors


def test_handle_preset_exceptions():
    stub = RetryStub(count_unsuccessful_calls=1, raised_exception=AttributeError())
    stub.execute = retry(2, timedelta(milliseconds=500), handled_exceptions=(ValueError,))(stub.execute)
    start = time.monotonic()
    with pytest.raises(AttributeError):
        stub.execute()
    result_time = time.monotonic() - start
    expected_time = timedelta(milliseconds=500).total_seconds()
    assert result_time < expected_time
    assert stub.total_calls == 1
