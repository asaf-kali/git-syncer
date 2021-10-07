# Git syncer

Allows cron job control and command execution on a remote machine using git infrastructure.

[![Tests](https://github.com/asaf-kali/git-syncer/actions/workflows/tests.yml/badge.svg)](https://github.com/asaf-kali/git-syncer/actions/workflows/tests.yml)
[![Lint](https://github.com/asaf-kali/git-syncer/actions/workflows/lint.yml/badge.svg)](https://github.com/asaf-kali/git-syncer/actions/workflows/lint.yml)

👷🏻 *Please note, this project is still a work-in-progress* 🏗️

<h2 id="quick-start">
Quick start
</h2>

On your computer, set up the basic repository:

1. [Create](https://github.com/new) a private GitHub repository and clone it.
2. Create a `requirements.txt` file, and add the `git-syncer` dependency.
3. Create a `main.py` file:

```python3
from git_syncer import run
from git_syncer.jobs import add_cron_jobs, add_boot_jobs
from git_syncer.executor import add_commands

add_boot_jobs()  # Add boot jobs here ⛷️ 
add_cron_jobs()  # Add cron jobs here 🚵🏻‍♀️
add_commands()  # Add remote commands here 🏋🏻‍♂️

if __name__ == "__main__":
    run()
```

4. Add a `.gitignore` file (tip: use [gitignore.io](https://www.toptal.com/developers/gitignore)). It must
   contain `out/`.
5. Commit and push your changes.

On your remote machine (SSH to it):

6. Set up GitHub credentials to clone your new repository.<br>
   **Highly recommended**: instead of providing your own personal GitHub credentials on the remote machine,
   [add an SSH deploy key to your repository](https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys)
   . If you choose to do so, check the `Allow write access` checkbox.
7. Clone your new repository to the remote machine.
8. Set up [virtual environment](https://docs.python.org/library/venv.html) for this project and activate it (
   using `source <venv_dir>/bin/activate`).
9. `cd` to your repository directory.
10. Install dependencies using `pip install -r requirements.txt` (`git-syncer` should be installed).
11. ⚠️ **THIS STEP WILL OVERRIDE YOUR EXISTING CRONTAB SETTINGS!** ⚠️<br>
    Activate the syncer using the CLI command `init-syncer`.

From now on, you can add new [cron jobs](#cron-jobs) and run [remote commands](#remote-commands) on the machine using
this git repository. For more details, see the [usage section](#usage).

<h2 id="usage">
Usage
</h2>

This tool writes logs to `~/logs/git-syncer/`.

<h4 id="remote-commands">
Remote commands
</h4>

👷🏻 TODO

<h4 id="boot-jobs">
Boot jobs
</h4>

👷🏻 TODO

<h4 id="cron-jobs">
Cron jobs
</h4>

👷🏻 TODO
