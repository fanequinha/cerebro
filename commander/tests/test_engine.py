import time

from engine import Engine


def test_connection(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    assert engine.vehicle is not None

    engine.vehicle.close()


def test_wait_armable_vehicle(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    while not engine.vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    assert engine.vehicle.is_armable

    engine.vehicle.close()


def test_vehicle_mode(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    engine.set_mode('GUIDED')

    assert engine.vehicle.mode.name == 'GUIDED'

    engine.vehicle.close()


def test_vehicle_armed(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    engine.arm()

    assert engine.vehicle.armed

    engine.vehicle.close()


def test_set_sail(connection_parameters):
    engine = Engine(**connection_parameters)

    engine.connect(True)
    engine.vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not engine.vehicle.armed:
        print(" Waiting for arming...")
        print(" vehicle mode: %s" % engine.vehicle.mode)

        time.sleep(1)

    engine.set_mode('GUIDED')

    print("Set default/target groundspeed to 3")
    engine.vehicle.groundspeed = 10

    lat_point = 42.227870
    long_point = -8.719468

    engine.goto(lat_point, long_point)

    while engine.vehicle.location.global_frame.lat < lat_point:
        print('Lat:', engine.vehicle.location.global_frame.lat)

    assert 42.227860 < engine.vehicle.location.global_frame.lat < 42.227890

    engine.vehicle.close()
