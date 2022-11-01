from git_syncer import run
from git_syncer.runnables import register

from .jobs.get_ip import GetIP
from .jobs.notify_boot import NotifyBoot
from .jobs.ping_cron import Ping

register(GetIP(), NotifyBoot(), Ping())

if __name__ == "__main__":
    run()
