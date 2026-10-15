
from src.data_validations.count_validation import count_check

def test_count(read_data):
    source, target = read_data
    status = count_check(source, target)

    assert status =='PASS'

# def test_duplicate(read_data):
#     source, target = read_data
#     status = duplicate_check(source, target)
#
#     assert status