from pyspark.sql.functions import lit, col, when, concat, sha2
from src.utility.report_lib import write_output



def data_compare(source_df, target_df, key_columns,num_records=10):
    smt = source_df.exceptAll(target_df).withColumn("datafrom", lit("source"))
    tms = target_df.exceptAll(source_df).withColumn("datafrom", lit("target"))
    failed = smt.union(tms)
    failed = failed.persist()
    failed_count = failed.count()

    if failed_count > 0:
        failed_records = failed.limit(num_records).collect()  # Get the first 5 failing rows
        failed_preview = [row.asDict() for row in failed_records]
        write_output(
            "data compare Check",
            "FAIL",
            "0"
            f"Data mismatch data: {failed_preview}"
        )


    else:
        write_output(
            "data compare Check",
            "PASS",
            '0'
            f"No mismatches found"
        )

    if failed_count > 0:
        failed2 = failed.select(key_columns).distinct().withColumn("hash_key",
                                                                  sha2(concat(*[col(c) for c in key_columns]), 256))
        source_df = source_df.withColumn("hash_key", sha2(concat(*[col(c) for c in key_columns]), 256)). \
            join(failed2, ["hash_key"], how='left_semi').drop('hash_key')
        target_df = target_df.withColumn("hash_key", sha2(concat(*[col(c) for c in key_columns]), 256)). \
            join(failed2, ["hash_key"], how='left_semi').drop('hash_key')

        print("after hash filter")
        source_df.show() #failed rows 101,104
        target_df.show() # failed 101,104

        columnList = source_df.columns# [customer_id,name,email,phone, batchid]
        print("columnList", columnList)
        print("keycolumns", key_columns) #['customer_id']
        for column in columnList: # column = email
            if column not in key_columns: # name not in ['customer_id'] #
                key_columns.append(column) # ['customer_id','phone']
                temp_source = source_df.select(key_columns).withColumnRenamed(column, "source_" + column)

                temp_target = target_df.select(key_columns).withColumnRenamed(column, "target_" + column)
                key_columns.remove(column) # ['customer_id']
                temp_join = temp_source.join(temp_target, key_columns, how='full_outer')
                (temp_join.withColumn("comparison", when(col('source_' + column) == col("target_" + column),
                                                         "True").otherwise("False")).
                 filter("comparison == False ").show())

        status ='FAIL'

        return status
    else:
        status = 'PASS'
        return status












