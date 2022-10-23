import logging
from typing import List

from git_syncer.models import Runnable
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)

BOOT_JOBS: List[Runnable] = []


def run_boot():
    log.info(f"Running {wrap(len(BOOT_JOBS))} boot jobs.")
    for job in BOOT_JOBS:
        log.debug(f"Running job {wrap(job.verbose_name)}")
        try:
            job.run()
        except:  # noqa
            log.exception("Job execution failed")


def add_boot_jobs(*jobs: Runnable):
    BOOT_JOBS.extend(jobs)
