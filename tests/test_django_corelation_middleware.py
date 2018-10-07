import structlog
from mock import Mock

from casualty.constants import HTTP_REQUEST_HEADER
from casualty.django_corelation_middleware import DjangoCorelationMiddleware


def mocked_fucntion():
    return True;


def test_flask_corelation_middleware():
    request = Mock()
    request.headers = {}
    request.META = {
        HTTP_REQUEST_HEADER: "12345",
        "HTTP_PROFILE_ID": "123",
        "REQUEST_METHOD": "POST",
        "HTTP_OPERATING_SYSTEM_VERSION": "ICE CREAM",
        "HTTP_PLATFORM": "ANDROID",
        "HTTP_APP_VERSION": "1.0.0",
        "HTTP_USER_AGENT": "AUTOMATED TEST"
    }
    request.path = '/testURL/'
    request.session = {}
    mocked_self_resposne = Mock()
    mocked_self_resposne.__call__ = mocked_fucntion.__call__
    django_middleware = DjangoCorelationMiddleware(mocked_self_resposne)
    django_middleware(request)

    request_id = structlog.get_config()["context_class"]._tl.dict_["request_id"]
    assert request_id == '12345'
