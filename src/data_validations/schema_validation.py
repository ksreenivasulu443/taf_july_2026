
import time

from src.utility.report_lib import write_output

def schema_check(source, target):

    start_time = time.perf_counter()

    source_schema = {
        field.name.lower(): field.dataType.simpleString()
        for field in source.schema.fields
    }

    print("source_schema",source_schema )

    target_schema = {
        field.name.lower(): field.dataType.simpleString()
        for field in target.schema.fields
    }

    print("target_schema", target_schema)

    all_columns = sorted(
        set(source_schema.keys()) | set(target_schema.keys())
    )

    print("all columns",all_columns)

    failures = []

    for column in all_columns:

        source_type = source_schema.get(column)
        target_type = target_schema.get(column)

        if source_type != target_type:

            failures.append({
                "column": column,
                "source_data_type": source_type,
                "target_data_type": target_type
            })

    failed_count = len(failures)

    if failed_count > 0:

        status = "FAIL"

        details = (
            f"Schema failed columns count={failed_count}, "
            f"Failures={failures}"
        )

    else:

        status = "PASS"
        details = "Source and target schemas match."

    duration = round(time.perf_counter() - start_time, 3)

    write_output(
        validation_type="Schema Check",
        status=status,
        details=details,
        duration_seconds=duration
    )

    return status


