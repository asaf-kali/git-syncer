import logging
from typing import List

import pycron

from git_syncer.models import CronJob
from git_syncer.runnables import get_cron_jobs
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)


def run_crons():
    jobs_to_run = _get_jobs_to_run()
    # First checking and then running because things might take longer then 1 minute.
    _run_jobs(jobs_to_run=jobs_to_run)


def _get_jobs_to_run() -> List[CronJob]:
    cron_jobs = get_cron_jobs()
    log.info(f"Checking {wrap(len(cron_jobs))} cron jobs.")
    jobs_to_run = []
    for job in cron_jobs:
        if pycron.is_now(job.expression):
            jobs_to_run.append(job)
            log.debug(f"Cron {wrap(job.verbose_name)} will run.")
    return jobs_to_run


def _run_jobs(jobs_to_run: List[CronJob]):
    log.debug(f"Total {wrap(len(jobs_to_run))} crons will run.")
    for job in jobs_to_run:
        try:
            log.debug(f"Running cron {wrap(job.verbose_name)}")
            job.run()
        except:  # noqa # pylint: disable=bare-except
            log.exception(f"Job {wrap(job.verbose_name)} execution failed")
