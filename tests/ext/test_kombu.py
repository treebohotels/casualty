from unittest import mock

import structlog
from mock import Mock

from casualty.constants import REQUEST_HEADER
from casualty.ext.kombu.patch import _inject_header, _bind_request_id_on_message_receive, \
    _initialize_structlog_configuration


def mocked_function():
    return True


@mock.patch("uuid.uuid4")
def test_inject_header(mock_uuid4):
    wrapped = Mock()
    instance = Mock()
    wrapped.__call__ = mocked_function.__call__
    args0 = {}
    kwargs = {}
    args = [args0]
    mock_uuid4.return_value = "12345"
    _inject_header(wrapped, instance, args, kwargs)

    assert kwargs['headers'][REQUEST_HEADER] == '12345'

@mock.patch("uuid.uuid4")

def test_bind_request_id_on_message_receive(mock_uuid4):
    wrapped = Mock()
    instance = Mock()
    wrapped.__call__ = mocked_function.__call__
    args0 = {}
    kwargs = {}
    args = [args0]
    mock_uuid4.return_value = "12345"

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    _bind_request_id_on_message_receive(wrapped, instance, args, kwargs)

    request_id = structlog.get_config()["context_class"]._tl.dict_["request_id"]
    assert request_id == '12345'
