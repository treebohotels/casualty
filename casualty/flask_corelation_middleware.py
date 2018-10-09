import uuid

import structlog

from casualty.casualty_logger import configure_structlog
from casualty.constants import HTTP_REQUEST_HEADER


class FlaskCorelationMiddleWare(object):
    """
    If request_id header is present bind it to logger
    else create an ew request_id and bind it to logger
    It uses structlog to maintain request_id
    """

    def __init__(self, app):
        self.app = app
        if not structlog.is_configured():
            configure_structlog()

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
