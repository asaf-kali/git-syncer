import logging
from typing import List

import pycron

from git_syncer.jobs.models import CronJob
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)

CRON_JOBS: List[CronJob] = []


def run_crons():
    for job in CRON_JOBS:
        if pycron.is_now(job.expression):
            log.debug(f"Running cron {wrap(job.name)}")
            try:
                job.run()
            except:
                log.exception("Job execution failed")


def add_cron_jobs(*jobs: CronJob):
    CRON_JOBS.extend(jobs)
