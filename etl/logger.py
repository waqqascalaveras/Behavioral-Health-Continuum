# etl/logger.py
import logging
import sys

def get_logger(name: str, log_file: str = 'etl.log', use_rich: bool = True) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')

    # File handler (always plain)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        logger.addHandler(fh)

    # Console handler (rich if available)
    if use_rich:
        try:
            from rich.logging import RichHandler
            rich_handler = RichHandler(rich_tracebacks=True, show_time=True, show_level=True, show_path=False)
            rich_handler.setLevel(logging.INFO)
            if not any(isinstance(h, RichHandler) for h in logger.handlers):
                logger.addHandler(rich_handler)
        except ImportError:
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
                logger.addHandler(ch)
    else:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            logger.addHandler(ch)

    logger.propagate = False
    return logger
