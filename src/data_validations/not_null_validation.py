
import time

from pyspark.sql import functions as F
from src.utility.report_lib import write_output


NULL_LIKE_VALUES = ["NA", "NULL", "NONE", "N/A", "UNKNOWN", 'NUL','?']



def null_value_check(df, not_null_columns, failed_records=5):

    start_time = time.perf_counter()

    failures = []

    for column in not_null_columns:

        value_as_string = F.trim(F.col(column).cast("string"))

        failing_rows = df.filter(
            F.col(column).isNull()
            | (value_as_string == "")
            | F.upper(value_as_string).isin(NULL_LIKE_VALUES)
        )

        null_count = failing_rows.count()

        if null_count > 0:

            sample_rows = failing_rows.limit(failed_records).collect()

            failed_preview = [
                row.asDict(recursive=True)
                for row in sample_rows
            ]


            failures.append({
                "column": column,
                "null_count": null_count,
                "sample_failed_records": failed_preview
            })

    if failures:
        status = "FAIL"
        details = f"Failures={failures}"
    else:
        status = "PASS"
        details = "No null, empty, or configured null-like values found."

    duration = round(time.perf_counter() - start_time, 3)

    write_output(
        validation_type="Null Value Check",
        status=status,
        details=details,
        duration_seconds=duration
    )

    return status
