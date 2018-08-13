import time

from engine import Engine


def test_connection():
    engine = Engine()
    engine.connect(wait_ready=False)

    assert engine.vehicle is not None

    engine.vehicle.close()

def test_wait_armable_vehicle():
    engine = Engine()
    engine.connect(wait_ready=False)

    while not engine.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    assert engine.vehicle.is_armable

    engine.vehicle.close()

def test_vehicle_mode():
    engine = Engine()
    engine.connect(wait_ready=False)

    while not engine.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    assert engine.vehicle.is_armable

    print("\nSet Vehicle.mode = GUIDED (currently: %s)" % engine.vehicle.mode.name)

    engine.set_guided_mode()

    assert engine.vehicle.mode.name=='GUIDED'

    engine.vehicle.close()

def test_vehicle_armed():
    engine = Engine()
    engine.connect(wait_ready=False)

    while not engine.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    assert engine.vehicle.is_armable

    engine.arm()

    assert engine.vehicle.armed

    engine.vehicle.close()

# def test_set_sail():
#     engine = Engine()

#     engine.connect(True)
#     print(engine.vehicle.location.global_frame.lat)
#     print(engine.vehicle.location.global_frame.lon)
#     engine.goto(-4.6540196, 55.3995094)

#     while engine.vehicle.location.global_frame.lat < -4:
#         print('Lat:', engine.vehicle.location.global_frame.lat)

#     assert engine.vehicle.location.global_frame.lat == -4.6540196
#     assert engine.vehicle.location.global_frame.lon == 55.3995094

#     engine.vehicle.close()