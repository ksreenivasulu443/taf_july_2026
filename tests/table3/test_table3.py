
from src.data_validations.count_validation import count_check

from src.data_validations.records_only_source import record_only_source
from src.data_validations.records_only_target import record_only_target
from src.data_validations.duplicate_validation import duplicate_check

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