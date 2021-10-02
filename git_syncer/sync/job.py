import logging
import os
from typing import Set, List

from git_syncer.jobs import CronJob
from git_syncer.sync.command import Command
from git_syncer.utils import execute_shell
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)

COMMANDS: List[Command] = []


def add_commands(*commands: Command):
    COMMANDS.extend(commands)


# def _format_file_name(name: str) -> str:
#     return name.lower().replace("_", "").replace("-", "").strip()
#  def _cd_to_current_dir():
#     current_file_path = os.path.abspath(__file__)
#     current_dir_path = os.path.dirname(current_file_path)
#     os.chdir(current_dir_path)


class SyncJob(CronJob):
    def __init__(self, base_dir: str):
        super().__init__()
        self.base_dir = base_dir

    @property
    def name(self) -> str:
        return "Sync"

    @property
    def expression(self) -> str:
        return "* * * * *"  # Every minute

    @property
    def commands_dir(self) -> str:
        return f"{self.base_dir}/commands"

    def run(self):
        log.info("Sync running...")
        # _cd_to_current_dir()
        execute_shell("git fetch")
        execute_shell("git stash")
        execute_shell("git checkout main")
        execute_shell("git reset --hard origin/main")
        # execute_shell("crontab crontab.txt")
        execute_shell("pip install -r requirements.txt")
        inputs = self._get_inputs()
        if not inputs:
            return
        executed = self._run_commands(inputs=inputs)
        if not executed:
            log.info("No commands executed.")
            return
        execute_shell("git add .")
        execute_shell('git commit -m "Execution result"')
        execute_shell("git push")

    def _get_inputs(self) -> Set[str]:
        if not os.path.exists(self.commands_dir):
            log.warning("No commands directory, returning")
            return set()
        inputs = set(os.listdir(self.commands_dir))
        log.debug(f"Existing files: {inputs}")
        return inputs

    def _run_commands(self, inputs: Set[str]) -> bool:
        executed = False
        for command in COMMANDS:
            if command.should_execute(inputs=inputs):
                executed = True
                self._run_command(command)
        return executed

    def _run_command(self, command: Command):
        log.debug(f"Running command {wrap(command.verbose_name)}.")
        original_command_file_name = os.path.join(self.commands_dir, command.formal_name)
        result_file_name = original_command_file_name + "-result.txt"
        result = command.execute()
        with open(result_file_name, "w") as result_file:
            log.info(f"Writing result: {result}")
            result_file.write(result)
        os.remove(original_command_file_name)
