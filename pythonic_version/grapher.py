from typing import List
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class _SingleRun:
    lambda_: float
    k: int
    error_rate: float


class Grapher:
    def __init__(self) -> None:
        self.runs: List[_SingleRun] = []

    def add(self, lambda_: float, k: int, error_rate: float):
        self.runs.append(
            _SingleRun(
                lambda_=lambda_,
                k=k,
                error_rate=error_rate,
            )
        )

    def plot_set_buffer_size(self, k: int):
        x: List[int] = []
        y: List[float] = []

        for run in self.runs:
            if run.k == k:
                x.append(run.lambda_)
                y.append(run.error_rate)

        if not x:
            raise ValueError(f"No runs with k = {k}")

        _, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()

    def plot_set_arrival_rate(self, lambda_: float):
        x: List[int] = []
        y: List[float] = []

        for run in self.runs:
            if run.lambda_ == lambda_:
                x.append(run.k)
                y.append(run.error_rate)

        if not x:
            raise ValueError(f"No runs with lambda = {lambda_}")

        _, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()
