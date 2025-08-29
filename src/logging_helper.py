import logging
import os

logging_dir = "LOGS"
logging_name = "logs.txt"

logging_path = os.path.join(logging_dir, logging_name)

if not os.path.exists(logging_dir):
    os.mkdir(logging_dir)

logging.basicConfig(filename=logging_path,
                    level=logging.INFO,
                    format='%(asctime)s:%(filename)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
