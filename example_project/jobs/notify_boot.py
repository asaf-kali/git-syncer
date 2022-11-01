import logging
import os
from time import sleep

import requests

from git_syncer.models import Runnable

log = logging.getLogger(__name__)

MAX_RETRIES = 5
RETRY_DELAY = 5

# Note: This is just an example! Never keep secrets in the code, even if it's a private repository.
# If you want to use this, you can use local secrets file.
telegram_bot_token = "ABC123"
chat_id = "123456789"


def _notify_boot_on_telegram():
    log.info("Notifying successful boot")
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    device_name = os.uname().nodename
    data = {
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "text": f"Successfully booted *{device_name}*!",
    }

    def send_message():
        response = requests.post(url, data=data, timeout=5)
        response.raise_for_status()
        return response

    for _ in range(MAX_RETRIES):
        try:
            return send_message()
        except Exception as e:
            log.warning(f"Failed to notify boot: {e}")
            sleep(RETRY_DELAY)


class NotifyBoot(Runnable):
    @property
    def verbose_name(self) -> str:
        return "Notify boot"

    @property
    def run_on_boot(self) -> bool:
        return True

    def run(self) -> str:
        response = _notify_boot_on_telegram()
        return response.text
