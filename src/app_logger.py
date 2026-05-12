"""
Centralized application logger.
Import `log` from here instead of using print() directly.
"""
import logging
import logging.handlers
from pathlib import Path
from src.config_manager import config_manager


def _build_logger() -> logging.Logger:
    logger = logging.getLogger("SmartOST")
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler — INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File handler — rotating, DEBUG and above
    try:
        paths = config_manager.get_paths_config()
        log_dir = config_manager.get_full_path(paths.get("logs", "logs"))
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_file = Path(log_dir) / "smart_ost.log"

        fh = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except Exception as e:
        logger.warning(f"Could not create file handler: {e}")

    return logger


log = _build_logger()


def get_logger(name: str) -> logging.Logger:
    """Return a child logger namespaced under SmartOST."""
    return logging.getLogger(f"SmartOST.{name}")
