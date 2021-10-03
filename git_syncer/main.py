import logging
import os
from argparse import ArgumentParser, Namespace

from git_syncer.jobs.run_boot import run_boot
from git_syncer.jobs.run_crons import run_crons, CRON_JOBS
from git_syncer.sync.job import SyncJob

log = logging.getLogger(__name__)


def run():
    log.debug("git-syncer start.")
    args = _parse_args()
    _add_sync_job()
    _run(is_boot=args.boot)
    log.debug("git-syncer done.")


def _add_sync_job():
    cwd = os.getcwd()
    sync_job = SyncJob(cwd)
    CRON_JOBS.insert(0, sync_job)


def _run(is_boot: bool):
    if is_boot:
        run_boot()
    else:
        run_crons()


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--boot", default=False, action="store_true")
    args = parser.parse_args()
    log.debug(f"Args: {args}")
    return args


if __name__ == "__main__":
    run()
