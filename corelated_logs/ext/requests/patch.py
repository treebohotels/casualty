import logging

import structlog
import wrapt

logger = logging.getLogger()


def patch():
    wrapt.wrap_function_wrapper(
        'requests',
        'Session.prepare_request',
        _inject_header
    )


def _inject_header(wrapped, instance, args, kwargs):
    request = args[0]
    headers = getattr(request, 'headers', {})
    inject_request_id_header(headers)
    setattr(request, 'headers', headers)
    return wrapped(*args, **kwargs)


def inject_request_id_header(headers):
    headers['X_CO_REQUEST_ID'] = str(structlog.get_config()['context_class']._tl.dict_['request_id'])
