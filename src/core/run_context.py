from datetime import datetime
from pathlib import Path
import os


# One ID generated once for the entire pytest execution
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = PROJECT_ROOT / "logs" / f"run_{RUN_ID}"


REPORT_DIR = PROJECT_ROOT / "reports" / f"run_{RUN_ID}"

LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def get_run_id():
    return RUN_ID


def get_log_dir():
    return LOG_DIR


def get_report_dir():
    return REPORT_DIR