#!/usr/bin/env python
"""
Rollsmart Logger
"""
import logging
from rich.logging import RichHandler

def init_logger():
    """
    Initialize logger
    """
    logging_format = "%(message)s"
    logging.basicConfig(
        level=logging.INFO, format=logging_format, datefmt="[%X]",
        handlers=[RichHandler(markup=True)]
    )
    logger = logging.getLogger('Rollsmart')
    return logger
