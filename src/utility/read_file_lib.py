from src.utility.helpers import read_schema, flatten

def read_file(spark, file_type, file_path, file_config,dir_path):
    file_type =  file_type.lower()
    if file_type == "csv":
        if file_config['schema'].upper() == 'Y':
            schema = read_schema(dir_path)
            df = spark.read.schema(schema).csv(file_path,
                                               header=file_config['header'],
                                               sep=file_config['sep'])
        else:
            df = spark.read.csv(file_path, header=file_config['header'],
                                               sep=file_config['sep'],
                                                inferSchema=file_config['inferSchema'])
    elif file_type == "parquet":
        df = spark.read.parquet(file_path)
    elif file_type == "json":
        if file_config['multiline'] == 'Y':
            df = spark.read.json(file_path, multiLine=True)
            df = flatten(df)
        else:
            df = spark.read.json(file_path, multiLine=False)
            df = flatten(df)
    elif file_type == "arvo":
        df = spark.read.format('avro').load(file_path)
    elif file_type == "dat":
        df = spark.read.csv(file_path, header=True, inferSchema=True)
    elif file_type == "xml":
        df = spark.read.format('xml').load(file_path)

    return df