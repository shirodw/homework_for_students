import csv
import os
from datetime import datetime, timezone
from typing import Protocol


class Storage(Protocol):
    def write(self, metrics: list[tuple[str, str, int]]):
        pass


class TxtStorage:
    def __init__(self, path: str):
        self.path = path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as _:
                pass

    def write(self, metrics: list[tuple[str, str, int]]):
        with open(self.path, "a") as file:
            for metric in metrics:
                file.write(f"{metric[0]} {metric[1]} {metric[2]}\n")


class CsvStorage:
    def __init__(self, path: str):
        self.path = path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as _:
                pass

    def write(self, metrics: list[tuple[str, str, int]]):
        with open(self.path, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            if os.path.getsize(self.path) == 0:
                writer.writerow(["date", "metric", "value"])
            for metric in metrics:
                writer.writerow(metric)


class Statsd:
    def __init__(self, storage: Storage, buffer_size: int = 10):
        self.storage = storage
        self.buffer_size = buffer_size
        self.buffer = []

    def incr(self, metric_name: str):
        self._add_metric(metric_name, 1)

    def decr(self, metric_name: str):
        self._add_metric(metric_name, -1)

    def _add_metric(self, metric_name: str, value: int):
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        self.buffer.append((now, metric_name, value))
        if len(self.buffer) >= self.buffer_size:
            self._evacuate()

    def _evacuate(self):
        if self.buffer:
            self.storage.write(self.buffer)
            self.buffer = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._evacuate()


def get_txt_statsd(path: str, buffer: int = 10) -> Statsd:
    if not path.endswith(".txt"):
        raise ValueError()
    storage = TxtStorage(path)
    return Statsd(storage, buffer)


def get_csv_statsd(path: str, buffer: int = 10) -> Statsd:
    if not path.endswith(".csv"):
        raise ValueError()
    storage = CsvStorage(path)
    return Statsd(storage, buffer)