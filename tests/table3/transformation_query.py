# from pyspark.sql import functions as F
#
# result_df = (
#     df.filter(F.col("customer_id") > 103)
#       .select(
#           F.col("customer_id").alias("SNO"),
#           F.col("name"),
#           F.coalesce(
#               F.col("email"),
#               F.lit("unkwn@gmail.com")
#           ).alias("email"),
#           F.col("phone")
#       )
# )
#
# result_df.show()
#
# source1 = spark.read.csv()
#
# source2 = spark.read.jdbc()
#
# source3 = spark.readStream()
#
# final = source1.union(source2).union(source3)