import logging
from pathlib import Path


LOG_DIRECTORY = Path("logs")

LOG_FILE = LOG_DIRECTORY / "knowledge.log"


# Create logs folder if not available
LOG_DIRECTORY.mkdir(exist_ok=True)


# Configure logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def log_info(message):
    """
    Store normal information logs
    """

    logging.info(message)
if __name__ == "__main__":
    log_info("Logger test successful")
    print("Check logs/knowledge.log")


def log_error(message):
    """
    Store error logs
    """

    logging.error(message)



def log_warning(message):
    """
    Store warning logs
    """

    logging.warning(message)