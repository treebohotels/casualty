import logging

import structlog
import wrapt

logger = logging.getLogger()


def patch():
    wrapt.wrap_function_wrapper(
        'kombu',
        'messaging.Producer.publish',
        _inject_header
    )


def _inject_header(wrapped, instance, args, kwargs):
    if 'headers' in kwargs:
        headers = kwargs['headers']
    else:
        headers = {}

    headers['X_CO_REQUEST_ID'] = str(structlog.get_config()['context_class']._tl.dict_['request_id'])
    kwargs['headers'] = headers
    return wrapped(*args, **kwargs)
