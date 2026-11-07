from src.data_validations.count_validation import count_check


def test_count(read_data, read_config):
    source_df, target_df = read_data
    source_df.show()
    target_df.show()
    config = read_config
    key_columns = config['validation']['key_columns']
    status = count_check(source_df=source_df, target_df=target_df, key_columns=key_columns)
    assert status == 'PASS'
