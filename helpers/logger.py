import logging


class CustomLogging:
    @classmethod
    def error(cls, message, extra=None):
        logging.basicConfig(level=logging.DEBUG)

        logging.error(message, extra=extra)
