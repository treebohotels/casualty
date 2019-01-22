import logging
import uuid
import structlog


class RequestIDFilter(logging.Filter):

    def filter(self, record):
        try:
            record.request_id = str(
                structlog.get_config()["context_class"]._tl.dict_["request_id"]
            )
        except :
            record.request_id=str(uuid.uuid4())

        return True
