from typing import List

from git_syncer.models import CronJob, Runnable

_RUNNABLES: List[Runnable] = []


def register(*runnables: Runnable):
    _RUNNABLES.extend(runnables)


def get_all_jobs() -> List[Runnable]:
    return _RUNNABLES


def get_boot_jobs() -> List[Runnable]:
    return [job for job in _RUNNABLES if job.run_on_boot]


def get_cron_jobs() -> List[CronJob]:
    return [job for job in _RUNNABLES if isinstance(job, CronJob)]
