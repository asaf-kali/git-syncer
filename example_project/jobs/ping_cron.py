import logging
from io import StringIO

from git_syncer.models import CronJob
from git_syncer.utils import execute_shell

log = logging.getLogger(__name__)


def _ping() -> str:
    stream = StringIO()
    execute_shell("ping 8.8.8.8 -c 5", output_redirect=stream)
    return f"{stream.getvalue()}"


class Ping(CronJob):
    @property
    def verbose_name(self) -> str:
        return "Ping"

    @property
    def expression(self) -> str:
        # Every 5 minutes
        return "*/5 * * * *"

    def run(self) -> str:
        return _ping()


if __name__ == "__main__":
    print(_ping())
