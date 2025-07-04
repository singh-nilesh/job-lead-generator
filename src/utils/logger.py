import logging
import os
from datetime import datetime

# Store in Logs folder 
LOG_FILE = f"{datetime.now().strftime('%d-%m-%Y__%H:%M:%S')}.log"
logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info(" Logging has started")