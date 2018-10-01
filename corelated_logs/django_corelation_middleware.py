import structlog


class DjangoCorelationMiddleware(object):
    CORELATED_HEADER = 'HTTP_X_CO_REQUEST_ID'

    def __init__(self, app):
        self.app = app
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt='ISO'),
                structlog.processors.JSONRenderer()
            ],
            context_class=structlog.threadlocal.wrap_dict(dict),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True
        )

    def process_request(self, request):

        logger = structlog.getLogger()
        if request.headers.get(self.CORELATED_HEADER):
            current_request_id = request.headers.get(self.CORELATED_HEADER)

        else:
            current_request_id = str(uuid.uuid4())
        logger = logger.bind(request_id=current_request_id)
