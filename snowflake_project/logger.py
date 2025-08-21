import logging
import os
from datetime import datetime


# Get the folder where main.py resides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FOLDER_NAME = os.path.join(BASE_DIR, "logs")
LOG_FOLDER_NAME = 'logs'
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

os.makedirs(LOG_FOLDER_NAME,exist_ok=True)

LOG_FILE_NAME_FINAL = os.path.join(LOG_FOLDER_NAME,LOG_FILE_NAME)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
logging.basicConfig(
    filename=LOG_FILE_NAME_FINAL,
    level=logging.INFO,
    format='%(asctime)s [Thread %(threadName)s - ID %(thread)d] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
