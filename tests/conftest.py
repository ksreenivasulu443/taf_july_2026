import pytest
import os
import yaml
from pyspark.sql import SparkSession
from src.utility.read_file_lib import read_file
from src.utility.read_db_lib import read_db

@pytest.fixture(scope="module")
def read_config(request):
    dir_path = request.node.fspath.dirname

    print("dir_path", dir_path)
    config_path = os.path.join(dir_path, "config.yml")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    print("config", config)
    # print("config keys", config.keys())
    # print(config.get("dummy", 0))
    # print("source config", config["dummy"])

    return config,dir_path

@pytest.fixture(scope="session")
def spark_session():
    taf_path = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    sql_server_jar = os.path.join(taf_path, "jars", "mssql-jdbc-13.4.0.jre11.jar")

    spark = SparkSession.builder \
        .master("local[1]") \
        .config("spark.jars", sql_server_jar) \
        .config("spark.driver.extraClassPath", sql_server_jar) \
        .config("spark.executor.extraClassPath", sql_server_jar) \
        .appName("etl automation framework") \
        .getOrCreate()

    return spark

@pytest.fixture(scope="module")
def read_data( read_config, spark_session):
    spark = spark_session
    config,dir_path = read_config
    source_config = config.get("source_config",{})
    target_config = config.get("target_config",{})
    validation_config = config.get("validation_config",{})

    if source_config['type'] == 'database':
        source = read_db(spark=spark,
                         config=source_config,
                         dir_path=dir_path)
        pass
    else:
        source = read_file(spark=spark,
                           file_type = source_config['type'],
                           file_path = source_config['path'],
                           file_config = source_config['file_config'],
                           dir_path = dir_path )

    if target_config['type'] == 'database':
        target = read_db(spark=spark,
                config=target_config,
                dir_path=dir_path)
        pass
    else:
        target = read_file(spark=spark,
                           file_type = target_config['type'],
                           file_path = target_config['path'],
                           file_config = target_config['file_config'],
                           dir_path = dir_path )



    return source, target





