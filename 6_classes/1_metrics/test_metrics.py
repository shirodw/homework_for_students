import csv
import os.path
from typing import Callable

import pytest

from metrics import get_txt_statsd, get_csv_statsd, Statsd
from helpers import CSVReader, Reader, TxtReader, remove_file, IncorrectValuesError, Metric, create_file


def test_wrong_file_for_init_statsd():
    """Тест проверяет, что мы не можем инициализировать метрики для файла с некорректным названием."""
    path = os.path.join("metrics.something")

    with pytest.raises(ValueError):
        _ = get_txt_statsd(path)

    with pytest.raises(ValueError):
        _ = get_csv_statsd(path)


@pytest.mark.parametrize(
    "filename, initializer",
    (
        ("metrics.txt", get_txt_statsd),
        ("metrics.csv", get_csv_statsd),
    )
)
def test_miss_file_for_statsd(tmp_path, filename, initializer):
    """Тест проверяет, что файл создасться, если изначально его не было."""
    temp_file = tmp_path / filename

    # файл не существует в системе - проверка ам для наглядности
    assert not temp_file.is_file()

    path = os.path.join(tmp_path, filename)
    statsd = initializer(path)
    try:
        with statsd as s:
            s.incr("test")
    except FileExistsError:
        pytest.fail("если исходного файла для хранения метрик нет, то он должен быть создан.")


@pytest.mark.parametrize(
    "filename, initializer",
    (
        ("metrics.txt", get_txt_statsd),
        ("metrics.csv", get_csv_statsd),
    )
)
def test_init_statsd(tmp_path, filename, initializer):
    """Тест проверяет, что функции инициализаторы создают нужный инстанс."""
    path = os.path.join(tmp_path, filename)

    statsd = initializer(path)

    assert isinstance(statsd, Statsd)

    remove_file(path)


@pytest.mark.parametrize(
    "filename, initializer, reader, count_metrics, expected_length",
    (
        ("metrics.txt", get_txt_statsd, TxtReader(), 1, 0),
        ("metrics.txt", get_txt_statsd, TxtReader(), 10, 10),
        ("metrics.txt", get_txt_statsd, TxtReader(), 15, 10),
        ("metrics.txt", get_txt_statsd, TxtReader(), 20, 20),
        ("metrics.txt", get_txt_statsd, TxtReader(), 21, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 1, 0),
        ("metrics.csv", get_csv_statsd, CSVReader(), 10, 10),
        ("metrics.csv", get_csv_statsd, CSVReader(), 15, 10),
        ("metrics.csv", get_csv_statsd, CSVReader(), 20, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 21, 20),
    )
)
def test_evacuate_incr_metrics_buffer(
        tmp_path,
        filename: str,
        initializer: Callable,
        reader: Reader,
        count_metrics: int,
        expected_length: int
):
    """Тест проверяет, что мы корректно используем буфер для обоих типов хранения.

    Если не заполнили достаточно буфер, то в файле ничего не должно быть.
    Если заполнили достаточно, то данные должны быть эвакуированы в файл.
    """
    path = os.path.join(tmp_path, filename)
    statsd: Statsd = initializer(path, 10)

    for _ in range(count_metrics):
        statsd.incr("test.metric.incr")

    try:
        metrics = reader.read_metrics(path)
    except IncorrectValuesError as e:
        pytest.fail(repr(e))

    assert expected_length == len(metrics)

    remove_file(path)


