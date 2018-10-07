import logging

import structlog


def getLogger(logger=None):
    if not logger:
        logger = logging.getLogger()

    if not structlog.is_configured():
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.processors.JSONRenderer(),
            ],
            context_class=structlog.threadlocal.wrap_dict(dict),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    logger = structlog.wrap_logger(logger=logger)
    return logger
