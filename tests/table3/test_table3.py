def test_count(read_data):
    source, target = read_data
    source.show()
    target.show()
    source.printSchema()
    assert True