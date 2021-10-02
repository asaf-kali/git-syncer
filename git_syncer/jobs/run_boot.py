import logging
from typing import List

from git_syncer.jobs.models import BootJob
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)

BOOT_JOBS: List[BootJob] = []


def run_boot():
    for job in BOOT_JOBS:
        log.debug(f"Running job {wrap(job.name)}")
        job.run()


def add_boot_jobs(*jobs: BootJob):
    BOOT_JOBS.extend(jobs)
