import os
from dotenv import load_dotenv

load_dotenv()



def read_db(spark,config, dir_path):
    df = spark.read.format("jdbc") \
        .option("url", os.getenv("URL")) \
        .option("user", os.getenv("USER_NAME")) \
        .option("password", os.getenv("DB_PASSWORD")) \
        .option("dbtable", config['table']) \
        .option("driver", os.getenv("DRIVER_CLASS")) \
        .load()

    return df



