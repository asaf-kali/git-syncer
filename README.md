# Git syncer

Allows cron job control and command execution on a remote machine using git
infrastructure.

[![Tests](https://github.com/asaf-kali/git-syncer/actions/workflows/tests.yml/badge.svg)](https://github.com/asaf-kali/git-syncer/actions/workflows/tests.yml)
[![Lint](https://github.com/asaf-kali/git-syncer/actions/workflows/lint.yml/badge.svg)](https://github.com/asaf-kali/git-syncer/actions/workflows/lint.yml)
[![PyPI version](https://badge.fury.io/py/git-syncer.svg)](https://badge.fury.io/py/git-syncer)

👷🏻 *Please note, this project is still a work-in-progress* 🏗️

<h2 id="quick-start">
Quick start
</h2>

On your computer, set up the basic repository
(checkout the `example_project` in this repository to see how this should generally look):

1. [Create](https://github.com/new) a **private** GitHub repository and clone it.
2. Create a `requirements.txt` file, and add the `git-syncer` dependency.
3. Create a `main.py` file:

```python3
from git_syncer import run
from git_syncer.runnables import register

register()  # Add boot jobs, cron jobs, and remote commands here 🏋🏻‍♂️

if __name__ == "__main__":
    run()
```

4. Add a `.gitignore` file (tip: use [gitignore.io](https://www.toptal.com/developers/gitignore)).
   It must contain `out/` directory.
5. Commit and push your changes.

On your remote machine (SSH to it):

6. Set up GitHub credentials to clone your new repository.<br>
   **Highly recommended**: instead of providing your own personal GitHub credentials on the remote machine,
   [add an SSH deploy key to your repository](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys)
   . If you choose to do so, check the `Allow write access` checkbox.
7. Clone your new repository to the remote machine.
8. Set up a [virtual environment](https://docs.python.org/library/venv.html) for this project and activate it
   (using `source <venv_dir>/bin/activate`).
9. `cd` to your repository directory.
10. Install dependencies using `pip install -r requirements.txt` (`git-syncer` should be installed).
11. ⚠️ **THIS STEP WILL OVERRIDE YOUR EXISTING CRONTAB SETTINGS!** ⚠️<br>
    Activate the syncer using the CLI command `init-syncer`.

From now on, you can add new [cron jobs](#cron-jobs) and execute [remote commands](#remote-commands) on the
remote machine using this git repository. For more details, see the [usage section](#usage).

<h2 id="usage">
Usage
</h2>

Note: this tool writes logs to `~/logs/git-syncer/`.

<h4 id="runnables">
Runnables
</h4>

A `Runnable` is the basic class that the package uses.
To define your own custom commands, create your own class, inherit `Runnable`,
and implement the mandatory abstract methods:
```python3
# File: my_runnables.py
from git_syncer.models import Runnable


class HelloWorld(Runnable):
    @property
    def verbose_name(self) -> str:
        return "Hello World"

    def run(self) -> str:
        return "This runnable was called!"
```
...and register your runnable in `main.py`:
```python3
# File: main.py
from git_syncer.runnables import register

from my_runnables import HelloWorld

register(HelloWorld())
```

<h3 id="boot-jobs">
Boot jobs
</h3>

Boot jobs will execute once the remote machine turns on.
In order to make a `Runnable` into a boot job, set the `run_on_boot` property to `True`:
```python3
class HelloWorld(Runnable):
    @property
    def run_on_boot(self) -> bool:
        return True
    ...
```

<h3 id="cron-jobs">
Cron jobs
</h3>

To create a cron job, inherit the `CronJob` class, and fill the `expression` property:
```python3
from git_syncer.models import CronJob

class MyCronJob(CronJob):
    @property
    def verbose_name(self) -> str:
        return "Ping"

    @property
    def expression(self) -> str:
        # Every 5 minutes
        return "*/5 * * * *"

    def run(self) -> str:
        return "This job runs every 5 minutes"
```

<h3 id="remote-commands">
Execute jobs on command
</h3>

In order to make a non-cron runnable execute on the remote machine:

1. On your local machine, commit an empty file matching your `Runnable` name under `execute` folder (for example,
   if the runnable class name is `GetIP`, commit a file named `execute/get-ip`).
2. Push your changes.
3. On the next round minute:
   1. The runnable will execute on the remote device,
   2. The execution result will be written in a file matching your runnable name (for example, if the runnable
      class name is `GetIP`, the result file will be named `execute/get-ip-result.txt`, and the `execute/get-ip`
      file will be removed).
   3. The changes will be committed and pushed back to the repository.
4. Wait a few seconds and pull your repository. You will see the execution result in the expected result file.

Expert mode: every minute, in order the check if a non-cron `Runnable` should be executed, its `should_execute` method
is called (matching file names to the runnable class name). In order to execute your runnable based on different logic,
override the `should_execute` method:
```python3
from typing import Set
from git_syncer.models import Runnable
import random

class HelloWorld(Runnable):
    @property
    def verbose_name(self) -> str:
        return "Hello World"

    def run(self) -> str:
        return "This runnable was called!"

     def should_execute(self, inputs: Set[str]) -> bool:
        # Take a look at the base method and implement your own logic.
        return random.randint(1, 100) % 5 == 0
```

<h3 id="error-handling">
Error handling
</h3>

👷🏻 TODO
