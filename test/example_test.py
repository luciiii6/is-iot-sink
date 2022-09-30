import pytest
import datetime

def test_example():
    assert True

TIMESTAMP_FUTURE = 1664526180
def test_get_delay():
    value = TIMESTAMP_FUTURE - datetime.datetime.now().timestamp()
    assert value > 0