import csv
import dataclasses
import os
from time import strptime
from typing import Protocol


def remove_file(path: str):
    os.remove(path)


def create_file(path: str):
    with open(path, "w") as _:
        pass


class IncorrectValuesError(Exception):
    pass


@dataclasses.dataclass
class Metric:
    def __init__(self, date: str, name: str, value: str):
        self.name = name
        try:
            self.value = int(value)
            self.date = strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        except Exception:
            raise IncorrectValuesError(
                f"в файле должны быть записаны корректные значения, текущие значения: {date}, {name}, {value}"
            )

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name


class Reader(Protocol):
    def read_metrics(self, filepath: str) -> list[Metric]:
        pass


class CSVReader:
    def read_metrics(self, filepath: str) -> list[Metric]:
        metrics = []
        with open(filepath, "r") as file:
            reader = csv.reader(file, delimiter=";")
            for idx, row in enumerate(reader):
                if idx == 0:
                    continue

                metrics.append(Metric(*row))

        return metrics


class TxtReader:
    def read_metrics(self, filepath: str) -> list[Metric]:
        metrics = []
        with open(filepath, "r") as file:
            for line in file.readlines():
                date, name, value = line.split()
                metrics.append(Metric(date, name, value))

        return metrics
