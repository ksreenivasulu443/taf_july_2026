import os

import pytest
import os
import yaml
from pyspark.sql import SparkSession
from src.utility.read_file_lib import read_file

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
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("etl automation framework") \
        .getOrCreate()

    return spark

@pytest.fixture(scope="module")
def read_data( read_config, spark_session):
    spark = spark_session
    config,dir_path = read_config
    dir_path = request.node.fspath.dirname

    source_config = config.get("source_config",{})
    target_config = config.get("target_config",{})
    validation_config = config.get("validation_config",{})

    if source_config['type'] == 'database':
        #source = read_db()
        pass
    else:
        source = read_file(spark=spark,
                           file_type = source_config['type'],
                           file_path = source_config['path'],
                           file_config = source_config['file_config'],
                           dir_path = dir_path )

    if target_config['type'] == 'database':
        #source = read_db()
        pass
    else:
        target = read_file(spark=spark,
                           file_type = target_config['type'],
                           file_path = target_config['path'],
                           file_config = target_config['file_config'],
                           dir_path = dir_path )



    return source, target





