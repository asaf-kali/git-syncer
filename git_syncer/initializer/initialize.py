import logging
import os

from jinja2 import Environment, FileSystemLoader

from git_syncer.utils import execute_shell
from git_syncer.utils.logger import wrap

log = logging.getLogger(__name__)


def initialize_syncer():
    # Get directories
    env_dir = os.getenv("VIRTUAL_ENV")
    working_dir = os.getcwd()
    home_dir = os.path.expanduser("~")
    log.info(f"Environment directory: {wrap(env_dir)}")
    log.info(f"Project working directory: {wrap(working_dir)}")
    log.info(f"User home directory: {wrap(home_dir)}")
    if env_dir is None:
        raise RuntimeError("init-syncer must be run only after venv is activated!")
    # Logs
    logs_dir = os.path.join(home_dir, "logs", "git-syncer")
    execute_shell(f"mkdir {logs_dir} -p")
    # Templates
    out_dir = os.path.join(working_dir, "out")
    context = {"working_dir": working_dir, "env_dir": env_dir, "logs_dir": logs_dir, "out_dir": out_dir}
    _render_templates(context, out_dir)


def _render_templates(context: dict, out_dir: str):
    execute_shell(f"mkdir {out_dir} -p")
    templates_dir = _get_templates_path()
    env = Environment(loader=FileSystemLoader(templates_dir), keep_trailing_newline=True)
    _render_crontab(context=context, env=env, out_dir=out_dir)
    _render_runner(context=context, env=env, out_dir=out_dir)


def _get_templates_path() -> str:
    init_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(init_dir, "templates")
    return templates_dir


def _render_runner(context: dict, env: Environment, out_dir: str):
    runner_out_file = os.path.join(out_dir, "runner.sh")
    env.get_template("runner.txt").stream(**context).dump(runner_out_file)
    execute_shell(f"chmod +x {runner_out_file}")


def _render_crontab(context: dict, env: Environment, out_dir: str):
    crontab_out_file = os.path.join(out_dir, "crontab.txt")
    env.get_template("crontab.txt").stream(**context).dump(crontab_out_file)
    execute_shell(f"crontab {crontab_out_file}")
