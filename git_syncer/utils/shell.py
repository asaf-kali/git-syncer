import logging
import subprocess
from io import StringIO
from typing import Iterable, Optional

from typing.io import IO

log = logging.getLogger(__name__)
execution_log = log.getChild("execution")
SEPARATOR = "------"


def str_to_bool(val: str) -> bool:
    clean_val = val.lower().strip()
    if clean_val in ("yes", "y", "true", "t", "1"):
        return True
    if clean_val in ("no", "n", "false", "f", "0"):
        return False
    raise ValueError(f"Could not parse boolean from '{val}'")


def yes_or_no(explanation: str) -> bool:
    while True:
        raw_answer = input(f"{explanation}. Are you sure you want to continue? (Y/n): ")
        try:
            answer = str_to_bool(raw_answer)
            return answer
        except ValueError:
            pass


def execute_shell(
    command: str,
    args: Iterable = None,
    print_command: bool = True,
    print_output: bool = True,
    output_redirect: Optional[StringIO] = None,
) -> int:
    full_command = command
    if args:
        full_command += " " + " ".join(args)
    if print_command:
        log.debug(f"Executing shell: '{full_command}'")
    process = subprocess.Popen(args=full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    _pass_output(origin=process.stdout, output_redirect=output_redirect, print_output=print_output)
    _pass_output(origin=process.stderr, output_redirect=output_redirect, print_output=print_output)
    exit_code = process.wait()
    if print_output:
        execution_log.info(f"{SEPARATOR}")  # End of command output{SEPARATOR}
        log.debug(f"Command exit code: {exit_code}")
    return exit_code


def _pass_output(origin: IO, output_redirect: Optional[StringIO], print_output: bool):
    if origin is None or (output_redirect is None and not print_output):
        return
    for line in origin.readlines():
        if isinstance(line, bytes):
            line_str = line.decode("utf-8")
        else:
            line_str = str(line)
        line_str = line_str[:-1]  # Trim \n TODO: think about this logic
        if print_output:
            execution_log.info(line_str)
        if output_redirect is not None:
            output_redirect.write(line_str)
            output_redirect.write("\n")
