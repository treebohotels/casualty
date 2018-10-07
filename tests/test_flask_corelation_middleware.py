import structlog
from mock import Mock

from casualty.constants import HTTP_REQUEST_HEADER
from casualty.flask_corelation_middleware import FlaskCorelationMiddleWare


def mocked_fucntion():
    return True;


def test_flask_corelation_middleware():
    envoirn = {}
    envoirn[HTTP_REQUEST_HEADER] = '12345'
    start_reposne = Mock()
    mocked_app = Mock()
    mocked_app.__call__ = mocked_fucntion.__call__
    flask_middleware = FlaskCorelationMiddleWare(mocked_app)
    flask_middleware(envoirn, start_reposne)
    request_id = structlog.get_config()["context_class"]._tl.dict_["request_id"]
    assert request_id == '12345'
