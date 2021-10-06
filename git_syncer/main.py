import logging
import os
from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import List

from .executor.job import ExecutorJob
from .jobs.run_boot import run_boot, add_boot_jobs
from .jobs.run_crons import run_crons, add_cron_jobs
from .utils import execute_shell

log = logging.getLogger(__name__)


class Mode(Enum):
    BOOT = "boot"
    CRONS = "crons"

    @classmethod
    def value_list(cls) -> List[str]:
        return [c.value for c in cls]


def run():
    log.debug("Git syncer start.")
    args = _parse_args()
    _run(mode=args.mode, sync=args.sync)
    log.debug("Git syncer done.")


def _run(mode: Mode, sync: bool):
    if sync:
        log.debug("Sync is on, pulling from git.")
        _run_sync()
        log.debug("Running same mode with --no-sync flag.")
        execute_shell(f"out/runner.sh {mode.value} --no-sync")
        return
    _add_execute_job()
    if mode == Mode.BOOT:
        run_boot()
    elif mode == Mode.CRONS:
        run_crons()
    else:
        raise NotImplementedError(f"Unexpected mode {mode}")


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("mode_name", choices=Mode.value_list())
    parser.add_argument("--no-sync", default=False, action="store_true")
    args = parser.parse_args()
    args.mode = Mode[args.mode_name.upper()]
    args.sync = not args.no_sync
    log.debug(f"Args: {args}")
    return args


def _run_sync():
    log.info("Sync running...")
    execute_shell("git fetch")
    execute_shell("git stash")
    execute_shell("git checkout main")
    execute_shell("git reset --hard origin/main")
    execute_shell("pip install -r requirements.txt")
    execute_shell("init-syncer --no-input")


def _add_execute_job():
    cwd = os.getcwd()
    execute_job = ExecutorJob(cwd)
    add_boot_jobs(execute_job)
    add_cron_jobs(execute_job)
