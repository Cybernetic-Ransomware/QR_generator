import logging
from logging.handlers import RotatingFileHandler


class AppLogger:
    logger = None

    @staticmethod
    def configure_logger(log_file='app.log', log_level=logging.ERROR, max_bytes=1048576, backup_count=3):
        AppLogger.logger = logging.getLogger()
        AppLogger.logger.setLevel(log_level)

        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        AppLogger.logger.addHandler(handler)
