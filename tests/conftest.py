import pytest
import os
import yaml
from pyspark.sql import SparkSession
from src.utility.read_file_lib import read_file
from src.utility.read_db_lib import read_db
from src.utility.report_lib import generate_summary,generate_html_report

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

# ============================================================
# Spark Session Fixture
# ============================================================

@pytest.fixture(scope="session")
def spark_session():
    print("this spark session")

    taf_july = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))

    azure_storage = os.path.join(taf_july,"jars","azure-storage-8.6.6.jar")

    hadoop_azure = os.path.join(taf_july,"jars","hadoop-azure-3.3.1.jar")

    sql_server = os.path.join(taf_july,"jars","mssql-jdbc-13.4.0.jre11.jar")

    jar_path = ",".join([azure_storage,hadoop_azure,sql_server])

    print("\nStarting Spark Session")
    print("Project Path :", taf_july)
    print("Jar Path :", jar_path)

    spark = (
        SparkSession.builder
        .master("local[1]")
        .config("spark.jars", jar_path)
        .config("spark.driver.extraClassPath", jar_path)
        .config("spark.executor.extraClassPath", jar_path)
        .appName("ETL Automation FW")
        .getOrCreate()
    )

    print("Spark Version :", spark.version)

    adls_account_name = os.getenv(
        "ADLS_ACCOUNT_NAME"
    )

    key = os.getenv(
        "ADLS_TOKEN"
    )

    spark.conf.set(
        f"fs.azure.account.auth.type.{adls_account_name}.dfs.core.windows.net",
        "SharedKey"
    )

    spark.conf.set(
        f"fs.azure.account.key.{adls_account_name}.dfs.core.windows.net",
        key
    )

    yield spark

    print("\nStopping Spark Session")

    #spark.stop()


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

    else:
        target = read_file(spark=spark,
                           file_type = target_config['type'],
                           file_path = target_config['path'],
                           file_config = target_config['file_config'],
                           dir_path = dir_path )

    source= source.drop(
        *source_config.get("exclude_cols", [])
    )

    target = target.drop(
        *target_config.get("exclude_cols", [])
    )

    return source, target

TEST_STATS = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0
}

def pytest_sessionfinish(
        session,
        exitstatus
):


        generate_summary(
            TEST_STATS
        )

        generate_html_report(
            TEST_STATS
        )

def pytest_runtest_logreport(report):

    # Only count actual test execution.
    # Do not count setup and teardown.
    if report.when != "call": # report.when 'setup', 'tear_down', 'call'
        return

    TEST_STATS["total"] += 1

    if report.passed:

        TEST_STATS["passed"] += 1

    elif report.failed:

        TEST_STATS["failed"] += 1

    elif report.skipped:

        TEST_STATS["skipped"] += 1



