import pytest

import settings


@pytest.fixture
def connection_parameters():
    connection_string = settings.DEFAULT_SERIAL_PORT
    baud_rate = settings.DEFAULT_BAUD_RATE

    return {'connection_string': connection_string, 'baudrate': baud_rate}
