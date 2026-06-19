"""
LinguaGraph — Logging Configuration

Zero-config logging setup. Call setup_logging() once at app entry point.
All modules use `import logging; logger = logging.getLogger(__name__)`.
"""
import logging
import sys
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: str | None = None,
    simple_format: bool = False,
) -> None:
    """
    Configure project-wide logging.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional path to log file. If None, logs to stderr only.
        simple_format: If True, omit timestamps (cleaner for CLI tools).
    """
    if simple_format:
        fmt = "%(levelname)-7s %(name)s: %(message)s"
    else:
        fmt = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"

    handlers = [logging.StreamHandler(sys.stderr)]

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(str(log_path), encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format=fmt,
        handlers=handlers,
        force=True,
    )

    # Quiet noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
