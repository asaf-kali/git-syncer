from abc import ABC
from dataclasses import dataclass


class Job:
    @property
    def verbose_name(self) -> str:
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()


class BootJob(Job, ABC):
    pass


@dataclass
class CronJob(Job, ABC):
    @property
    def expression(self) -> str:
        raise NotImplementedError()
