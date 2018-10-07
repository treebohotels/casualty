import logging
import uuid

import structlog
import wrapt

from casualty import constants

logger = logging.getLogger()


def patch():
    wrapt.wrap_function_wrapper("kombu", "messaging.Producer.publish", _inject_header)
    wrapt.wrap_function_wrapper(
        "kombu", "messaging.Consumer.__init__", _initialize_structlog_configuration
    )
    wrapt.wrap_function_wrapper(
        "kombu", "messaging.Consumer.receive", _bind_request_id_on_message_receive
    )


def _inject_header(wrapped, instance, args, kwargs):
    if "type" in args[0] and args[0]["type"] == "worker-heartbeat":
        return wrapped(*args, **kwargs)

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


def _initialize_structlog_configuration(wrapped, instance, args, kwargs):
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return wrapped(*args, **kwargs)


def _bind_request_id_on_message_receive(wrapped, instance, args, kwargs):
    logger = structlog.getLogger()
    try:
        request_id = args[1].headers[constants.REQUEST_HEADER]
    except Exception as e:
        request_id = str(uuid.uuid4())

    logger = logger.bind(request_id=request_id)
    return wrapped(*args, **kwargs)
