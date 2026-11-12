
from src.data_validations.count_validation import count_check

def test_count(read_data):
    source, target = read_data
    status = count_check(source, target)
    source.show()
    target.show()

    assert status[0] =='PASS'