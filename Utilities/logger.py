from loguru import logger
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    f"{LOG_DIR}/app.log",
    rotation="1 MB",
    retention="7 days",
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<cyan>{level}</cyan> | "
           "{message}"
)

__all__ = ["logger"]
