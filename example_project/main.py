from jobs.get_ip import GetIP
from jobs.notify_boot import NotifyBoot
from jobs.ping_cron import Ping

from git_syncer import run
from git_syncer.runnables import register

register(GetIP(), NotifyBoot(), Ping())

if __name__ == "__main__":
    run()
