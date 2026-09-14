import logging
import os

log_path = "log/"
if not os.path.exists(log_path):
    os.makedirs(log_path)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_path}app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("PetSystem")