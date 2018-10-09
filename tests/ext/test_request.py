from mock import Mock

from casualty.constants import REQUEST_HEADER
from casualty.ext.requests.patch import _inject_header


def mocked_function():
    return True


def test_inject_header(mocker):
    wrapped = Mock()
    instance = Mock()
    wrapped.__call__ = mocked_function.__call__
    request = Mock()
    request.headers = {}
    args = [request]
    mocker.patch("uuid.uuid4", return_value="12345")
    _inject_header(wrapped, instance, args, {})
    assert request.headers[REQUEST_HEADER] == '12345'

    print(123)
