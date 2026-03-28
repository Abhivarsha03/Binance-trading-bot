import logging
import logging.handlers
import os
from datetime import datetime

LOG_DIR = "logs"


def setup_logging(log_level: str = "INFO", log_dir: str = LOG_DIR):
    os.makedirs(log_dir, exist_ok=True)

    # one log file per day — keeps things tidy
    today = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"trading_bot_{today}.log")

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # capture everything, handlers will filter

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # file handler — verbose (DEBUG and up)
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # console handler — only INFO and up so the terminal stays clean
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    ch.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))

    root.addHandler(fh)
    root.addHandler(ch)

    return log_file
