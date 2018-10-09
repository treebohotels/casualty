import logging

import structlog


def getLogger(logger=None):
    if not logger:
        logger = logging.getLogger()

    if not structlog.is_configured():
        configure_structlog()

    logger = structlog.wrap_logger(logger=logger)
    return logger


def configure_structlog():
    """
    default configuration for structlog if not specified during initialization
    :return:
    """
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
