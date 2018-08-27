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


def test_vehicle_armed_and_disarmed(connection_parameters):
    engine = Engine(**connection_parameters)
    engine.connect(wait_ready=False)

    engine.arm()
    assert engine.vehicle.armed

    engine.disarm()
    assert not engine.vehicle.armed

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
    # from dronekit import VehicleMode
    # engine.vehicle.mode = VehicleMode("GUIDED")
    print("Taking off!")
    engine.vehicle.simple_takeoff(10)  # Take off to target altitude
    #  # Wait until the vehicle reaches a safe height before processing the goto
    # #  (otherwise the command after Vehicle.simple_takeoff will execute
    # #   immediately).
    while True:
        print(" Altitude: ", engine.vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if engine.vehicle.location.global_relative_frame.alt >= 10 * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

    print("Set default/target groundspeed to 3")
    engine.vehicle.groundspeed = 3

    print(engine.vehicle.location.global_frame.lat)
    print(engine.vehicle.location.global_frame.lon)
    engine.goto(-4.6540196, 55.3995094)

    while engine.vehicle.location.global_frame.lat < -4:
        print('Lat:', engine.vehicle.location.global_frame.lat)

    assert engine.vehicle.location.global_frame.lat == -4.6540196
    assert engine.vehicle.location.global_frame.lon == 55.3995094

    engine.vehicle.close()