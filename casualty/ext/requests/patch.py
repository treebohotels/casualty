import logging
import uuid

import structlog
import wrapt

from casualty import constants

logger = logging.getLogger()


def patch():
    wrapt.wrap_function_wrapper("requests", "Session.prepare_request", _inject_header)


def _inject_header(wrapped, instance, args, kwargs):
    """

    Add request_id header to all outgoing http request

    :param wrapped:
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    request = args[0]
    headers = getattr(request, "headers", {})
    inject_request_id_header(headers)
    setattr(request, "headers", headers)
    return wrapped(*args, **kwargs)


def inject_request_id_header(headers):
    try:
        headers[constants.REQUEST_HEADER] = str(
            structlog.get_config()["context_class"]._tl.dict_["request_id"]
        )
    except Exception as e:
        headers[constants.REQUEST_HEADER] = str(uuid.uuid4())
