import logging
import sys
from bot_service.settings import LOGS_FILE


logging.basicConfig(
    filename=LOGS_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи в файл
)


def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    logging.error("Необработанное исключение", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = log_uncaught_exceptions
