import time
import os
import fcntl
from typing import Dict

class _PP:
    def __init__(self, name):
        self.name = name
        self.tot_time = 0
        self.rounds = 0
        self.started = None
        self.max_time = 0

    def start(self):
        if self.started is not None:
            raise RuntimeError("Already started")
        self.started = time.perf_counter()

    def stop(self, stop_time):
        if self.started is None:
            raise RuntimeError("Not started")
        runtime = stop_time - self.started
        self.max_time = max(self.max_time, runtime)
        self.tot_time += runtime
        self.rounds += 1
        self.started = None

    def stop_if_started(self, stop_time):
        if self.started is None:
            return
        self.stop(stop_time)


__pp__: Dict[str, _PP] = {}


def pp_start(name: str):
    if name not in __pp__:
        __pp__[name] = _PP(name)
    __pp__[name].start()


def pp_stop(name: str, strict: bool = True):
    stop_time = time.perf_counter()
    if name not in __pp__:
        __pp__[name] = _PP(name)
    if strict:
        __pp__[name].stop(stop_time)
    else:
        __pp__[name].stop_if_started(stop_time)


def pp_stats():
    def _truncate(string, max_length):
        if len(string) > max_length:
            return string[: max_length - 3] + "..."
        return string

    def _print_row(row, column_widths):
        formatted_row = [_truncate(str(item), w).ljust(w) for item,w in zip(row, column_widths)]
        print(" | ".join(formatted_row))

    # Determine the maximum width of each column
    headers = ["PID", "Name", "tot_time", "rounds", "avg_time", "max_time"]
    table = [headers] + [
        [os.getpid(), pp.name, pp.tot_time, pp.rounds, pp.tot_time / pp.rounds, pp.max_time]
        for pp in sorted(__pp__.values(), key=lambda pp: pp.tot_time, reverse=True)
    ]
    assert all(len(headers) == len(row) for row in table)

    max_col_width = 25
    column_widths = [min(max_col_width, max(len(str(row[i])) for row in table)) for i in range(len(headers))]

    file_descriptor = open(os.path.expanduser("~/.omni_lock"), "w", encoding="utf-8")
    fcntl.flock(file_descriptor, fcntl.LOCK_EX)
    try:
        print(f"PP STATS for PID {os.getpid()}")
        _print_row(headers, column_widths)
        for pp in sorted(__pp__.values(), key=lambda pp: pp.tot_time, reverse=True):
            _print_row(
                [os.getpid(), pp.name, pp.tot_time, pp.rounds, pp.tot_time / pp.rounds, pp.max_time],
                column_widths
            )
        print()
    finally:
        fcntl.flock(file_descriptor, fcntl.LOCK_UN)
        file_descriptor.close()

