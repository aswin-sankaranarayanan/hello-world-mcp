"""Logging configuration utilities."""

import os
import logging


def setup_logging() -> logging.Logger:
    """Configure logging with environment variable support.""" 
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logger initialized with level: {log_level}")
    
    return logger