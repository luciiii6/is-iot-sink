import pytest
from is_iot_sink.sink import Sink
from test.helper import TestHelper

TestHelper.suite_setup()

def test_smoke_test():
    settings = TestHelper.default_test_settings()
    sink = Sink(settings)

    sink.start()
    assert sink.status() == True

    sink.stop()
    assert sink.status() == False

TestHelper.suite_teardown()
