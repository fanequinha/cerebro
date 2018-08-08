from engine import Mision


def test_connection():
    engine = Mision()
    engine.connect()

    assert engine.vehicle is not None
