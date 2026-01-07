#!python3
import functools
import logging
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

import toml

logger = logging.getLogger(__name__)


checkpoints_file = Path("checkpoints.toml")
checkpoints_last_file = Path("checkpoints_last.toml")


def load_state():
    if checkpoints_file.exists():
        return toml.load(checkpoints_file)
    return {}


def save_state(state):
    checkpoints_file.write_text(toml.dumps(state))


def get_legible_timestamp():
    tz_env = os.getenv("TZ")
    if tz_env:
        # If TZ is set, use it
        import zoneinfo

        try:
            tz = zoneinfo.ZoneInfo(tz_env)
            return datetime.now(tz).isoformat()
        except Exception:
            logger.debug("Invalid TZ, falling back to UTC")
    return datetime.now(timezone.utc).isoformat()


def checkpoint(func=None):
    def decorator(inner_func):
        @functools.wraps(inner_func)
        def wrapper(*args, **kwargs):
            module = inner_func.__module__
            name = inner_func.__name__
            state = load_state()
            module_state = state.get(module, {})
            if module_state.get(name, False):
                logger.info(f"Skipping {module}.{name}, already done.")
                return 0
            result = inner_func(*args, **kwargs)
            if result == 0:
                module_state[name] = get_legible_timestamp()
                state[module] = module_state
                save_state(state)
            return result

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)


def cleanup():
    if checkpoints_file.exists():
        if checkpoints_last_file.exists():
            checkpoints_last_file.unlink()
        checkpoints_file.rename(checkpoints_last_file)
    else:
        logger.warning(f"No {checkpoints_file.name} to clean up!")
