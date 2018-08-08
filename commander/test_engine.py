from engine import Engine


def test_connection():
    engine = Engine()
    engine.connect(wait_ready=False)

    assert engine.vehicle is not None
