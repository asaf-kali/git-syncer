import logging
from typing import List

import pycron

from .models import CronJob
from ..utils.logger import wrap

log = logging.getLogger(__name__)

CRON_JOBS: List[CronJob] = []


def run_crons():
    jobs_to_run = _get_jobs_to_run()
    # First checking and then running because things might take longer then 1 minute.
    _run_jobs(jobs_to_run=jobs_to_run)


def _get_jobs_to_run() -> List[CronJob]:
    log.info(f"Checking {wrap(len(CRON_JOBS))} cron jobs.")
    jobs_to_run = []
    for job in CRON_JOBS:
        if pycron.is_now(job.expression):
            jobs_to_run.append(job)
            log.debug(f"Cron {wrap(job.verbose_name)} will run.")
    return jobs_to_run


def _run_jobs(jobs_to_run: List[CronJob]):
    log.debug(f"Total {wrap(len(jobs_to_run))} crons will run.")
    # TODO: Maybe run async in parallel?
    for job in jobs_to_run:
        try:
            log.debug(f"Running cron {wrap(job.verbose_name)}")
            job.run()
        except:  # noqa
            log.exception(f"Job {wrap(job.verbose_name)} execution failed")


def add_cron_jobs(*jobs: CronJob):
    CRON_JOBS.extend(jobs)
