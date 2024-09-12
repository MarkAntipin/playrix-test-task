import json
import logging
import sys
import traceback


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
            'filename': record.filename,
            'funcName': record.funcName,
            'lineno': record.lineno,
        }

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
            log_record['traceback'] = ''.join(traceback.format_exception(*record.exc_info))

        return json.dumps(log_record)


def setup_logger(level: int = logging.INFO) -> None:
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = JsonFormatter()

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
