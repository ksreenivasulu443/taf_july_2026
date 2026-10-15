import csv
import threading
from src.core.run_context import get_run_id, get_report_dir, get_log_dir
from datetime import datetime

# _name private variable
# __name strict private variable oops(class and objects)
# _function private function ( local to this specific python module file)

_lock = threading.Lock()


HEADERS = [
    "run_id",
    "timestamp",
    "validation",
    "status",
    "duration_seconds",
    "details"
]

REPORT_DIR = get_report_dir()

CSV_REPORT = REPORT_DIR / "validation_report.csv"
HTML_REPORT = REPORT_DIR / "validation_report.html"
SUMMARY_REPORT = REPORT_DIR / "summary.txt"

def _create_report():

    if CSV_REPORT.exists():
        return

    with CSV_REPORT.open(
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(HEADERS)

def write_output(validation_type,
        status,
        duration_seconds,
        details):
    with _lock:
        _create_report()

        with CSV_REPORT.open(
                mode="a",
                newline="",
                encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            writer.writerow([
                get_run_id(),
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                validation_type,
                status,
                duration_seconds,
                details
            ])
