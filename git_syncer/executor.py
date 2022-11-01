import logging
import os
from typing import Set

from git_syncer.models import CronJob, Runnable
from git_syncer.runnables import get_all_jobs
from git_syncer.utils import execute_shell
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)

EXECUTE_DIR = "execute"


class ExecutorJob(CronJob):
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
        no_results = {i for i in inputs if "result" not in i}
        log.debug(f"Existing files: {inputs}, no results: {no_results}")
        return no_results

    def _run_commands(self, inputs: Set[str]):
        all_jobs = get_all_jobs()
        log.debug(f"Checking {wrap(len(all_jobs))} commands.")
        for command in all_jobs:
            if command.should_execute(inputs=inputs):
                if self._run_command(command):
                    self.succeeded_count += 1
                else:
                    self.failed_count += 1

    def _run_command(self, command: Runnable) -> bool:
        log.debug(f"Running command {wrap(command.verbose_name)}.")
        original_command_file_name = os.path.join(self.commands_dir, command.command_file_name)
        result_file_name = original_command_file_name + "-result.txt"
        succeeded = True
        try:
            result = command.run()
        except Exception as e:  # pylint: disable=broad-except,invalid-name
            succeeded = False
            log.exception("Command execution failed")
            result = str(e)
        with open(result_file_name, "w") as result_file:  # pylint: disable=unspecified-encoding
            log.info(f"Writing result: {result}")
            result_file.write(result)
        os.remove(original_command_file_name)
        return succeeded
