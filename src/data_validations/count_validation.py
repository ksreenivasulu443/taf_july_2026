
import time

def count_check(source, target):
    start_time = time.perf_counter()
    src_cnt = source.count()
    tgt_cnt = target.count()
    difference = abs(src_cnt - tgt_cnt)

    if difference == 0:
        status = True
        print(f"Source count is {src_cnt} and target count is {tgt_cnt} and difference is {difference}")
    else:
        status = False
        print(f"Source count is {src_cnt} and target count is {tgt_cnt} and difference is {difference}")

    duration = round(
        time.perf_counter() - start_time,
        3
    )

    print("count func duration: ", duration)

    return status