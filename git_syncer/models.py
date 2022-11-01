import re
from abc import ABC
from dataclasses import dataclass
from typing import Set


class Runnable(ABC):
    @property
    def verbose_name(self) -> str:
        raise NotImplementedError()

    @property
    def command_file_name(self) -> str:
        return _camel_to_dash_case(self.__class__.__name__)

    @property
    def run_on_boot(self) -> bool:
        return False

    def should_execute(self, inputs: Set[str]) -> bool:
        for i in inputs:
            if self.command_file_name in i and "result" not in i:
                return True
        return False

    def run(self) -> str:
        raise NotImplementedError


@dataclass
class CronJob(Runnable, ABC):
    @property
    def expression(self) -> str:
        raise NotImplementedError()


def _camel_to_dash_case(camel_input):
    words = re.findall(r"[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+", camel_input)
    return "-".join(map(str.lower, words))
