import os
from datetime import datetime, timezone
from typing import List, Tuple


class Statsd:
    def __init__(self, path: str, buffer_limit: int = 10):
        self.path = path
        self.buffer_limit = buffer_limit
        self.buffer: List[Tuple[str, str, int]] = []
        self._initialize_writer()

    def _initialize_writer(self):
        if self.path.endswith(".txt"):
            self.write_metrics = self._write_txt_metrics
        elif self.path.endswith(".csv"):
            self.write_metrics = self._write_csv_metrics
        else:
            raise ValueError()

    def incr(self, name: str):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")
        self._add_metric(timestamp, name, 1)

    def decr(self, name: str):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+0000")
        self._add_metric(timestamp, name, -1)

    def _add_metric(self, timestamp: str, name: str, value: int):
        self.buffer.append((timestamp, name, value))
        if len(self.buffer) >= self.buffer_limit:
            self.flush()

    def flush(self):
        if self.buffer:
            try:
                self.write_metrics(self.buffer)
                self.buffer.clear()
                with open(self.path, 'r') as file:
                    lines = [line for line in file if line.strip()]
                with open(self.path, 'w') as file:
                    file.writelines(lines)
            except Exception:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.buffer:
            self.flush()

    def _write_txt_metrics(self, metrics: List[Tuple[str, str, int]]):
        with open(self.path, "a") as file:
            for metric in metrics:
                line = f"{metric[0]} {metric[1]} {metric[2]}\n"
                file.write(line)

    def _write_csv_metrics(self, metrics: List[Tuple[str, str, int]]):
        file_exists = os.path.exists(self.path)
        with open(self.path, "a", newline="") as file:
            if not file_exists or os.stat(self.path).st_size == 0:
                header = "date;metric;value\n"
                file.write(header)
            for metric in metrics:
                line = f"{metric[0]};{metric[1]};{metric[2]}\n"
                file.write(line)



def get_txt_statsd(path: str, buffer_limit: int = 10) -> Statsd:
    """Реализуйте инициализацию метрик для текстового файла"""
    if not os.path.exists(path):
        with open(path, "w") as file:
            pass
    return Statsd(path, buffer_limit)


def get_csv_statsd(path: str, buffer_limit: int = 10) -> Statsd:
    """Реализуйте инициализацию метрик для csv файла"""
    if not os.path.exists(path):
        with open(path, "w", newline="") as file:
            header = "date;metric;value\n"
            file.write(header)
    return Statsd(path, buffer_limit)

