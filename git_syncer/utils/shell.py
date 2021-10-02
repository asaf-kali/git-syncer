import logging
import subprocess
from typing import Iterable

log = logging.getLogger(__name__)
execution_log = log.getChild("execution")
SEPARATOR = "------"


def execute_shell(
    command: str,
    args: Iterable = None,
    print_command: bool = True,
    print_output: bool = True,
) -> int:
    full_command = command
    if args:
        full_command += " " + " ".join(args)
    if print_command:
        log.debug(f"Executing shell: '{full_command}'")
    p = subprocess.Popen(args=full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if print_output:
        for line in p.stdout.readlines():
            if isinstance(line, bytes):
                line_str = line.decode("utf-8")
            else:
                line_str = str(line)
            line_str = line_str[:-1]  # Trim \n, TODO: think about this logic
            execution_log.info(line_str)
    output = p.wait()
    if print_output:
        execution_log.info(f"{SEPARATOR}")  # End of command output{SEPARATOR}
        log.debug(f"Command exit code: {output}")
    return output
