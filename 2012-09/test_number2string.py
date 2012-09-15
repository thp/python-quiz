
from number2string import number2string
from number2string_minimal import f

from nose.tools import assert_equal

def check_result(x, y):
    assert_equal(number2string(x), y)
    assert_equal(f(x), y)

def test_number2string():
    yield check_result, '10', '10'
    yield check_result, '100', '100'
    yield check_result, '1000', '1.000'
    yield check_result, '1000000', '1.000.000'
    yield check_result, '1999995.99', '1.999.995,99'
    yield check_result, '1337.88888', '1.337,88888'

def check_result_altsep(x, y):
    assert_equal(number2string(x, ',', '.'), y)
    assert_equal(f(x, ',', '.'), y)

def test_number2string_altsep():
    yield check_result_altsep, '1000', '1,000'
    yield check_result_altsep, '1000000', '1,000,000'
    yield check_result_altsep, '1999995.99', '1,999,995.99'

