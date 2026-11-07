from src.utility.report_lib import write_output
import time
def record_only_target(source,target, key_columns,num_records=5):
    start_time = time.perf_counter()
    record_only_target_df = target.select(key_columns).join(source.select(key_columns), on = key_columns, how = 'left_anti')

    missing_count = record_only_target_df.count()


    if missing_count == 0:
        status = 'PASS'
        details = {
            f"Source={source.count()}, "
            f"Target={target.count()}, "
            f"missing_count={missing_count}",
            f"sample_missing_primary_key=No missing records"
        }
    else:
        status = 'FAIL'
        details = {
            f"Source={source.count()}, "
            f"Target={target.count()}, "
            f"missing_count={missing_count}",
            f"sample_missing_primary_key={record_only_target_df.limit(num_records).collect()}"
        }

    duration = round(
        time.perf_counter() - start_time,
        3
    )

    print("record_only_target func duration: ", duration)

    write_output(
        validation_type="records only in target",
        status=status,
        duration_seconds=duration,
        details=details
    )

    return status

