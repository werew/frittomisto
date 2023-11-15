"""
Perf measuring utilities
"""
import time
import os
import fcntl
from typing import Dict, Optional, List, Union
from itertools import chain


class _PP:
    def __init__(self, name: str):
        """
        name: name of the profiler
        """
        self.name: str = name
        self.tot_time: float = 0
        self.rounds: int = 0
        self.started: Optional[float] = None
        self.max_time = 0

    def start(self) -> None:
        """
        Starts the perf counter
        """
        if self.started is not None:
            raise RuntimeError("Already started")
        self.started = time.perf_counter()

    def stop(self, stop_time: float) -> None:
        """
        Stops the perf counter, trowhs an error if it was not started.
        Note: `stop_time` is the time returned by `time.perf_counter()`,
        this value is passed as parameter to avoid overhead.
        """
        if self.started is None:
            raise RuntimeError("Not started")
        runtime = stop_time - self.started
        self.max_time = max(self.max_time, runtime)
        self.tot_time += runtime
        self.rounds += 1
        self.started = None

    def stop_if_started(self, stop_time: float) -> None:
        """
        Stops the perf counter if it was started
        """
        if self.started is None:
            return
        self.stop(stop_time)


__pp__: Dict[str, _PP] = {}


def pp_start(name: str):
    """
    Start a perf counter named `name`
    """
    if name not in __pp__:
        __pp__[name] = _PP(name)
    # Start the perf counter as last as possible to avoid overhead
    __pp__[name].start()


def pp_stop(name: str, strict: bool = True):
    """
    Stop a perf counter named `name`
    """
    # Stop the perf counter as soon as possible to avoid overhead
    stop_time = time.perf_counter()
    if name not in __pp__:
        __pp__[name] = _PP(name)
    if strict:
        __pp__[name].stop(stop_time)
    else:
        __pp__[name].stop_if_started(stop_time)


def pp_stats():
    """ 
    Pretty print perf counters stats
    """

    def _truncate(string: str, max_length: int):
        """
        Truncate a string to `max_length` characters,
        adding "..." if the string is longer than `max_length`
        """
        if len(string) > max_length:
            return string[: max_length - 3] + "..."
        return string

    def _print_row(row: Union[List[str], List[str | int | float]], column_widths: List[int]):
        """
        Print a row of the table
        """
        formatted_row = [_truncate(str(item), w).ljust(w) for item, w in zip(row, column_widths)]
        print(" | ".join(formatted_row))

    # Determine the maximum width of each column
    headers: List[str] = ["PID", "Name", "tot_time", "rounds", "avg_time", "max_time"]
    rows: List[List[str | int | float]] = [
        [os.getpid(), pp.name, pp.tot_time, pp.rounds, pp.tot_time / pp.rounds, pp.max_time]
        for pp in sorted(__pp__.values(), key=lambda pp: pp.tot_time, reverse=True)
    ]

    # Ensure that all rows have the same number of columns
    assert all(len(headers) == len(r) for r in rows)

    # Determine the maximum width of each column
    max_col_width = 25
    column_widths = [
        min(max_col_width, max(len(str(r[i])) for r in chain([headers], rows)))
        for i in range(len(headers))
    ]

    # Print the table
    with open(os.path.expanduser("~/.omni_lock"), "w", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            _print_row(headers, column_widths)
            for pp in sorted(__pp__.values(), key=lambda pp: pp.tot_time, reverse=True):
                _print_row(
                    [
                        os.getpid(),
                        pp.name,
                        pp.tot_time,
                        pp.rounds,
                        pp.tot_time / pp.rounds,
                        pp.max_time,
                    ],
                    column_widths,
                )
            print()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
