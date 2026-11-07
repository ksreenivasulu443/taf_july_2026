
import time
from src.utility.report_lib import write_output


def uniqueness_check(df, unique_cols):

    start_time = time.perf_counter()

    duplicate_counts = {} #'customer': 0, 'email':0

    for column in unique_cols:

        dup_df = (
            df.groupBy(column)
            .count()
            .filter("count > 1")
        )

        count_duplicates = dup_df.count()

        duplicate_counts[column] = count_duplicates

    status = (
        "PASS"
        if all(count == 0 for count in duplicate_counts.values())
        else "FAIL"
    )

    details = f"Duplicate groups per column={duplicate_counts}"

    duration = round(time.perf_counter() - start_time, 3)

    write_output(
        validation_type="Uniqueness Check",
        status=status,
        details=details,
        duration_seconds=duration
    )

    return status
