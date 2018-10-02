import uuid

import structlog

from corelated_logs.constants import HTTP_REQUEST_HEADER


class FlaskCorelationMiddleWare(object):
    """
    If request_id header is present bind it to logger
    else create an ew request_id and bind it to logger
    It uses structlog to maintain request_id
    """

    def __init__(self, app):
        self.app = app
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.processors.JSONRenderer(),
            ],
            context_class=structlog.threadlocal.wrap_dict(dict),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def __call__(self, environ, start_response):

        """
        :param environ:
        :param start_response:
        :return:
        """

        logger = structlog.getLogger()
        if HTTP_REQUEST_HEADER in environ:
            current_request_id = environ[HTTP_REQUEST_HEADER]

        else:
            current_request_id = str(uuid.uuid4())
        logger = logger.bind(request_id=current_request_id)
        return self.app(environ, start_response)
