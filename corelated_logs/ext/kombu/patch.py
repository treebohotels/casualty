import logging

import structlog
import wrapt
import uuid

from corelated_logs import constants

logger = logging.getLogger()


def patch():
    wrapt.wrap_function_wrapper("kombu", "messaging.Producer.publish", _inject_header)


def _inject_header(wrapped, instance, args, kwargs):
    if "headers" in kwargs:
        headers = kwargs["headers"]
    else:
        headers = {}

    try:
        headers[constants.REQUEST_HEADER] = str(
            structlog.get_config()["context_class"]._tl.dict_["request_id"]
        )
    except Exception as e:
        headers[constants.REQUEST_HEADER] = str(uuid.uuid4())
    kwargs["headers"] = headers
    return wrapped(*args, **kwargs)