@pytest.mark.parametrize(
    "filename, initializer, reader, count_metrics, expected_length",
    (
        ("metrics.txt", get_txt_statsd, TxtReader(), 1, 0),
        ("metrics.txt", get_txt_statsd, TxtReader(), 10, 10),
        ("metrics.txt", get_txt_statsd, TxtReader(), 15, 10),
        ("metrics.txt", get_txt_statsd, TxtReader(), 20, 20),
        ("metrics.txt", get_txt_statsd, TxtReader(), 21, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 1, 0),
        ("metrics.csv", get_csv_statsd, CSVReader(), 10, 10),
        ("metrics.csv", get_csv_statsd, CSVReader(), 15, 10),
        ("metrics.csv", get_csv_statsd, CSVReader(), 20, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 21, 20),
    )
)
def test_evacuate_decr_metrics_buffer(
        tmp_path,
        filename: str,
        initializer: Callable,
        reader: Reader,
        count_metrics: int,
        expected_length: int
):
    """Тест проверяет, что мы корректно используем буфер для обоих типов хранения.

    Если не заполнили достаточно буфер, то в файле ничего не должно быть.
    Если заполнили достаточно, то данные должны быть эвакуированы в файл.
    """
    path = os.path.join(tmp_path, filename)
    statsd: Statsd = initializer(path, 10)

    for _ in range(count_metrics):
        statsd.decr("test.metric.incr")

    try:
        metrics = reader.read_metrics(path)
    except IncorrectValuesError as e:
        pytest.fail(repr(e))

    assert expected_length == len(metrics)

    remove_file(path)


@pytest.mark.parametrize(
    "filename, initializer, reader, count_metrics, expected_length",
    (
        ("metrics.txt", get_txt_statsd, TxtReader(), 1, 1),
        ("metrics.txt", get_txt_statsd, TxtReader(), 5, 5),
        ("metrics.txt", get_txt_statsd, TxtReader(), 12, 12),
        ("metrics.txt", get_txt_statsd, TxtReader(), 20, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 1, 1),
        ("metrics.csv", get_csv_statsd, CSVReader(), 5, 5),
        ("metrics.csv", get_csv_statsd, CSVReader(), 12, 12),
        ("metrics.csv", get_csv_statsd, CSVReader(), 20, 20),
    )
)
def test_evacuate_protected_incr_metrics_buffer_without_error(
        tmp_path,
        filename: str,
        initializer: Callable,
        reader: Reader,
        count_metrics: int,
        expected_length: int
):
    """Тест проверяет, что мы корректно используем буфер для обоих типов хранения.

    Защищенная эвакуация, которая записывает все метрики в файл, даже если буфер не заполнен.
    """
    path = os.path.join(tmp_path, filename)
    statsd: Statsd = initializer(path, 10)

    with statsd as s:
        for _ in range(count_metrics):
            s.incr("test.metric.incr")

    try:
        metrics = reader.read_metrics(path)
    except IncorrectValuesError as e:
        pytest.fail(repr(e))

    assert expected_length == len(metrics)

    remove_file(path)


@pytest.mark.parametrize(
    "filename, initializer, reader, count_metrics, expected_length",
    (
        ("metrics.txt", get_txt_statsd, TxtReader(), 1, 1),
        ("metrics.txt", get_txt_statsd, TxtReader(), 5, 5),
        ("metrics.txt", get_txt_statsd, TxtReader(), 12, 12),
        ("metrics.txt", get_txt_statsd, TxtReader(), 20, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 1, 1),
        ("metrics.csv", get_csv_statsd, CSVReader(), 5, 5),
        ("metrics.csv", get_csv_statsd, CSVReader(), 12, 12),
        ("metrics.csv", get_csv_statsd, CSVReader(), 20, 20),
    )
)
def test_evacuate_protected_decr_metrics_buffer_without_error(
        tmp_path,
        filename: str,
        initializer: Callable,
        reader: Reader,
        count_metrics: int,
        expected_length: int
):
    """Тест проверяет, что мы корректно используем буфер для обоих типов хранения.

    Защищенная эвакуация, которая записывает все метрики в файл, даже если буфер не заполнен.
    """
    path = os.path.join(tmp_path, filename)
    statsd: Statsd = initializer(path, 10)

    with statsd as s:
        for _ in range(count_metrics):
            s.decr("test.metric.incr")

    try:
        metrics = reader.read_metrics(path)
    except IncorrectValuesError as e:
        pytest.fail(repr(e))

    assert expected_length == len(metrics)

    remove_file(path)


