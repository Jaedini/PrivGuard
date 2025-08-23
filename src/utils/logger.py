import os
import logging
from pathlib import Path

def appdata_dir() -> str:
    base = os.getenv("APPDATA") or os.path.join(Path.home(), ".config")
    p = os.path.join(base, "PrivGuard")
    os.makedirs(p, exist_ok=True)
    return p

def log_file_path() -> str:
    return os.path.join(appdata_dir(), "privguard.log")

logging.basicConfig(
    filename=log_file_path(),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("PrivGuard gestartet")
