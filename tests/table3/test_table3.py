
from src.data_validations.count_validation import count_check

from src.data_validations.records_only_source import record_only_source
from src.data_validations.records_only_target import record_only_target
from src.data_validations.duplicate_validation import duplicate_check
from src.data_validations.uniqueness_validation import uniqueness_check
from src.data_validations.not_null_validation import  null_value_check

def test_count(read_data):
    source, target = read_data
    status = count_check(source, target)

    assert status =='PASS'

def test_records_only_source(read_data, read_config):
    source, target = read_data
    config,_ = read_config
    key_columns = config['validation_config']['key_columns']
    num_records = config['validation_config']['num_records']
    status = record_only_source(source, target, key_columns, num_records=num_records)

    assert status == 'PASS'

def test_records_only_target(read_data, read_config):
    source, target = read_data
    config,_ = read_config
    key_columns = config['validation_config']['key_columns']
    num_records = config['validation_config']['num_records']
    status = record_only_target(source, target, key_columns, num_records=num_records)

    assert status == 'PASS'

def test_duplicate(read_data, read_config):
    _, target = read_data
    config,_ = read_config
    key_columns = config['validation_config']['key_columns']
    num_records = config['validation_config']['num_records']
    status = duplicate_check( target, key_columns, num_records=num_records)

    assert status == 'PASS'

def test_unique_check(read_data, read_config):
    _, target = read_data
    config,_ = read_config
    unique_cols = config['validation_config']['unique_cols']
    status = uniqueness_check(df = target,
                              unique_cols=unique_cols
                              )

    assert status == 'PASS'

def test_not_null_check(read_data, read_config):
    _, target = read_data
    config,_ = read_config
    not_null_cols = config['validation_config']['not_null_cols']
    num_records = config['validation_config']['num_records']
    status = null_value_check( df =target,
                               not_null_columns=not_null_cols,
                               failed_records=num_records)

    assert status == 'PASS'