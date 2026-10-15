import time

from src.utility.report_lib import write_output


def count_check(source_df, target_df, key_columns=None):

    start_time = time.perf_counter()

    # Count source and target records
    src_cnt = source_df.count()
    tgt_cnt = target_df.count()

    # Calculate count difference
    difference = abs(src_cnt - tgt_cnt)

    # Validate counts
    if src_cnt == tgt_cnt:

        status = "PASS"

        details = (
            f"Source={src_cnt}, "
            f"Target={tgt_cnt}, "
            f"Difference=0"
        )

    else:

        status = "FAIL"

        details = (
            f"Source={src_cnt}, "
            f"Target={tgt_cnt}, "
            f"Difference={difference}"
        )

    # Calculate execution duration
    duration = round(
        time.perf_counter() - start_time,
        3
    )

    # Write validation result to report
    write_output(
        validation_type="Count Check",
        status=status,
        duration_seconds=duration,
        details=details
    )

    return status