# app_logger.py
import logging
from datetime import datetime

_log_format = f"""%(time_send)s %(message)s; %(asctime)s.%(msecs)03d; %(message_accept)s """
_log_format_keepalive = "-; -; -; %(asctime)s.%(msecs)03d; %(message_accept)s"
def get_file_handler(log_format):
    file_handler = logging.FileHandler("x.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, "%Y-%m-%d; %H:%M:%S"))
    return file_handler

def get_logger(name, log_format):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(log_format))
    return logger

logger1 = get_logger("log_default", _log_format)
logger2 = get_logger("log_ignore", _log_format_keepalive)
logger1.propagate = False
logger2.propagate = False

def log_client(time_send, message_send, message_accept, keepAlive=False):
    if not keepAlive:
        logger_out = logging.LoggerAdapter(logger1, {"time_send": time_send, "message_accept": message_accept})
    else:
        logger_out = logging.LoggerAdapter(logger2, {"message_accept": message_accept})
    logger_out.info(message_send)