@pytest.mark.parametrize(
    "filename, initializer, reader, count_metrics, expected_length",
    (
        ("metrics.txt", get_txt_statsd, TxtReader(), 1, 1),
        ("metrics.txt", get_txt_statsd, TxtReader(), 5, 5),
        ("metrics.txt", get_txt_statsd, TxtReader(), 12, 12),
        ("metrics.txt", get_txt_statsd, TxtReader(), 20, 20),
        ("metrics.csv", get_csv_statsd, CSVReader(), 1, 1),
        ("metrics.csv", get_csv_statsd, CSVReader(), 5, 5),
        ("metrics.csv", get_csv_statsd, CSVReader(), 12, 12),
        ("metrics.csv", get_csv_statsd, CSVReader(), 20, 20),
    )
)
def test_evacuate_protected_incr_metrics_buffer_with_error(
        tmp_path,
        filename: str,
        initializer: Callable,
        reader: Reader,
        count_metrics: int,
        expected_length: int
):
    """Тест проверяет, что мы корректно используем буфер для обоих типов хранения.

    Защищенная эвакуация, которая записывает все метрики в файл, даже если буфер не заполнен и произошла ошибка.
    """
    path = os.path.join(tmp_path, filename)
    statsd: Statsd = initializer(path, 10)

    with pytest.raises(ValueError):
        with statsd as s:
            for _ in range(count_metrics):
                s.incr("test.metric.incr")
            raise ValueError

    try:
        metrics = reader.read_metrics(path)
    except IncorrectValuesError as e:
        pytest.fail(repr(e))

    assert expected_length == len(metrics)

    remove_file(path)


@pytest.mark.parametrize(
    "filename, initializer, reader, expected_values",
    (
        (
            "metrics.txt",
            get_txt_statsd,
            TxtReader(),
            [
                Metric(date="2024-09-21T19:09:14+0000", name="test.metric.name", value="1"),
                Metric(date="2024-09-21T19:09:14+0000", name="test.metric.name", value="-1"),
            ]
        ),
        (
            "metrics.csv",
            get_csv_statsd,
            CSVReader(),
            [
                Metric(date="2024-09-21T19:09:14+0000", name="test.metric.name", value="1"),
                Metric(date="2024-09-21T19:09:14+0000", name="test.metric.name", value="-1"),
            ]
        ),
    )
)
def test_correct_values(tmp_path, filename: str, initializer, reader: Reader, expected_values: list[Metric]):
    """Тест проверяет корректность данных, записываемых в файл.

    Дату не проверяю, проверяю только порядок и формат даты.
    """
    path = os.path.join(tmp_path, filename)
    statsd: Statsd = initializer(path, 10)

    with statsd as s:
        s.incr("test.metric.name")
        s.decr("test.metric.name")

    try:
        metrics = reader.read_metrics(path)
    except IncorrectValuesError as e:
        pytest.fail(repr(e))

    for idx, metric in enumerate(metrics):
        expected_metric = expected_values[idx]
        assert expected_metric == metric

    remove_file(path)


def test_target_file_for_csv_with_header(tmp_path):
    """Тест проверяет кейс, когда у нас уже есть csv файл и в нем содержится header."""
    path = os.path.join(tmp_path, "metrics.csv")
    create_file(path)

    with open(path, "w") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["date", "metric", "value"])

    statsd: Statsd = get_csv_statsd(path, 10)

    with statsd as s:
        s.incr("test.metric.name")

    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=";")
        lines = [row for row in reader]

    assert len(lines) == 2


def test_target_file_for_csv_without_header(tmp_path):
    """Тест проверяет кейс, когда у нас уже есть csv файл и в нем НЕ содержится header."""
    path = os.path.join(tmp_path, "metrics.csv")
    create_file(path)

    statsd: Statsd = get_csv_statsd(path, 10)

    with statsd as s:
        s.incr("test.metric.name")

    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=";")
        lines = [row for row in reader]

    assert len(lines) == 2
