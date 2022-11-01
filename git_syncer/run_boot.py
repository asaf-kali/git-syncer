import logging

from git_syncer.runnables import get_boot_jobs
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)


def run_boot():
    boot_jobs = get_boot_jobs()
    log.info(f"Running {wrap(len(boot_jobs))} boot jobs.")
    for job in boot_jobs:
        log.debug(f"Running job {wrap(job.verbose_name)}")
        try:
            job.run()
        except:  # noqa pylint: disable=bare-except
            log.exception("Job execution failed")
