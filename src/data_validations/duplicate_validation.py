
from src.utility.report_lib import write_output
import time
def duplicate_check(df, key_columns, num_records):
    start_time = time.perf_counter()
    duplicates = df.groupby(key_columns).count().filter('count>1')

    duplicates_count = duplicates.count()

    if  duplicates_count == 0:
        status = 'PASS'
        details = {
            f"Target={df.count()}, "
            f"duplicate_count={duplicates_count}",
            f"sample duplicate=No duplicates"
        }

    else:
        status = 'FAIL'
        details = {
            f"Target={df.count()}, "
            f"duplicate_count={duplicates_count}",
            f"sample duplicate={duplicates.limit(num_records).collect()}"
        }

    duration = round(
        time.perf_counter() - start_time,
        3
    )

    print("record_only_target func duration: ", duration)

    write_output(
        validation_type="duplicate_check",
        status=status,
        duration_seconds=duration,
        details=details
    )

    return status
