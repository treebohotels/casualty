import logging

import structlog


class RequestIDFilter(logging.Filter):

    def filter(self, record):
        record.request_id = str(
            structlog.get_config()["context_class"]._tl.dict_["request_id"]
        )
        return True
