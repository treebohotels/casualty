import logging

import structlog
import wrapt
import uuid

logger = logging.getLogger()


def patch():
    wrapt.wrap_function_wrapper("kombu", "messaging.Producer.publish", _inject_header)


def _inject_header(wrapped, instance, args, kwargs):
    if "headers" in kwargs:
        headers = kwargs["headers"]
    else:
        headers = {}

    try:
        headers["X_CO_REQUEST_ID"] = str(
            structlog.get_config()["context_class"]._tl.dict_["request_id"]
        )
    except Exception as e:
        headers["X_CO_REQUEST_ID"] = str(uuid.uuid4())
    kwargs["headers"] = headers
    return wrapped(*args, **kwargs)
