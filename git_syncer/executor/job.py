import logging
import os
from typing import List, Set

from . import Command
from ..jobs import BootJob, CronJob
from ..utils import execute_shell
from ..utils.logger import wrap

log = logging.getLogger(__name__)

EXECUTE_DIR = "execute"
COMMANDS: List[Command] = []


def add_commands(*commands: Command):
    COMMANDS.extend(commands)


class ExecutorJob(BootJob, CronJob):
    def __init__(self, base_dir: str):
        super().__init__()
        self.base_dir = base_dir
        self.succeeded_count = 0
        self.failed_count = 0

    @property
    def verbose_name(self) -> str:
        return "Detect commands and execute"

    @property
    def expression(self) -> str:
        return "* * * * *"  # Every minute

    @property
    def commands_dir(self) -> str:
        return os.path.join(self.base_dir, EXECUTE_DIR)

    @property
    def has_executed(self) -> bool:
        return self.succeeded_count > 0 or self.failed_count > 0

    def run(self):
        log.info("Executor running...")
        inputs = self._get_inputs()
        if not inputs:
            log.debug("No inputs found.")
            return
        self._run_commands(inputs=inputs)
        if not self.has_executed:
            log.info("No commands executed.")
            return
        execute_shell("git add .")
        execute_shell('git commit -m "Execution result"')
        execute_shell("git push")

    def _get_inputs(self) -> Set[str]:
        if not os.path.exists(self.commands_dir):
            log.debug("No commands directory, returning")
            return set()
        inputs = set(os.listdir(self.commands_dir))
        log.debug(f"Existing files: {inputs}")
        return inputs

    def _run_commands(self, inputs: Set[str]):
        log.debug(f"Checking {wrap(len(COMMANDS))} commands.")
        for command in COMMANDS:
            if command.should_execute(inputs=inputs):
                if self._run_command(command):
                    self.succeeded_count += 1
                else:
                    self.failed_count += 1

    def _run_command(self, command: Command) -> bool:
        log.debug(f"Running command {wrap(command.verbose_name)}.")
        original_command_file_name = os.path.join(self.commands_dir, command.formal_name)
        result_file_name = original_command_file_name + "-result.txt"
        succeeded = True
        try:
            result = command.execute()
        except Exception as e:
            succeeded = False
            log.exception("Command execution failed")
            result = str(e)
        with open(result_file_name, "w") as result_file:
            log.info(f"Writing result: {result}")
            result_file.write(result)
        os.remove(original_command_file_name)
        return succeeded
