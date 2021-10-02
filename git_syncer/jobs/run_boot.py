import logging
from typing import List

from git_syncer.jobs.models import BootJob
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)

BOOT_JOBS: List[BootJob] = []


def run_boot():
    log.info("Running boot jobs.")
    for job in BOOT_JOBS:
        log.debug(f"Running job {wrap(job.name)}")
        try:
            job.run()
        except:
            log.exception("Job execution failed")


def add_boot_jobs(*jobs: BootJob):
    BOOT_JOBS.extend(jobs)
