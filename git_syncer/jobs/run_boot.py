import logging
from typing import List

from .models import BootJob
from ..utils.logger import wrap

log = logging.getLogger(__name__)

BOOT_JOBS: List[BootJob] = []


def run_boot():
    log.info(f"Running {wrap(len(BOOT_JOBS))} boot jobs.")
    for job in BOOT_JOBS:
        log.debug(f"Running job {wrap(job.verbose_name)}")
        try:
            job.run()
        except:  # noqa
            log.exception("Job execution failed")


def add_boot_jobs(*jobs: BootJob):
    BOOT_JOBS.extend(jobs)
