from typing import Set


class Command:
    @property
    def verbose_name(self) -> str:
        raise NotImplementedError()

    @property
    def formal_name(self) -> str:
        raise NotImplementedError()

    def should_execute(self, inputs: Set[str]) -> bool:
        for i in inputs:
            if self.formal_name in i and "result" not in i:
                return True
        return False

    def execute(self) -> str:
        raise NotImplementedError()
