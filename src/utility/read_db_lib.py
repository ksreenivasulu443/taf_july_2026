import os
from dotenv import load_dotenv

creds = load_dotenv()

print(creds)

print(os.getenv("USER_NAME"))
print(os.getenv("DB_PASSWORD"))
print(os.getenv("DRIVER_CLASS"))
print(os.getenv("URL"))

def read_db(spark,config, dir_path):
    df = spark.read.format("jdbc") \
        .option("url", os.getenv("URL")) \
        .option("user", os.getenv("USER_NAME")) \
        .option("password", os.getenv("DB_PASSWORD")) \
        .option("table", config['table']) \
        .option("driver", os.getenv("DRIVER_CLASS")) \
        .load()

    return df
