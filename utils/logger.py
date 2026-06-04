import logging
from logging.handlers import RotatingFileHandler

LOGGER_NAME = 'qrgen'


class AppLogger:
    logger = logging.getLogger(LOGGER_NAME)

    @staticmethod
    def configure_logger(log_file='app.log', log_level=logging.ERROR, max_bytes=1048576, backup_count=3):
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(log_level)
        if not logger.handlers:
            handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            handler.setLevel(log_level)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
        AppLogger.logger = logger
